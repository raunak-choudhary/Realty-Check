# Testing the Chrome extension with Playwright

Working notes from the build. The probe script `test_ext.py` named below was a throwaway and is not included in this repo.

**VERDICT: WORKS_WITH_LIMITS.** The Playwright Python library loads and fully drives an unpacked MV3 extension in Playwright's **bundled Chromium**, both headed and headless. Installed Google Chrome cannot load it (`channel="chrome"`), the real Chrome side panel cannot be opened by automation, and Apartments.com and Zillow return bot walls to the automated browser.

Run on 2026-11-14, Windows 11. Playwright 1.65.2 (Python, project `.venv`, installed with `uv pip`). Bundled Chromium 159.0.8154.6. Installed Google Chrome 157.0.8103.51.

## Which runs were headed
- **Main run: headed** (visible window), bundled Chromium, `slow_mo=700`, with 2 s pauses after the glow appears, after the popover opens and after the verdict lands. It covered checks 1–5. Command: `python test_ext.py headed --real`
- Secondary: `python test_ext.py headless` (bundled Chromium, `channel="chromium"`, new headless) covered checks 1–4.
- Secondary: `python test_ext.py chrome` (installed branded Chrome) covered check 1, and checks 2–4 by cascade.

## Checks
| # | Check | headed (bundled Chromium) | headless (`channel="chromium"`) | `channel="chrome"` (Chrome 157) |
|---|---|---|---|---|
| 1 | Extension loads: service worker present, extension id read | PASS | PASS | **FAIL**: no service worker within 10 s. Branded Chrome ignores `--load-extension` |
| 2 | Content script on local fixture: 3 `.rc-glow` spans with the right text | PASS (3/3; the address in `<script>` is correctly skipped) | PASS | FAIL (0 spans) |
| 3 | Click glow → shadow-DOM popover → "Inspect Location" → service worker POST → verdict shown | PASS. Server log has the address; popover shows `Verdict: LOOKS_LEGIT (0.87)` | PASS | n/a |
| 4a | `chrome-extension://<id>/panel.html` opened as a normal tab; its JS runs | PASS | PASS | n/a |
| 4b | `chrome.sidePanel.open()` called from `service_worker.evaluate` | **FAIL**: `` `sidePanel.open()` may only be called in response to a user gesture. `` | FAIL (same error) | n/a |
| 5a | Apartments.com (`/princeton-nj/`), one load | **BLOCKED**: Akamai "Access Denied" (HTTP 200, title "Access Denied"). Content script ran and found 0 addresses. Not retried | - | - |
| 5b | Zillow (`/princeton-nj/rentals/`), one load | **BLOCKED**: "Press & Hold to confirm you are a human" modal over partly rendered results. The content script injected and counted 8 matches at idle, but 0 glow spans survived (the page re-rendered or the wall replaced them). Not retried, no evasion | - | - |
| 5c | Unprotected real page: princetonnj.gov home | PASS: page loaded, 1 address found and wrapped (in the footer, below the fold in the screenshot) | - | - |
| 6 | `@playwright/mcp` loading an extension | **UNTESTED** (read `--help` of v0.0.85 only, see below) | | |

The `[rc-content] injected, addresses found: N` console line is the in-page evidence.

## Exact launch that works
```python
ctx = p.chromium.launch_persistent_context(
    user_data_dir="<fresh throwaway dir>",
    headless=False,                 # or headless=True, channel="chromium" (new headless) - also works
    args=[f"--disable-extensions-except={EXT}", f"--load-extension={EXT}"],
    slow_mo=700,                    # watch mode only
)
sw = ctx.service_workers[0] if ctx.service_workers else ctx.wait_for_event("serviceworker")
ext_id = sw.url.split("/")[2]
```
- **Works:** Playwright bundled Chromium 159 (`playwright install chromium`), headed, and headless with `channel="chromium"`.
- **Fails:** `channel="chrome"` (Google Chrome 157 stable). The extension never loads, which is consistent with Chrome 137+ dropping `--load-extension` in branded builds. We did not try Edge or Chrome for Testing.
- A `launch_persistent_context` is required, and the fresh user-data-dir is deleted after each run.
- Locators: Playwright CSS pierces open shadow roots, so `page.locator("#rc-host").locator("#rc-inspect")` works directly. A closed shadow root would need a test hook.

## Check 6: Playwright MCP (UNTESTED)
`npx @playwright/mcp@0.0.85 --help` shows `--config <path>`, `--browser` (chrome, firefox, webkit, msedge), `--executable-path`, `--user-data-dir`, `--cdp-endpoint`, and `--extension`. The `--extension` flag means "connect to your running Chrome via the Playwright Extension"; it does not load your own extension. Possible ways to get there, none of them run:
1. A `--config` JSON with `browser.browserName: "chromium"`, `browser.userDataDir`, and `browser.launchOptions.args: ["--disable-extensions-except=…", "--load-extension=…"]`, with `launchOptions.channel` set to `"chromium"` or `--executable-path` pointing at the bundled Chromium. The default MCP browser is branded Chrome, which will **not** load the extension.
2. Simpler and more reliable: launch bundled Chromium ourselves with the extension and `--remote-debugging-port`, then start MCP with `--cdp-endpoint http://127.0.0.1:<port>`.

## What cannot be automated (needs a human)
- **Opening the real Chrome side panel.** `sidePanel.open()` requires a user gesture, and service-worker `evaluate` does not count as one. Automation can test `panel.html` as a tab (logic and rendering), but a human has to check the docked panel: size, layout, and that clicking the toolbar icon opens it.
- **Behavior on Zillow / Apartments.com.** Both return bot walls to automation. Check them by hand in a normal Chrome, or test against saved HTML.
- **Behavior in the user's real branded Chrome** (Chrome Web Store build, or "Load unpacked" in `chrome://extensions`). Automation only covers bundled Chromium.
- Visual quality of the glow and popover on real sites with heavy CSS. Screenshots help, but a person has to judge.

## Recommended test recipe for the real build
1. **Unit-test address detection (fast, no browser).** Save HTML from Zillow and Apartments.com pages by hand ("Save page as") into `fixtures/real/`. Keep the detector as a pure function `findAddresses(text)` and test it with vitest or node:test on the extracted text, asserting the expected addresses and no false positives (prices, phone numbers, "2 Beds · 1 Bath · 950 sq ft").
2. **Extension end-to-end on local fixtures (the `test_ext.py` pattern used here).** Use bundled Chromium with `launch_persistent_context` and the two flags, and serve the saved real-site HTML plus synthetic pages from a local server. Assert the glow count, click the popover, POST to a **mock backend** (assert the request body), and check the verdict render. Test `panel.html` as a tab. Run headless in CI and `headed` with `slow_mo` for demos. Also test dynamic content: inject addresses after load and assert a MutationObserver picks them up. The probe found that Zillow's re-rendering wipes the spans.
3. **Manual checklist (about 5 minutes, real Chrome, "Load unpacked")**: (a) the extension loads with no errors in `chrome://extensions`; (b) on a live Zillow listing and a live Apartments.com listing, addresses glow and the popover works; (c) the verdict appears and the backend shows the request; (d) clicking the toolbar icon opens the side panel and it renders correctly; (e) nothing breaks on pages with no addresses; (f) no console errors in the service worker's "Inspect views".
