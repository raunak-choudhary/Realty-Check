# deepagents: research notes for HackPrinceton (as of 2026-11-13)

Working notes from the build.

Legend: **[V-pkg]** verified against the installed package (deepagents 0.7.38 in a throwaway venv, including fake-model runs with no API key). **[V-doc]** verified on an official docs page, blog post or repo. **[I]** inference or opinion. **[unverified]** I could not confirm it.

---

## 1. What deepagents is today

| Fact | Value | Source |
|---|---|---|
| Python package | `deepagents` **0.7.38**, uploaded to PyPI **2026-11-13 14:32 UTC** (today) | [V-pkg] https://pypi.org/project/deepagents/ |
| Recent cadence | 0.5.0 on 2026-04-07; 0.6.0 on 2026-05-12; 0.7.0 on 2026-07-29; 0.7.20 on 2026-09-29; 0.7.30 on 2026-10-22. Releases come roughly weekly, so **pin the version** | [V-pkg] PyPI JSON |
| Status | "Development Status :: 4 - Beta" | [V-pkg] METADATA |
| Python | `>=3.11,<4.0` (3.11 through 3.14) | [V-pkg] |
| JS/TS | npm `deepagents` **1.16.5**, repo `langchain-ai/deepagentsjs` | [V-doc] registry.npmjs.org |
| Licence | MIT | [V-pkg] |
| PyPI summary | "Production-ready, extensible agent harness with a built-in filesystem and context management, sub-agent delegation, skills, and long-term memory." | [V-pkg] |
| Hard dependencies | `langchain>=1.5.0`, `langchain-core>=1.8.0`, `langchain-anthropic>=1.7.10`, `langchain-google-genai>=4.4.3`, `langsmith>=0.14.17`, `wcmatch`. The resolver pulled `langgraph` 1.2.22. Extras: `[aws]`, `[quickjs]`, `[video]` | [V-pkg] |
| Docs | https://docs.langchain.com/oss/python/deepagents/overview ; API reference https://reference.langchain.com/python/deepagents/ | [V-pkg] |

**Relationship.** LangChain's own wording is: "LangChain is an agent framework, LangGraph is an agent runtime, DeepAgents is an agent harness" (Harrison Chase, Oct 25 2025, https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my). The stack works like this:
- `create_deep_agent` builds on `langchain.agents.create_agent` and its middleware system.
- It returns a LangGraph `CompiledStateGraph` [V-pkg], so checkpointing, streaming, interrupts, the store and `langgraph dev` / Studio all work as they do for any LangGraph graph.
- LangSmith supplies tracing and evals. It also backs a `LangSmithSandbox` backend and a `ContextHubBackend` [V-pkg].

### Public API (0.7.38) [V-pkg]
- `deepagents` exports: `create_deep_agent`, `SubAgent`, `CompiledSubAgent`, `AsyncSubAgent`, `SubAgentMiddleware`, `AsyncSubAgentMiddleware`, `FilesystemMiddleware`, `FilesystemPermission`, `FsToolName`, `MemoryMiddleware`, `RubricMiddleware`, `DeepAgentState`, `HarnessProfile`, `HarnessProfileConfig`, `ProviderProfile`, `GeneralPurposeSubagentProfile`, `register_harness_profile`, `register_provider_profile`, plus the modules `backends`, `middleware`, `profiles` and `graph`.
- `deepagents.backends` exports: `StateBackend`, `FilesystemBackend`, `StoreBackend`, `CompositeBackend`, `LocalShellBackend`, `LangSmithSandbox`, `ContextHubBackend`, `BackendProtocol`, `NamespaceFactory`, `DEFAULT_EXECUTE_TIMEOUT`.
- `deepagents.middleware` adds: `SkillsMiddleware`, `SummarizationMiddleware`, `SummarizationToolMiddleware`, `create_summarization_tool_middleware`, `UnsupportedContentMiddleware`, and the rubric types `GraderVerdict`, `RubricEvaluation`, `RubricResult` and others.

