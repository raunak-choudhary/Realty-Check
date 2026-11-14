"""One-shot calls to Claude Code CLI (headless Sonnet, isolated, no API key).

ask_text / ask_json: text in, text or parsed JSON out.  ask_images: same, with image files.
Each call is a fresh process with no memory of any other call.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .cli_chat_model import ISO_CWD, ISOLATION_FLAGS, child_env, find_cli

PLAIN_SYSTEM = "You are a careful analyst. Follow the user's output format exactly. No preamble."


def _run(cmd: list[str], prompt: str, cwd: Path, timeout_s: int) -> str:
    cwd.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                       cwd=str(cwd), env=child_env(), timeout=timeout_s)
    try:
        res = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude CLI exit {p.returncode}: {p.stdout[-300:]} {p.stderr[-300:]}")
    if res.get("is_error"):
        raise RuntimeError(f"claude CLI error: {str(res.get('result'))[:300]}")
    return res.get("result") or ""


def ask_text(prompt: str, system: str = PLAIN_SYSTEM, model: str = "sonnet", timeout_s: int = 180) -> str:
    cmd = [find_cli(), "-p", "--model", model, "--output-format", "json", *ISOLATION_FLAGS,
           "--tools", "", "--system-prompt", system]
    return _run(cmd, prompt, ISO_CWD, timeout_s)


def parse_json(text: str) -> Any:
    """Parse the first JSON object or array in text (tolerates code fences and prose around it)."""
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.S)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    for opener, closer in (("{", "}"), ("[", "]")):
        i, j = t.find(opener), t.rfind(closer)
        if 0 <= i < j:
            try:
                return json.loads(t[i:j + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError(f"no JSON in model reply: {text[:200]}")


def ask_json(prompt: str, system: str = PLAIN_SYSTEM, model: str = "sonnet", retries: int = 1) -> Any:
    err = ""
    for _ in range(retries + 1):
        text = ask_text(prompt + (f"\n\nYour last reply was not valid JSON ({err}). Reply with JSON only." if err else ""),
                        system, model)
        try:
            return parse_json(text)
        except ValueError as e:
            err = str(e)[:120]
    raise ValueError(err)


def ask_images(image_paths: list[str], question: str, model: str = "sonnet", timeout_s: int = 240) -> str:
    """Ask a question about image files. Images are copied to a fresh empty folder the model may Read."""
    work = Path(tempfile.mkdtemp(prefix="rc_vision_"))
    try:
        names = []
        for i, src in enumerate(image_paths):
            name = f"img{i + 1}{Path(src).suffix.lower() or '.jpg'}"
            shutil.copyfile(src, work / name)
            names.append(name)
        prompt = ("Read these image files in the current folder, then answer.\n"
                  + "\n".join(f"- {n}" for n in names) + f"\n\n{question}")
        cmd = [find_cli(), "-p", "--model", model, "--output-format", "json", *ISOLATION_FLAGS,
               "--tools", "Read", "--allowedTools", "Read", "--restricted",
               "--permission-prompts", "none", "--system-prompt", PLAIN_SYSTEM]
        return _run(cmd, prompt, work, timeout_s)
    finally:
        shutil.rmtree(work, ignore_errors=True)
