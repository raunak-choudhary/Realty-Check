# Decisions

- 2026-11-14: harness model = Claude Code CLI headless Sonnet via own adapter (probe: 2/2 runs, 12–15 s). No API keys.
- 2026-11-14: UI = in-page edge tab + push-left drawer (Simplify pattern), not Chrome side panel (cannot be opened by automation).
- 2026-11-14: page reader is site-agnostic: regex + JSON-LD + one model call; no per-site selectors.
- 2026-11-14: single working tree, disjoint folder ownership, orchestrator commits.