Full signature [V-pkg]:
```python
create_deep_agent(model=None, tools=None, *, system_prompt=None, middleware=(), subagents=None,
    skills=None, memory=None, permissions=None, backend=None, interrupt_on=None,
    response_format=None, state_schema=None, context_schema=None, checkpointer=None,
    store=None, debug=False, name=None, cache=None) -> CompiledStateGraph
```

Built-in tools observed by binding a fake model [V-pkg]: `ls, read_file, write_file, edit_file, delete, glob, grep, task`. `execute` appears only when the backend is a sandbox (`LocalShellBackend`, `LangSmithSandbox` or another `BaseSandbox`).

> **BREAKING / commonly wrong in tutorials:** `write_todos` (the planning tool) is **no longer on by default**. It became opt-in in PR #4929, "feat(sdk,code,quickjs)!: make the `ToDoListMiddleware` list opt-in" (merged 2026-07-23), which shipped in the 0.7 line. Add it yourself with `from langchain.agents.middleware import TodoListMiddleware` and `middleware=[TodoListMiddleware()]`. [V-pkg + gh]

Default middleware order, from the docstring [V-pkg]:
1. FilesystemMiddleware
2. SubAgentMiddleware
3. SummarizationMiddleware
4. PatchToolCallsMiddleware
5. AsyncSubAgentMiddleware
6. *your middleware*
7. the profile's extra middleware
8. SkillsMiddleware
9. AnthropicPromptCachingMiddleware (always added; it no-ops for non-Anthropic models)
10. MemoryMiddleware
11. HumanInTheLoopMiddleware (only if `interrupt_on` is set)
12. UnsupportedContentMiddleware
13. ModelRefusalMiddleware
14. _ToolExclusionMiddleware

### Primitives, with tested sketches
Everything below was executed end to end with a fake chat model [V-pkg]: the interrupt fired, the resume approved and executed the tool, and the store persisted the file.

```python
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import TodoListMiddleware      # planning (opt-in)
from langgraph.checkpoint.memory import InMemorySaver            # checkpointing / resume
from langgraph.store.memory import InMemoryStore                 # long-term store
from langgraph.types import Command
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend, FilesystemBackend

def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""   # plain functions become tools; the docstring is the description
    ...

verifier = {                                   # SubAgent is a TypedDict
    "name": "verifier",
    "description": "Cross-checks a claim against a second data source; returns VERIFIED/CONTRADICTED/UNKNOWN with citations.",
    "system_prompt": "You are a skeptical verifier...",
    "tools": [query_source_b],                 # optional; model, middleware, interrupt_on, skills,
}                                              # permissions, response_format, mode are optional too

store = InMemoryStore()
agent = create_deep_agent(
    model=init_chat_model("anthropic:claude-sonnet-4-6"),     # or the string "anthropic:claude-sonnet-4-6"
    tools=[query_source_a, query_source_b, send_email],
    system_prompt="You are a real-estate due-diligence analyst...",
    middleware=[TodoListMiddleware()],
    subagents=[verifier],
    backend=CompositeBackend(default=StateBackend(),
            routes={"/memories/": StoreBackend(store=store, namespace=lambda rt: ("memories",))}),
    memory=["/memories/AGENTS.md"],            # AGENTS.md files loaded into the system prompt at startup
    skills=["/skills/"],                       # dirs of <name>/SKILL.md (YAML frontmatter name+description)
    interrupt_on={"send_email": {"allowed_decisions": ["approve", "edit", "reject"]}},
    checkpointer=InMemorySaver(),              # required for interrupts/resume
    store=store,
)
cfg = {"configurable": {"thread_id": "deal-123"}}
r = agent.invoke({"messages": [{"role": "user", "content": "Assess 12 Main St"}]}, config=cfg)
r["__interrupt__"]   # [Interrupt(value={'action_requests':[{name,args,description}], 'review_configs':[...]})]
r = agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config=cfg)
# other decisions: {"type":"edit","edited_action":{...}}, {"type":"reject","message":"..."}, {"type":"respond",...}
```

