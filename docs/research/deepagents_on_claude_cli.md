# deepagents on the Claude Code CLI

Working notes from the build.

**VERDICT: WORKS_WITH_LIMITS** — deepagents 0.7.38 ran end to end on the Claude Code CLI 2.1.299 (headless, Sonnet, subscription login, no API key), 2 of 2 runs passed, 12–15 s per run. The limits: tool calling is emulated in the prompt, and the account identity, cwd and OS still reach the model.

Probe date 2026-11-14. Windows 11 ARM64, Python 3.11.9 (`.venv`), `claude` 2.1.299, deepagents 0.7.38, langchain 1.5.0, langchain-core 1.8.0, langgraph 1.2.22.

## 1. Exact command line

Per model call (fresh process, cwd = a dedicated empty folder `iso_cwd`, prompt on stdin):

```
claude.exe -p --model sonnet --output-format json
  --safe-mode --setting-sources "" --strict-mcp-config
  --disable-slash-commands --no-session-persistence
  --tools "" --system-prompt "<short fixed backend prompt>"
```

Child environment: every `*_API_KEY`, `ANTHROPIC_AUTH_TOKEN` and `CLAUDE*` variable is deleted before spawn (never read). Two `*_API_KEY` variables were present in the parent shell; they were stripped.

The adapter calls `...\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe` directly, not `claude.cmd`, to avoid cmd.exe quoting of the empty-string arguments.

Flags found in this version's `--help`:

| Purpose | Flag |
|---|---|
| Headless | `-p, --print` |
| Model | `--model sonnet` (resolved to `claude-sonnet-5-5`) |
| Output | `--output-format text\|json\|stream-json` (`stream-json` needs `--verbose`) |
| System prompt | `--system-prompt`, `--append-system-prompt` |
| Tools | `--tools ""` (none), `--tools "Read"`, `--allowedTools`, `--disallowedTools` |
| Settings | `--setting-sources`, `--settings` |
| MCP | `--strict-mcp-config`, `--mcp-config` |
| Customisations off | `--safe-mode` (CLAUDE.md, skills, plugins, hooks, MCP, custom agents) |
| Sandbox-ish | `--restricted` (no code-running tools, file tools confined to cwd, ignores settings files) |
| No resume | `--no-session-persistence` |
| Skills off | `--disable-slash-commands` |
| Other | `--effort`, `--json-schema`, `--max-budget-usd`, `--permission-prompts none` |

- **`--bare` cannot be used**: its help text says OAuth and keychain are never read, auth is strictly `ANTHROPIC_API_KEY`. That contradicts the no-key requirement.
- **There is no `--max-turns` flag** in this version's help. With `--tools ""` every call was 1 turn anyway.

## 2. Isolation findings

**Did not leak (checked specifically):**
- `~/.claude/CLAUDE.md` (user-level instructions): absent.
- Text from a user-level hook: absent. Model reported "Hook-injected text: none".
- MCP servers: init event shows `"mcp_servers":[]`.
- Tools: `"tools":[]`. Skills `[]`, slash commands `[]`.
- Memory and project names: none.
- Previous call: call 2 answered `UNKNOWN` for the codeword planted in call 1. Every call has a distinct `session_id`. No session folder for `iso_cwd` appeared under `~/.claude/projects`, and `iso_cwd` stayed empty.

**Did leak (the CLI adds these itself; no flag found that removes them):**
- The account identity, in an auto-attached context block. Account identity can appear in output; isolate it (never log or publish raw CLI output or model context).
- The absolute working directory path, platform, shell, OS version, today's date, model ID.
- A fixed prefix on the system prompt: "You are a Claude agent, built on Anthropic's Claude Agent SDK."
- The init event still lists built-in agents (`claude`, `Explore`, `general-purpose`, `Plan`, `web-fetch`) and three built-in plugins. With no tools the model cannot use them.

**Auth:** init event reports `"apiKeySource":"none"`, with the key variables removed from the child, so the calls ran on the logged-in subscription.

## 3. Existing adapters (PyPI lookup only; none installed or run — UNTESTED)

| Package | Version / last release | Licence | Note |
|---|---|---|---|
| `langchain-claude-cli` | 1.2.1, 2026-08-24, 14 releases | MIT | Built on `claude-agent-sdk`, has `bind_tools`. Rejected on source reading: it resumes CLI sessions (`options.resume`, `_sessions.py`, `_pool.py`), and has a code path that reads `ANTHROPIC_API_KEY` for Files API downloads. Both conflict with the isolation and no-key rules. |
| `langchain-claude-agent-sdk` | 0.2.0, 2026-05-23 | MIT | Not inspected. |
| `langchain-claude-code` | 0.1.0, 2025-12-02, 1 release | MIT | Looks unmaintained. |
| `claude-agent-sdk` | 0.2.182, 2026-11-13 | MIT | Official SDK, not a LangChain model. |
| `claude-code-sdk` | 0.0.25, 2025-09-29 | MIT | Superseded by `claude-agent-sdk`. |

