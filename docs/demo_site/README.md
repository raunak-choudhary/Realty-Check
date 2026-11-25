# Demo listing pages

Pages to run the extension against. They are plain static files.

## `houston.html`, `la.html`: invented listings

Made-up buildings on a made-up listing site ("Northstar"), with `site.css` and `site.js`. Safe to show anywhere.
Serve and open:

```
cd docs/demo_site
python -m http.server 8899 --bind 127.0.0.1
```

- http://127.0.0.1:8899/houston.html
- http://127.0.0.1:8899/la.html

Then start the checker (`python -m server`, port 8787), load `extension/` unpacked in Chrome, and run the check from
the page. The checker needs the private sponsor data folder (`RC_PRIVATE_DIR`) to return real results.

Rules for these pages:

- Buildings, addresses, photos and text are invented. Do not add copies of real property websites or their photos.
- Never add images from CoStar, Matterport or Vexcel here: a listing page is the thing being checked, not a source.