| Primitive | Exact names (verified) | Notes |
|---|---|---|
| Planning | `TodoListMiddleware` provides the `write_todos` tool | Opt-in since 0.7 [V-pkg] |
| Virtual filesystem | `FilesystemMiddleware`. Tools: `ls, read_file, write_file, edit_file, delete, glob, grep` (+`execute`) | Files are also returned in the result's `files` key [V-pkg] |
| Backends | `StateBackend()` (default; ephemeral, per thread), `FilesystemBackend(root_dir=..., virtual_mode=True, max_file_size_mb=10)` (real disk), `StoreBackend(namespace=callable, store=...)` (persists across threads), `CompositeBackend(default=..., routes={"/prefix/": backend})`, `LocalShellBackend(root_dir, timeout=120, env=..., inherit_env=False)` (real shell, **no sandboxing**), `LangSmithSandbox(sandbox)` | [V-pkg] |
| Permissions | `FilesystemPermission(operations=["read"/"write"], paths=[globs], mode="allow"/"deny"/"interrupt")`; first match wins; `interrupt` auto-installs HITL | [V-pkg] |
| Subagents | `SubAgent` dict, `CompiledSubAgent` (`name`, `description`, `runnable`), `AsyncSubAgent` (`name`, `description`, `graph_id`, `url?`, `headers?`, ...). All are called through the `task` tool (`description`, `subagent_type`). A `general-purpose` subagent is auto-added | Default `mode="isolated"` gives a fresh context, and only the final answer returns to the parent. `mode="fork"` (experimental) inherits the parent conversation [V-pkg] |
| Middleware | Subclass `langchain.agents.middleware.AgentMiddleware` (hooks: `before_agent`, `before_model`, `wrap_model_call`, `wrap_tool_call`, `after_model`, `after_agent`); pass `middleware=[...]` | Ready-made middleware in `langchain.agents.middleware` includes `ModelCallLimitMiddleware`, `ToolCallLimitMiddleware`, `ModelFallbackMiddleware`, `ToolRetryMiddleware`, `PIIMiddleware`, `ContextEditingMiddleware`, `LLMToolSelectorMiddleware` (module names verified; class names inferred from module names [I]) |
| Skills | `skills=["/skills/"]`, which wires up `SkillsMiddleware`. Each skill is `<dir>/<name>/SKILL.md` with frontmatter `name` and `description` | Progressive disclosure: only name and description go into the prompt until the skill is needed [V-pkg] |
| Memory files | `memory=["/memories/AGENTS.md"]`, which wires up `MemoryMiddleware`. The files load at startup into the system prompt | Route `/memories/` to `StoreBackend` so the agent can edit them and keep the edits across runs [V-pkg] |
| HITL | `interrupt_on={tool: True or InterruptOnConfig}`, which wires up langchain's `HumanInTheLoopMiddleware`. Decisions: `approve`, `edit`, `reject`, `respond`. Resume with `Command(resume={"decisions":[...]})` | Needs a checkpointer. Declarative subagents inherit `interrupt_on`; compiled and async subagents do not [V-pkg] |
| Code execution | `execute` tool, only with a sandbox backend. `LocalShellBackend` uses `subprocess.run(shell=True)` | On Windows this is **cmd.exe**, not bash [V-pkg] |
| Long-term memory | LangGraph `BaseStore` (`InMemoryStore`; Postgres store in production) + `StoreBackend` | [V-pkg] |
| Checkpoint / resume | `checkpointer=InMemorySaver()` (or `SqliteSaver` / `PostgresSaver` from langgraph-checkpoint-* packages [I]) + a `thread_id` | [V-pkg] |
| Streaming | Standard LangGraph: `agent.stream(input, cfg, stream_mode=["updates","messages"], subgraphs=True)` lets you see subagent internals | Standard LangGraph API [I: not exercised here] |
| Structured output | `response_format=PydanticModel` (or `ToolStrategy`/`ProviderStrategy`); result in `r["structured_response"]`. Subagents can also take `response_format` | [V-pkg signature] |
| Self-verification | **`RubricMiddleware(model=..., system_prompt=None, tools=None, max_iterations=3, on_evaluation=cb)`**. It activates when the invoke state includes `rubric`; a grader subagent scores the output and makes the agent iterate. Status is in `_rubric_status`, and a `rubric_evaluation_end` stream event fires | A built-in critic loop and a strong signal of depth for judges [V-pkg] |
| Profiles | `HarnessProfile(base_system_prompt, system_prompt_suffix, tool_description_overrides, excluded_tools, excluded_middleware, extra_middleware, general_purpose_subagent)`, applied with `register_harness_profile` | Built-in profiles exist for `claude-sonnet-4-6`, `claude-opus-4-7`, `claude-haiku-4-5`, openai codex and nvidia nemotron [V-pkg] |