Decision: own adapter, `cli_chat_model.py` (about 200 lines; now `harness/model/cli_chat_model.py`), because it gives direct control of the isolation flags.

## 4. deepagents runs

A probe script (not included in this repo): `create_deep_agent(model=ClaudeCLIChatModel(), tools=[lookup_record], system_prompt=..., subagents=[field-verifier])`. The subagent owns `measure_floors`.

| | Run 1 | Run 2 |
|---|---|---|
| Pass | yes | yes |
| Full run wall-clock | 12.21 s | 15.15 s |
| Model turns | 4 | 4 |
| Per-turn wall-clock (s) | 3.29, 3.32, 2.73, 2.81 | 2.90, 4.99, 4.01, 3.19 |
| Input tokens per turn | 4.4k–5.5k | 4.4k–5.5k |
| Parse failures | 0 | 0 |
| Verdict | CONTRADICTED (5 vs 6) | CONTRADICTED (5 vs 6) |

Proof from the trace, same shape both runs:
1. Main agent AI message with two tool calls: `lookup_record({"address": ...})` and `task({"subagent_type":"field-verifier", ...})`.
2. Tool message `lookup_record` returning `stories: 5`.
3. Inside the subgraph: `field-verifier` AI message calling `measure_floors`, tool message `6`, then its answer.
4. Tool message `task` back in the parent, then the final verdict.

The Python functions also log their own invocations (`python_tool_log`), and both fired in both runs.

Tool-calling reliability: 8 of 8 model turns parsed cleanly, including one turn with two parallel tool calls. That is a small sample.

**Caveat on the delegation criterion:** the probe design forces delegation, because the main agent does not have `measure_floors` and its prompt tells it to use the subagent. Whether the model delegates when it has a choice is UNTESTED. `write_todos` was not enabled (opt-in in 0.7) — UNTESTED.

## 5. Vision

Works. A Pillow-generated `vision_cwd/plan.png` (three rectangles, two labelled) was read and described correctly: "2 labelled rooms: ROOM 1 (red) and ROOM 2 (blue). The green rectangle has no text." 6.6 s wall-clock, 3 turns.

Flags that allowed exactly file reading and nothing more (in addition to the isolation flags above):

```
--tools "Read" --allowedTools "Read" --restricted --permission-prompts none
```

with cwd set to a folder holding only the image. Init event: `"tools":["Read"]`. A deliberate attempt in the same call to read `../cli_chat_model.py` was denied ("is outside ...\vision_cwd"), so `--restricted` confines Read to the cwd.

Not wired into the adapter: image blocks in LangChain messages are replaced with "[image omitted]". For vision, make the image step a Python tool that runs this separate CLI call.

## 6. Latency and usage

- One bare CLI call ("Reply OK"): 2.3–2.9 s wall-clock, of which about 0.9 s is the API. So roughly 1.5–2 s is process startup per call.
- 6 calls in parallel: all correct, 3.56 s total, 6 distinct sessions.
- No rate-limit or usage-limit errors seen across about 25 calls.

## 7. What would break at scale

- **Weekly quota.** Every agent turn resends the whole history plus about 4–5k tokens of deepagents prompt and tool schemas, with no cross-call prompt cache hits observed (each call shows cache creation, zero cache read). Long runs with file tools will burn quota quickly.
- **Emulated tool calls.** A tool result or user text that contains `<tool_calls>` would be mis-parsed. There is one retry on a parse error, then the raw text is returned as the final answer.
- **Not implemented:** streaming tokens, `tool_choice`, image inputs, native structured output. `response_format=` through deepagents is UNTESTED.
- **Long prompts.** The prompt goes through stdin, so there is no command-line length limit, but very long histories were not tested.
- **Async.** Only `_generate` exists; `ainvoke` falls back to a thread. UNTESTED under `langgraph dev`.
- **Version drift.** Flags come from 2.1.299; a CLI auto-update could change them.
- **Install.** On this ARM64 Python, `uv pip install deepagents==0.7.38` fails building `cryptography` 50.0.2 from source. `--only-binary cryptography` fixed it (resolved to 46.0.3).

## 8. Recommended use in the build

1. Copy `cli_chat_model.py` into the app and pass `ClaudeCLIChatModel(model="sonnet")` as `model=` to `create_deep_agent`, and as `SubAgent["model"]` where wanted.
2. Keep the isolation flags as they are. Keep a dedicated empty cwd.
3. Keep tool outputs short and prefer few, coarse tools; each turn costs about 3 s plus the full history.
4. Cap runs with `ModelCallLimitMiddleware` to protect the weekly quota, and record one good demo run early.
5. Do vision as a Python tool that shells out with the Read-only flag set from section 5.
6. Fallback if it proves too slow or brittle: keep the deepagents graph and swap only the model object. The agent code does not change. The no-key alternatives are `--json-schema` for CLI-validated tool-call JSON (UNTESTED) or `langchain-claude-cli` with sessions disabled (UNTESTED). A real `ChatAnthropic` needs an API key, which the team ruled out.
