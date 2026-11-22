# WebMCP: what it is and whether we use it (researched 2026-11-13)

Working notes from the build.

Verdict: **GO_WITH_GAPS, as a slice.** Build one JS tool registry in the console. The Python agent reaches it over our own WebSocket, which is the path the demo depends on. The same registry is also registered with `document.modelContext` when that object exists. The WebMCP registration costs about 20 lines and gives us a "standards-native" talking point at no risk. Do not make the live demo depend on WebMCP, browse CLI or a Chrome flag.

All sources below are primary and were read this session (repos via `gh api`, docs via fetch). Nothing was installed or run.

---

## 1. WebMCP: what it is

- **What it is.** A proposed web API from the W3C Web Machine Learning Community Group. It lets a page register client-side JS functions as tools, each with a name, description, JSON Schema `inputSchema` and an `execute` callback. Agents can then call those tools instead of scraping the DOM. The explainer describes pages as "in-page MCP servers".
  - Explainer: https://github.com/webmachinelearning/webmcp (licensed under the W3C Software and Document License)
  - Spec: https://webmachinelearning.github.io/webmcp/
- **API name.** The current spec, the explainer and Google's own guide all use **`document.modelContext.registerTool()`**. Older material (and the Playwright 1.64 docs) says `navigator.modelContext`. **Feature-detect both.**
- **Declarative forms.** `<form toolname="..." tooldescription="..." toolautosubmit>` appears only in a separate "future exploration" explainer. It is not in the spec, so we ignore it.
- **In-page consumer API.** `document.modelContext.getTools()` and `executeTool(tool, args)` are meant for embedded agents and test harnesses. There is also a `toolchange` event, and a tool is unregistered by aborting its `AbortSignal`.
- **Chrome status.**
  - Chrome Status entry 5117755740913664 lists a dev trial (behind a flag) in M146 and an **origin trial in M149 through M156**. One blog says the trial was extended to M162; I did not verify that.
  - Chrome's overall status is still "Proposed", so it is **not shipped in stable by default**.
  - For local development, enable `chrome://flags/#enable-webmcp-testing`, or launch Chrome with `--enable-features=WebMCP,WebMCPTesting,DevToolsWebMCPSupport` (these are Stagehand's default flags).
  - A production origin needs an origin-trial token.
- **Other browsers.** Edge 150 has an origin trial. Brave's Leo will support it from 1.102 (January 2027). ChatGPT Desktop lists support. Firefox and Safari have only standards-position threads open.
- **Security model.**
  - The `tools` Permissions Policy defaults to `self`. A cross-origin iframe needs `allow="tools"`, and without the permission `registerTool` rejects with `NotAllowedError`.
  - Cross-frame discovery requires a mutual opt-in: `exposedTo` on the provider side and `getTools({fromOrigins})` on the caller side.
  - The browser mediates every call.
  - Annotations such as `readOnlyHint` and `untrustedContentHint` are hints only. The app must validate in `execute`.
  - Error messages from a handler are replaced by a generic "invocation failed" string. Return `{isError:true, content:[...]}` instead so the agent can self-correct.

Minimal registration:

```js
const mc = document.modelContext ?? navigator.modelContext;
if (mc) {
  const ac = new AbortController();
  await mc.registerTool({
    name: "fly_to",
    description: "Fly the map camera to a property by lat/lon.",
    inputSchema: { type: "object", properties: {
      lat: { type: "number" }, lon: { type: "number" }, zoom: { type: "number" } },
      required: ["lat", "lon"] },
    async execute({ lat, lon, zoom = 17 }) {
      await map.flyTo({ center: [lon, lat], zoom });
      return { content: [{ type: "text", text: `at ${lat},${lon}` }] };
    },
  }, { signal: ac.signal });
}
```

- **Polyfills and libraries.**
  - `@w3c/webmcp-polyfill` 0.1.0 (Apache-2.0).
  - MCP-B: `@mcp-b/global` 6.2.0 (MIT, from the WebMCP-org/npm-packages monorepo). Its `@mcp-b/webmcp-polyfill` is deprecated in favour of the W3C polyfill.
  - `webmcp-types` (MIT) provides TypeScript types.
  - GoogleChromeLabs/webmcp-tools (Apache-2.0) contains the Model Context Tool Inspector extension, evals and `webmcp-skills`.

## 2. "browse cli"

- **What it is.** The npm package **`browse`** (0.11.4, MIT), the Browserbase CLI, built from `browserbase/stagehand/packages/cli`.
  - Install with `npm install -g browse`. It needs **Node 22.18 or newer**.
  - Its CI runs a Chrome smoke test on Windows.
  - It runs a per-session daemon, so commands after the first reuse the open browser. That is the realistic basis for the often-quoted "1 to 2 seconds, not 30" claim. The claim itself is a tweet and was not measured.
- **Local mode is free.** `browse open http://localhost:5173 --local` needs no key. **The default is a cloud browser when `BROWSERBASE_API_KEY` is set, and a cloud browser cannot reach localhost.**
- **WebMCP support.**
  - The CLI has **no dedicated WebMCP command** (its commands are open, eval, snapshot, screenshot, click and so on).
  - Browserbase's own `add-webmcp` skill calls page tools with `browse eval '...document.modelContext.getTools()... executeTool(t, JSON.stringify(args))'`.
  - Its gotchas: eval accepts only single-line scripts, and arguments must be a **JSON string**.
  - The Stagehand SDK, Python and TypeScript, has first-class `page.tools()` and `tool.invoke()` with the flags above.
- **Similar tools.**
  - `@playwright/cli` (Apache-2.0) has `webmcp-list` and `webmcp-call`.
  - Vercel `agent-browser` (Apache-2.0) has WebMCP enabled by default for local Chrome.

## 3. How our Python deepagents agent could call the console's tools

| Option | How it works | Verdict |
|---|---|---|
| A. Our own WebSocket channel | The console opens `ws://localhost:8000/ui`. Python sends `{id, tool, args}`, the page runs `TOOLS[tool].execute(args)` and replies `{id, result}`. | **Use this.** About 50 lines in total. It works in any browser, including the one the user is already looking at, with no flags. Image returns are just base64 strings. Fully under our control. |
| B. Playwright for Python ≥1.64 `page.webmcp.call_tool(name, args)` | Launch a headed Chromium with `--enable-features=WebMCP`. | This is real (Playwright class WebMCP, since v1.64; Python 1.65.2 exists). But the browser must be launched by Playwright, the API is experimental, the flag is required, and Playwright's docs still say `navigator.modelContext` while the spec says `document`. **Fallback or flair only.** |
| C. `browse` CLI as a subprocess tool | `browse eval` with a one-line JS snippet per call. | Needs Node 22, a daemon and string escaping, and still needs the flag. It is the worst fit for a Python harness. **Skip.** |
| D. Stagehand Python `page.tools()` | Same as B, plus a Stagehand dependency. | Skip. |

**Blunt answer.** For our own page driven by our own Python agent, WebMCP is **not better** than a WebSocket. WebMCP exists so that *third-party* agents (Gemini in Chrome, extensions, ChatGPT Desktop) can find a page's tools. We own both ends.

The useful idea we can borrow is the **shape**: name, description, JSON Schema, execute. Keep one `TOOLS` registry in JS with WebMCP-shaped definitions, and add a `list_tools` WS message. Python can then auto-generate LangChain `StructuredTool`s from the schemas, with zero duplication. When `document.modelContext` exists, register the same objects with it too. That is the "WebMCP-ready" claim at almost no cost.

## 4. Ranked utility for our build

1. **`capture_view()` / `open_scan(model, sweep)` / `scan_rooms()`. This is real utility.** The Matterport SDK runs only in the browser, so a browser-side tool is the only way the agent can move through the scan and get pixels back.
   - `open_scan` loads the model and calls `Sweep.moveTo` (we must wait for the move to finish).
   - `capture_view` calls `Renderer.takeScreenShot` and returns base64 JPEG to Python, which then makes a vision-model call.
   - Effort: 2 to 3 hours including the WS round trip.
2. **`fly_to`, `add_pin(evidence)`, `set_aerial_year(y)`. Real utility as visible proof, partly flair.** These let the judges watch the agent's investigation happen on screen, synchronised with the event rail. Effort: about 1.5 hours once the map exists.
3. **Auto-generated LangChain tools from `list_tools`. Small win.** Effort: about 0.5 hours.
4. **WebMCP registration of the same registry. Flair or talking point.** Show it in the Model Context Tool Inspector or Gemini in Chrome only if the flag is on. Effort: about 0.5 hours.
5. **Voice control. Demo flair only.** It needs speech-to-text plus a low-latency loop, and our agent's tool calls go through a deep-agent planner that takes seconds. **Skip**, unless everything else is done.

**Risks.**
- The Chrome flag or origin-trial token may be missing on the demo laptop.
- The API is still changing (navigator versus document is a live example).
- `executeTool` strips error text.
- A Playwright-launched browser is a different profile from the one we present in.
- A WebSocket has none of these risks.

## 5. GoogleChrome/modern-web-guidance-src

- Licence Apache-2.0, about 5k stars, active as of 2026-11-14. It is the **source and eval repo**. The distributable is `GoogleChrome/modern-web-guidance` (Apache-2.0), which ships `skills/modern-web-guidance` and `skills/chrome-extensions` plus plugin manifests for Claude, Codex, Cursor and others.
- The npm CLI `modern-web-guidance` provides `search`, `retrieve <id>` and `legacy-scan .`.
- The repo is organised into:
  - `guides/` with 18 disciplines, **including `guides/webmcp/`** (`agentic-javascript-tools`, `agentic-forms`, `webmcp`), plus `user-experience`, `performance`, `ui-components` and `css`
  - `features/` (popover, anchor-positioning and others)
  - `.agents/skills/`, which contains maintainer skills and is not useful to us
- **What to use.**
  - Copy `skills/modern-web-guidance` from the *distribution* repo into `.claude/skills` as reference. That is allowed: it is Apache-2.0 and it is not our code.
  - Read `guides/webmcp/agentic-javascript-tools/guide.md` (it confirms `document.modelContext`, AbortController registration and `exposedTo`).
  - The View Transitions and popover/anchor guides are useful for console polish.
  - The performance guides (INP, `scheduler.yield`) are low priority for a 2-minute demo.

## Sources
- https://github.com/webmachinelearning/webmcp (README, implementation-status.md, declarative-api-explainer.md)
- https://chromestatus.com/feature/5117755740913664 (OT M149 to M156; dev trial M146)
- https://developer.chrome.com/docs/ai/webmcp, https://developer.chrome.com/blog/ai-webmcp-origin-trial (2026-06-09)
- https://github.com/browserbase/skills (skills/add-webmcp/SKILL.md, skills/browser/SKILL.md); npm `browse` 0.11.4 MIT
- https://github.com/browserbase/stagehand (packages/cli, packages/docs/v4/basics/webmcp.mdx, sdk-python/examples/webmcp.py)
- https://github.com/microsoft/playwright/blob/main/docs/src/api/class-webmcp.md; playwright-python `_impl/web_mcp.py`
- https://github.com/GoogleChrome/modern-web-guidance-src, https://github.com/GoogleChrome/modern-web-guidance
- npm: @w3c/webmcp-polyfill, @mcp-b/global, webmcp-types, @playwright/cli, agent-browser
