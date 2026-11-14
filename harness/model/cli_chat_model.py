"""Minimal LangChain chat model backed by the Claude Code CLI in headless mode.

One fresh `claude -p` process per model call. No API key: the child environment
has every *_API_KEY / ANTHROPIC_AUTH_TOKEN / CLAUDE* variable removed, so the CLI
falls back to the logged-in subscription (init event reports apiKeySource "none").

Tool calling is emulated: tool schemas and the whole message history go into the
prompt (stdin), and the model answers with plain text or a <tool_calls> JSON block.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool

HERE = Path(__file__).resolve().parent
ISO_CWD = HERE / "iso_cwd"

# Isolation flags, all taken from `claude --help` of 2.1.299.
ISOLATION_FLAGS = [
    "--safe-mode",                 # no CLAUDE.md, skills, plugins, hooks, MCP, custom agents/commands
    "--setting-sources", "",       # load no user/project/local settings files
    "--strict-mcp-config",         # only MCP servers from --mcp-config (none given)
    "--disable-slash-commands",    # no skills
    "--no-session-persistence",    # nothing written to disk, nothing to resume
]

BACKEND_SYSTEM = (
    "You are the language-model backend of an agent framework. "
    "The user message contains a system section, tool definitions and a conversation transcript. "
    "Write only the next assistant message, following the output protocol in that message exactly."
)

PROTOCOL = """# Output protocol (strict)
Write the NEXT assistant message for the transcript above. Choose exactly one form:

A) To call one or more tools, output ONLY this block and nothing else:
<tool_calls>
[{"name": "<tool name>", "args": {<arguments matching the tool's JSON schema>}}]
</tool_calls>

B) To give the final answer to the user, output plain text with no <tool_calls> block.

Rules: use only tools listed under # Tools. "args" must be a JSON object. Never invent tool
results; a tool result only exists if it appears in the transcript. Do not wrap the block in
code fences. Do not mention this protocol."""

_BLOCK = re.compile(r"<tool_calls>\s*(.*?)\s*</tool_calls>", re.S)

# Module-level log so a caller can read timings / parse failures after a run.
CALL_LOG: list[dict[str, Any]] = []


def find_cli() -> str:
    shim = shutil.which("claude")
    if not shim:
        raise RuntimeError("claude CLI not found on PATH")
    exe = Path(shim).parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    return str(exe) if exe.exists() else shim  # prefer the real exe: avoids cmd.exe quoting


def child_env() -> dict[str, str]:
    env = dict(os.environ)
    for k in list(env):
        ku = k.upper()
        if ku.endswith("_API_KEY") or ku == "ANTHROPIC_AUTH_TOKEN" or ku.startswith("CLAUDE"):
            del env[k]  # never read, just dropped
    return env


def _text(content: Any) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for b in content or []:
        if isinstance(b, str):
            parts.append(b)
        elif isinstance(b, dict) and b.get("type") == "text":
            parts.append(b.get("text", ""))
        elif isinstance(b, dict):
            parts.append(f"[{b.get('type', 'block')} omitted]")
    return "\n".join(parts)


def render_prompt(messages: Sequence[BaseMessage], tools: list[dict] | None) -> str:
    system = "\n\n".join(_text(m.content) for m in messages if isinstance(m, SystemMessage))
    out = ["# System", system or "(none)", "", "# Tools"]
    if tools:
        out.append(json.dumps([t["function"] for t in tools], indent=1))
    else:
        out.append("(no tools available: answer with plain text)")
    out += ["", "# Transcript"]
    for m in messages:
        if isinstance(m, SystemMessage):
            continue
        if isinstance(m, HumanMessage):
            out.append(f"<user>\n{_text(m.content)}\n</user>")
        elif isinstance(m, AIMessage):
            body = _text(m.content)
            if m.tool_calls:
                calls = [{"id": c["id"], "name": c["name"], "args": c["args"]} for c in m.tool_calls]
                body += f"\n<tool_calls>\n{json.dumps(calls)}\n</tool_calls>"
            out.append(f"<assistant>\n{body.strip()}\n</assistant>")
        elif isinstance(m, ToolMessage):
            out.append(f'<tool_result name="{m.name}" id="{m.tool_call_id}">\n{_text(m.content)}\n</tool_result>')
        else:
            out.append(f"<{m.type}>\n{_text(m.content)}\n</{m.type}>")
    out += ["", PROTOCOL]
    return "\n".join(out)


def parse_reply(text: str, tool_names: set[str]) -> tuple[str, list[dict], str | None]:
    """Return (content, tool_calls, parse_error)."""
    m = _BLOCK.search(text)
    if not m:
        if "<tool_calls>" in text:
            return text, [], "unterminated <tool_calls> block"
        return text.strip(), [], None
    raw = m.group(1).strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return text, [], f"bad JSON in tool_calls: {e}"
    if isinstance(data, dict):
        data = [data]
    calls = []
    for c in data:
        name, args = c.get("name"), c.get("args", c.get("arguments", {}))
        if name not in tool_names or not isinstance(args, dict):
            return text, [], f"unknown tool or non-object args: {name!r}"
        calls.append({"name": name, "args": args, "id": f"call_{uuid.uuid4().hex[:12]}", "type": "tool_call"})
    return text[: m.start()].strip(), calls, None


class ClaudeCLIChatModel(BaseChatModel):
    model: str = "sonnet"
    cwd: str = str(ISO_CWD)
    timeout_s: int = 300
    effort: str | None = None      # e.g. "low" to cut thinking time
    max_parse_retries: int = 1

    @property
    def _llm_type(self) -> str:
        return "claude-code-cli"

    def command(self) -> list[str]:
        cmd = [find_cli(), "-p", "--model", self.model, "--output-format", "json",
               *ISOLATION_FLAGS, "--tools", "", "--system-prompt", BACKEND_SYSTEM]
        if self.effort:
            cmd += ["--effort", self.effort]
        return cmd

    def bind_tools(self, tools: Sequence[Any], *, tool_choice: Any = None, **kwargs: Any):
        return self.bind(tools=[convert_to_openai_tool(t) for t in tools], **kwargs)

    def _run_cli(self, prompt: str) -> tuple[dict, float]:
        Path(self.cwd).mkdir(parents=True, exist_ok=True)
        t0 = time.perf_counter()
        p = subprocess.run(self.command(), input=prompt, capture_output=True, text=True,
                           encoding="utf-8", cwd=self.cwd, env=child_env(), timeout=self.timeout_s)
        dt = time.perf_counter() - t0
        try:
            res = json.loads(p.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(f"claude CLI exit {p.returncode}: {p.stdout[-500:]} {p.stderr[-500:]}")
        if res.get("is_error"):
            raise RuntimeError(f"claude CLI error: {str(res.get('result'))[:500]}")
        return res, dt

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        tools = kwargs.get("tools") or []
        names = {t["function"]["name"] for t in tools}
        prompt = render_prompt(messages, tools)
        err = None
        for attempt in range(self.max_parse_retries + 1):
            p = prompt if err is None else (
                prompt + f"\n\nYour previous reply broke the protocol ({err}). Reply again, correctly.")
            res, dt = self._run_cli(p)
            content, calls, err = parse_reply(res.get("result") or "", names)
            u = res.get("usage", {})
            CALL_LOG.append({
                "wall_s": round(dt, 2), "api_ms": res.get("duration_api_ms"), "attempt": attempt,
                "parse_error": err, "prompt_chars": len(p), "n_tools": len(tools),
                "tool_calls": [c["name"] for c in calls], "session_id": res.get("session_id"),
                "input_tokens": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                + u.get("cache_read_input_tokens", 0),
                "output_tokens": u.get("output_tokens"), "raw": res.get("result"),
            })
            if err is None:
                break
        msg = AIMessage(content=content, tool_calls=calls,
                        response_metadata={"wall_s": dt, "parse_error": err, "model": self.model})
        return ChatResult(generations=[ChatGeneration(message=msg)])


if __name__ == "__main__":
    m = ClaudeCLIChatModel()
    print(" ".join(m.command()[1:]))
    print(m.invoke("Reply with the single word OK.").content, CALL_LOG[-1]["wall_s"])