## 2. Models
- **Selecting a model.** Pass a `provider:model` string, which is resolved through `init_chat_model`, or pass a `BaseChatModel` instance. Any LangChain chat model with tool calling works. The docs list Google (`google_genai:`), OpenAI (`openai:`, which uses the Responses API by default) and Anthropic (`anthropic:`), plus Baseten, Fireworks, OpenRouter and Ollama. https://docs.langchain.com/oss/python/deepagents/models [V-doc]
- **Default.** With `model=None` the default is `ChatAnthropic(model_name="claude-sonnet-4-6")`. This is **deprecated since 0.5.3** and will be removed in 1.0, so always pass a model. [V-pkg]
- **Claude support.** Claude is first-class. `langchain-anthropic` is a hard dependency, Anthropic prompt caching is always on, and there are Claude-specific harness profiles. Docs-recommended models are `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `gpt-5.5`, `gpt-5.4`, `gemini-3.1-pro-preview`, `gemini-4-hydrogen`, GLM-5.2, Kimi-K2.7 and MiniMax-M3. [V-doc]
- **Cost and latency [I].** Deep agents use many tokens: planning, file reads and subagent fan-out each mean extra model calls.
  - Use a cheaper model for subagents (`SubAgent["model"]`) and a strong one for the orchestrator.
  - Prompt caching helps on Anthropic.
  - Cap runs with `ModelCallLimitMiddleware` and `ToolCallLimitMiddleware`.
  - Expect a full run to take 1–5 minutes, so pre-record or cache a demo run.
  - The docs give no cost numbers.

## 3. "Harness" in LangChain vocabulary
Quotes [V-doc, fetched via a summariser; re-check the wording before quoting publicly]:
- "LangChain is an agent framework, LangGraph is an agent runtime, DeepAgents is an agent harness." A harness "comes with batteries included" and "adds in default prompts, opinionated handling for tool calls, tools for planning, has access to a filesystem, and more." (Chase, Oct 25 2025) https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my
- "Agent = Model + Harness." "If you're not the model, you're the harness." (Trivedy, Mar 10 2026) https://www.langchain.com/blog/the-anatomy-of-an-agent-harness. Its section headings: filesystems for durable storage and context, bash/code as a general tool, sandboxes to execute and verify work, memory and search, battling context rot, and long-horizon execution (planning, self-verification).
- "The harness is the system you build around the model to help your agent be successful in its domain... prompts, tools, skills..." and "The runtime is everything underneath: durable execution, memory, multi-tenancy, observability." (Apr 20 2026) https://www.langchain.com/blog/runtime-behind-production-deep-agents
- Original deep agents post (Jul 30 2025): plain loops are "shallow". Deep agents add "a planning tool, sub agents, access to a file system, and a detailed prompt", and the design was inspired by Claude Code. https://www.langchain.com/blog/deep-agents
- Harness engineering (Feb 17 2026) https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
  - Terminal Bench 2.0 went from 52.8 to 66.5 "only tweak[ing] the harness" with the model fixed.
  - Key lesson: agents don't naturally self-verify. They added a `PreCompletionChecklistMiddleware`, a `LoopDetectionMiddleware`, time-budget warnings and a "reasoning sandwich".
  - These are the blog's custom middlewares, not exports of the package.
- Evals (Dec 3 2025): "Deep agents require bespoke test logic for each datapoint." Test single steps (decisions), full turns (end state and artifacts) and multi-turn runs, with reproducible environments. https://www.langchain.com/blog/evaluating-deep-agents-our-learnings

**Harness vs one agent with tools [I].** A harness adds these on top of a tool-using agent:
- a reusable typed tool layer;
- explicit planning state;
- subagents whose context isolation is justified;
- a working-memory filesystem with offloading and an evidence ledger;
- a verification or critic loop before completion;
- approval gates on side effects;
- persistent memory across runs;
- resumability through a checkpointer;
- traces and an eval set with a measured before/after.

**What a LangChain judge will see as depth vs a thin wrapper [I].**
- **Thin:** `create_deep_agent(tools=[...])` with default prompts, a todo list nobody reads, subagents that are just renamed prompts, no traces, no evals.
- **Deep:**
  1. a domain verify loop the agent cannot skip (RubricMiddleware or custom pre-completion middleware);
  2. one or two custom middlewares motivated by failures seen in traces;
  3. a small eval table showing a number moving with the model held fixed;
  4. HITL on every external side effect;
  5. memory that changes behaviour on run 2;
  6. a LangSmith trace you can open live.

## 4. Hackathon track info
- **HackPrinceton Fall 2026 (Nov 13–15)** [V-doc, https://www.hackprinceton.com]
  - LangChain is a listed sponsor, alongside CoStar, Amazon, Salesforce, D. E. Shaw, Capital One, Scale AI and others. "$15K+ in prizes".
  - Tracks: Education, Entertainment, Sustainability, Healthcare, Business + Enterprise, Science + Discovery.
  - **No public wording or criteria for a LangChain/deepagents prize was found.** The Devpost (`hackprinceton-fall-2026.devpost.com`) returned 403, so it is unread, not empty.
- **LangChain x hackers&wizards, "Building with Agent Harnesses", Hamburg, Dec 4 2026.** Teams build deep agents using harnesses and demo them to expert judges, for $6,000 in LangSmith credits. No rubric published. [V-doc] https://hackathonhub.eu/events/langchain-x-hackers-wizards-hackathon-building-with-agent-harnesses-hamburg-hamburg-2026
- **Not readable:**
  - The "Deep Agents Hackathon" Devpost (https://deep-agents-hackathon.devpost.com/) returned 403. Its snippet reads "build agents, copilots, and autonomous systems that actually work end to end".
  - AI Tinkerers Dublin (grand prize: Interrupt tickets) also returned 403.
- **Not found:** a LangChain prize at TreeHacks 2026, LA Hacks 2026, HackMIT, Cal Hacks or PennApps, and any Devpost project that names deepagents as a prize winner.
- **[I]** Judging will likely reward a working end-to-end demo, visible planning, subagents and filesystem, LangSmith traces, and HITL.

## 5. Reasoning and action patterns
**Reasoning loop [I], built on verified primitives:**
1. **Plan.** `write_todos`, with steps like "pull parcel record", "pull comps" and "check permits".
2. **Gather.** Researcher subagents query one source each and write raw results to `/evidence/<source>/<id>.json`. This offloads context and leaves only a short summary in the conversation.
3. **Hypothesise.** The orchestrator writes `/work/hypotheses.md`, with each claim, a confidence level and the evidence IDs behind it.
4. **Verify.** A `verifier` subagent, with tools only for a *different* source, returns VERIFIED, CONTRADICTED or UNKNOWN per claim.
5. **Revise.** Edit the hypotheses. Contradictions trigger a re-plan.
6. **Decide.** Produce structured output (`response_format=Decision` with fields `claims[]`, `citations[]`, `confidence`, `open_questions[]`), with `RubricMiddleware` checking that every claim cites at least two sources and that uncertainty is stated.

The evidence ledger is a `/ledger.jsonl` file holding `claim | source | url/record id | retrieved_at | value | agrees_with`. Uncertainty handling: never resolve a conflict silently; surface it as `open_questions` and route it to the human through a `respond` interrupt.

**Action tools: 36 hours, Windows, Python** [V-doc via the research agent; gate column V-pkg]

| Action | Fastest implementation | Gotchas |
|---|---|---|
| Email | `resend` 2.53.2: `resend.Emails.send({...,"attachments":[...]})`. Free tier 3k/month, 100/day | Resend's shared onboarding sender delivers only to your own address unless you verify a domain [unverified]. Alternatives: Gmail API (`google-api-python-client` 2.202 + OAuth desktop flow, 30–45 min); SMTP app password |
| Calendar | Generate an `.ics` file (no OAuth) and email it, **or** Google Calendar `events().insert(...)` | Do Gmail and Calendar in one OAuth consent. `langchain-google-community[gmail,calendar]` 5.1.1 has `GmailToolkit` and `CalendarToolkit` |
| Phone / SMS | `twilio` 9.13.0: `calls.create(twiml="<Response><Say>..</Say></Response>")` | Trial accounts reach only verified numbers (at most 5), and trial SMS may be limited to templates, so voice is safer. Vapi/Retell/Bland for AI voice (Vapi free numbers can't dial out) |
| Slack / Discord | `requests.post(webhook_url, json={"text"/"content": ...})` | About 5 minutes each. Discord caps messages at 2,000 chars; use `?wait=true` |
| Ticket | `PyGithub` 2.10.0 `create_issue`, or Linear GraphQL `issueCreate` | Fine-grained PAT |
| Document | `fpdf2` 2.9.0 (pure Python) | Avoid WeasyPrint on Windows (GTK/Pango DLLs) |
| gws CLI | `googleworkspace/cli` v0.22.5 (`gws gmail +send`, `gws calendar +insert`) | Pre-1.0 and "not an official Google product" |

**Safety gates deepagents offers [V-pkg]:**
- `interrupt_on={"send_email": {"allowed_decisions": ["approve","edit","reject"]}}`, where "edit" lets a human fix the recipient or body;
- `FilesystemPermission(mode="interrupt")` for writes to `/outbox/**`;
- per-subagent `interrupt_on`.

Also [I]:
- a dry-run flag on every action tool;
- an allow-list of recipients;
- an idempotency key so a resumed run does not double-send;
- logging every executed action to `/actions.log`.

## 6. Observability, evals, UI
**LangSmith tracing [V-doc]** (https://docs.langchain.com/langsmith/trace-with-langchain)
- Required env vars: `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=...`. Optional: `LANGSMITH_PROJECT=hackprinceton`, plus `LANGSMITH_WORKSPACE_ID` if your key spans several workspaces.
- Short scripts can drop traces on exit. Call `langchain_core.tracers.langchain.wait_for_all_tracers()` or set `LANGCHAIN_CALLBACKS_BACKGROUND=false`.

**Free Developer plan [V-doc]** (https://www.langchain.com/pricing): 1 seat, 5,000 base traces a month, 14-day retention. Plus is $39 per seat a month. [I] A single deep-agent run is one trace, so 5k is plenty for a hackathon.

**Public trace link [V-doc]** (https://docs.langchain.com/langsmith/share-trace): open the trace, choose **Share**, and copy the link. Anyone can view it read-only. Put it in the Devpost write-up.

**Local server and Studio [V-doc]** (https://docs.langchain.com/langsmith/local-server)
- Install with `uv pip install "langgraph-cli[inmem]"`.
- Write a `langgraph.json`: `{"dependencies":["."],"graphs":{"agent":"./agent.py:agent"},"env":"./.env"}`.
- Run `langgraph dev`. The API is at http://127.0.0.1:2024, and Studio is at `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`. Studio has a graph view, threads, state time-travel, and interrupt resume.
- Under `langgraph dev`, **don't pass your own checkpointer**. The server supplies one [I: standard LangGraph platform behaviour].

**deep-agents-ui [V-doc]** (https://github.com/langchain-ai/deep-agents-ui) is **archived** (last push 2026-06-21), but it still works.
- To run it: `yarn install && yarn dev` (:3000), with `langgraph dev` running alongside. Enter the URL `http://127.0.0.1:2024` and the assistant ID from `langgraph.json`.
- What it shows: chat, threads, a todos and files sidebar, a file viewer, subagent indicators, tool-call boxes, and a **ToolApprovalInterrupt** approve/reject card. This is ideal for the demo.
- The todos panel stays empty unless you add `TodoListMiddleware`.
- The current official route is a custom React UI using `useStream` from `@langchain/react`, which exposes `todos`, `subagents` and interrupts: https://docs.langchain.com/oss/python/deepagents/frontend/overview

**Other official tools [V-doc]**
- The terminal coding agent is now `deepagents-code` (`dcode`).
- The `deepagents-cli` PyPI package (0.3.0) is deprecated and points to Managed Deep Agents (`mda`).

**Repo examples worth copying** (https://github.com/langchain-ai/deepagents/tree/main/examples): `deep_research` (has a `langgraph.json`), **`rubric_middleware`** (the verify loop), **`better-harness`**, `text-to-sql-agent`, `async-subagent-server`, `ralph_mode`, `llm-wiki`.

**2-minute demo plan [I]**
- Run in deep-agents-ui or Studio so the audience sees the todos tick, subagent cards, ledger files appearing and the approval card.
- Then open the shared LangSmith trace and expand the verifier subagent run.
- End on the eval table. Pre-record a backup video, because live runs take minutes.

**Evals [I + V-doc]**
- Build a LangSmith dataset and run `langsmith.evaluate(target, data=..., evaluators=[...])` [unverified exact signature in this langsmith version].
- Use per-datapoint assertions, as in LangChain's "Evaluating Deep Agents" post: trajectory checks (was the verifier called? was the interrupt hit before the action?) and end-state checks (the memo's numbers, its citation count).

## 7. Windows gotchas, known bugs, breaking changes
**Verified locally [V-pkg]:**
- The `LocalShellBackend` `execute` runs `subprocess.run(shell=True)`, which is **cmd.exe** on Windows. LLM-written bash (`ls`, `cat`, `&&` chains with POSIX tools) fails. Prefer custom Python tools over `execute`, or tell the model in the prompt that the shell is cmd/PowerShell.
- Skill and memory paths must be POSIX style (`/skills/`), relative to the backend root, even on Windows. Use `FilesystemBackend(root_dir=..., virtual_mode=True)`.
- `FilesystemBackend` grep shells out to ripgrep and falls back to Python if `rg` is missing (slower, but it works).

**Breaking changes [V-pkg / gh]:**
- todos became opt-in (PR #4929, 2026-07);
- `model=None` is deprecated (since 0.5.3);
- PR #7512 (merged 2026-11-05): "raise on model refusals by default and report subagent refusals to the parent". That means `ModelRefusalMiddleware` now raises.
- Third-party reports say v0.7 cut default harness tokens by about 65% [unverified].

**0.7.0 breaking changes (2026-07-29)** [V-doc] https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0
- **Todos are opt-in.** Subagents need `TodoListMiddleware` added separately.
- **The default base prompt is now empty.** `BASE_AGENT_PROMPT` is deprecated (removal in 0.9). `TASK_SYSTEM_PROMPT` and `FILESYSTEM_SYSTEM_PROMPT` were removed. **Write your own system prompt.**
- **`virtual_mode=True` is the default** for `FilesystemBackend` and `LocalShellBackend`. Paths are anchored at `root_dir`, and `..` is rejected.
- **New `delete` tool.** It is recursive. Write permission implies delete.
- **`write_file` overwrites** instead of erroring.
- **Backends must be instances, not factories.** `StoreBackend` requires `namespace`.
- **`read_file` output no longer has `cat -n` line numbers.**
- **`SummarizationMiddleware(history_path_prefix=...)` raises `TypeError`.**
- Most tutorials and blog posts from before 2026-07 are wrong on these points.

**Latest patches [V-doc]**
- 0.7.38 (today) ignores symlinks that escape the search scope in `ls`, `grep` and `glob`.
- 0.7.36 binds the backend to middleware and fixes a FIFO hang.
- The release cadence is roughly twice a week. **Pin `deepagents==0.7.38`.**

**Open bugs relevant to Windows [V-doc]**
- grep returns garbled text or a `UnicodeDecodeError` on non-ASCII content with ripgrep (#6964).
- `edit` converts CRLF to LF (#7488).
- `edit_file` rejects CRLF text (#5840).
- grep keeps the CR (#6827).
- Filenames containing `..` are rejected (#7167).
- **SKILL.md files with a UTF-8 BOM are silently skipped (#6811).** This is the classic Windows-editor trap.
- Closed: parallel first writes failed with `virtual_mode` (#6916), and the 260-character path limit was hit (#7146).

**Open bugs, general [V-doc]**
- stale `read_file` after a same-step write (#6983);
- `check_async_task` returns the last message rather than the structured response (#7274);
- double interrupts in async subagents (#7702);
- a pending Anthropic `web_search` call breaks the thread with 400s (#7489);
- nested routes in `CompositeBackend.ls` (#6568).

**Windows mitigations [I]**
- Set `PYTHONUTF8=1`.
- Save files as LF and UTF-8 without a BOM (`.gitattributes`: `* text=auto eol=lf`).
- Keep the repo path short.
- Avoid `execute`. Expose Python tools instead.
- Your own action tools are not affected by these bugs.

## 8. Recommended skeleton architecture for a real-estate harness [I]
```
harness/
  tools/            # typed tool layer: one module per source, each returns {data, source, record_id, url, retrieved_at}
    source_a.py     # e.g. property/parcel API         -> get_property(address)
    source_b.py     # e.g. comps/listings dataset      -> get_comps(lat,lng,radius)
    source_c.py     # e.g. permits/zoning/3D (Matterport/Vexcel) -> get_permits(parcel_id)
    actions.py      # send_email, create_calendar_ics, post_slack, file_ticket, make_pdf  (dry_run + allow-list)
  agents/
    orchestrator    # create_deep_agent(model=opus/sonnet, middleware=[TodoListMiddleware(), RubricMiddleware(...), BudgetMiddleware])
    researcher_a/b/c# SubAgent per source, cheap model, writes /evidence/<src>/*.json, returns 5-line summary
    verifier        # SubAgent w/ tools from a DIFFERENT source than the claim; returns VERIFIED/CONTRADICTED/UNKNOWN
    critic/writer   # SubAgent: drafts memo from ledger; response_format=Memo
  memory layout (CompositeBackend):
    /evidence/  /work/plan.md  /work/hypotheses.md  /ledger.jsonl   -> StateBackend (per thread)
    /memories/AGENTS.md  /memories/<market>.md                    -> StoreBackend (cross-run: learned source quirks, user prefs)
    /skills/<name>/SKILL.md                                        -> FilesystemBackend (repo, e.g. "comp-selection", "zoning-check")
    /outbox/                                                       -> FilesystemPermission(mode="interrupt")
  gates: interrupt_on for every tool in actions.py (approve/edit/reject); idempotency keys; actions.log
  runtime: SqliteSaver/InMemorySaver checkpointer + thread_id per deal -> resume after approval or crash
  ui: langgraph dev + LangSmith Studio / deep-agents-ui for todos, files, subagents, approve button
  evals/ (LangSmith dataset, 10-20 addresses):
    - single-step: "given this plan, does it call verifier before decide?"
    - end-state: memo cites >=2 sources per claim; numbers match ground truth within tolerance
    - safety: never calls send_email without interrupt; injected contradiction is surfaced, not hidden
    - report before/after table: plain agent vs harness, same model
  demo (2 min): ask -> todos appear -> subagents fan out -> ledger file fills -> verifier flags a contradiction ->
    revised memo -> approval card for email+calendar -> approve -> email lands -> open LangSmith trace + eval table
```
