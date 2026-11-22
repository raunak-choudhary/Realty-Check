# Docs

Everything here supports the code in this repo. Nothing in this folder holds sponsor data. Examples use invented addresses and ids.

## How the product works

- [CONTRACT.md](CONTRACT.md) is the message contract between the extension and the checker.
- [DECISIONS.md](DECISIONS.md) records the design decisions and the reasons behind them.
- [env.example](env.example) lists the settings the checker reads. Copy it to a private folder and fill it in there.

## Research

Notes written before and during the build, in [research/](research/).

- [capabilities.md](research/capabilities.md) maps what each data source can and cannot answer.
- [matterport_api.md](research/matterport_api.md) and [matterport_sdk.md](research/matterport_sdk.md) cover the 3D scan API and the viewer SDK.
- [vexcel_api.md](research/vexcel_api.md) covers aerial imagery and elevation.
- [deepagents.md](research/deepagents.md) and [deepagents_on_claude_cli.md](research/deepagents_on_claude_cli.md) cover the agent harness.
- [webmcp.md](research/webmcp.md) and [extension_testing.md](research/extension_testing.md) cover the browser side.

## Ideation

The brainstorm that led to the listing checker, in [ideation/](ideation/). Most ideas here were explored and not built.

- [ideas_brief.md](ideation/ideas_brief.md) is the brief every memo answered.
- `perspective_*.md` are eight first-round memos, each from a different point of view.
- `round2_*.md` are five second-round memos by audience.
- `round3_world_data_*.md` list public open datasets for Houston and Los Angeles.
- [renter_opportunities.md](ideation/renter_opportunities.md) looks at where the checker could go next.

## Evaluation

What we measured on the working checker, in [evaluation/](evaluation/).

- [run_summary.md](evaluation/run_summary.md) gives totals across 127 check runs.
- [county_coverage.md](evaluation/county_coverage.md), [county_layer.md](evaluation/county_layer.md) and [county_fix_before_after.md](evaluation/county_fix_before_after.md) cover the county record layer.
- [claim_stability.md](evaluation/claim_stability.md) tests whether the same page gives the same claims twice.
- [scan_pairing.md](evaluation/scan_pairing.md) covers matching a listing to the right 3D scan.
- [live_check_findings.md](evaluation/live_check_findings.md) lists what live checks turned up.

## Pitch

- [pitch/](pitch/) holds the talk track, the seven-slide deck source and the interactive architecture diagram.

## Design

- [design/](design/) holds the three interface directions we compared and the redesign mockup. The renders are in [img/](img/) as `design-*.png` and `walkthrough-*.png`.
