# Matterport Showcase SDK test (verified in a real browser, 2026-11-13)

Working notes from the build; sponsor identifiers and record values removed.

## Run
    .venv/Scripts/python.exe serve.py      # a small local test server (not included here); serves http://localhost:8080
Open http://localhost:8080 (MUST be `localhost`; key domain is localhost only, not 127.0.0.1 / file://).
Server injects MATTERPORT_SDK_KEY from `.env` at request time (placeholders `__KEY__`, `__SID__`, `__BOOT__` in index.html), so the key is never stored in a repo file.
Options: `?sid=<model sid>`, `?boot=static` (static.matterport.com bootstrap). Results land in `<pre id="out">`, console, and `window.RESULTS`.
Tour + SDK connect take ~10 s; no play click was needed (`play=1`).

## Results
Connect succeeded on all three runs; `Model.getData().sid` echoed the sid back.
| Run | URL | sid echoed | sweeps |
|---|---|---|---|
| public, api.matterport.com bootstrap | http://localhost:8080/ | `<model_id>` | 39 |
| COMMERCIAL (`<model_id>`, an apartment unit) | /?sid=<model_id> | `<model_id>` | 32 |
| public, static.matterport.com bootstrap | /?boot=static | `<model_id>` | (connect ok, same results) |

Per-call (identical on public and commercial model):
| Call | Result |
|---|---|
| Model.getData | OK: keys `sid, sweeps, modelSupportsVr` only (no name) |
| Sweep.data (subscribe) | OK: id, position {x,y,z}, floorIndex |
| Floor.data | OK: 1 floor "Floor 1" |
| Room.data | OK: public 17 rooms, commercial 7; fields `bounds, floorInfo, id, label` |
| Camera.getPose | OK: position, rotation {x,y} degrees, projection matrix, sweep id, mode `mode.inside` |
| Mattertag.getData / Tag.data | OK, both empty (0) on these models |
| Sweep.moveTo (FLY) | OK, camera pose sweep id changed to target |
| Camera.rotate(60,0) | OK, yaw changed by -60 in pose |
| Renderer.getWorldPositionData({x:.5,y:.5}) | OK: world position + floorInfo + floor |
| Camera.takeScreenShot({width:640,height:360}) | OK: `data:image/jpg;base64,...` (~84-98 KB) |
| Renderer.takeEquirectangular(1024) | OK: `data:image/jpg;base64,...` |
| Camera.takeEquirectangular | FAIL: `sdk.Camera.takeEquirectangular is not a function` (my guess at the name; it lives on Renderer) |

Only console error was a favicon 404 from my server.
Not tested: wrong-host rejection, key refused for a model, non-embeddable model (nothing failed, so no failure causes to isolate).

## What the SDK adds beyond the Model API
Live camera control (pose, rotate, moveTo sweep with transitions), screenshots and equirectangular renders of the current view, raycast from screen point to world position (Renderer.getWorldPositionData), live sweep/floor/room collections, Mattertag/Tag read/write, scene objects (Scene namespace; not exercised here), and UI/pointer events.

## Gotchas
- Key allowed domain is `localhost`; serve from http://localhost:<port>.
- Each teammate has their own key in their own `.env`.
- Coordinate frames: SDK returned Y-up (camera height y~1.5, floor plane x/z). The Model/GraphQL API data is Z-up; convert before mixing. (SDK Y-up observed; Z-up API claim is from the task brief, not tested here.)
- Rotation in getPose is degrees; screenshots are base64 data URLs.
- Floor id appeared identical across the two models, so don't use it as a global key.
- Mattertag/Tag empty on tested models.
