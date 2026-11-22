# Vexcel API 2.0 — what it can and cannot do (live-tested 2026-11-13)

Working notes from the build; sponsor identifiers and record values removed.

Sources read: the sponsor's Vexcel API tutorial PDF (13 pages, all read) and its quickstart Python script
(445 lines, read in full, not executed). No other sponsor PDF was found.
About 60 API calls in total. No 429 seen. Sequential, at least 0.6 s apart.

## Basics
- Base `https://api.vexcelgroup.com/v2`. Auth header `X-API-KEY: <key>` (or `?api_key=<key>`, which was verified to work).
- Bad key → `401 {"status":401,"message":"Unauthorized"}`.
- Outside the key's geofence (Princeton NJ): `property/extract` → `403 "Unauthorized by Geofencing permission"`;
  `ortho/extract` and `oriented/collections` → `403 "Forbidden"`. The key covers Houston + Los Angeles areas.
- **WKT is lon-lat** (`POINT(<lon> <lat>)`). Always send `srid=4326`.
- Layers: `urban` (7.5 cm ortho + obliques), `urban-r` (7.5 cm ortho only), `wide-area` (15 cm ortho),
  `urban-g` (other 7.5 cm, e.g. a Leica 2018-19 capture in LA). `layer=urban,urban-r,wide-area,urban-g` = the API
  picks in that priority order. **It is NOT "newest":** at the LA example point, `urban-r` held a Jul-2026 capture
  while the default returned `urban` from Dec-2025.
- 429 → back off exponentially (1, 2, 4, 8, 16 s), as in the quickstart's `send()`.
- Imagery is © Vexcel Imaging US, Inc.; keep that credit on anything we show.

## Endpoints: documented vs verified

| Endpoint | Documented (PDF p13) | Live result |
|---|---|---|
| `GET /property/extract` | GeoJSON parcels + attributes; `wkt, srid, layer, latest, include, unit-system, buffer-meter`, `page/page-size` (≤500), filters `pool=true`, `roof-solar=true`, `roof-material=metal` | 200 at 4 of 5 test points (0.4–1.7 s). 404 `"No available property data for request"` at one LA test point (point not on a parcel); `buffer-meter=30` fixed it (12 features). `roof-solar=true` filter works. Area query (point + `buffer-meter=150`, `page-size=50`) returned 50 parcels. |
| `include=calculated` | roof height/elevation, slow | 200 in 1.1 s. Per structure: `roof-characteristics.elevation`, `roof-characteristics.height` (metric). Values are noisy (see Elevation below). |
| `POST /ortho/extract` (GET also) | JPEG/PNG/TIFF; `wkt, layer, buffer-meter`/`bbox-dimensions, crop, zoom, drawing, destination-dimensions, image-format` | 200 for all 4 layers, jpeg/png/tiff, `zoom=19`, `collection=` (history), `drawing` overlays. `zoom=22` → 404 "No image matching…". |
| `POST /oriented/extract` | obliques/nadir; `wkt, layer=urban, product-type=oblique-north/south/east/west (or nadir), crop=bbox, rotation=natural, downsample, drawing` (colors as bare `"r,g,b"` plus `fill-color` and `transparency:0`) | 200 for all 4 directions, `nadir`, an older `collection`, and point + `buffer-meter`. 1.3–1.8 s, about 1,900×1,400 px for a 120 m box. |
| `GET /oriented/collections` | coverage; `wkt, product-type, include` | 200. With `include=product-type,collection,last-capture-date` it lists every collection × direction with its date: 33 entries at the LA example (2019→2025-12), 28 at H2 (2020→2026-01). Without `include` it also returns `graysky-event` and coverage MultiPolygons (795 KB). |
| `GET /oriented/query` | image metadata; `wkt, product-type, include, order-by` | 200: 312 raw images at H2 (2016→2026, including `us-tx-harvey-hurricane-2017`). `include=product-type,collection,capture-date` works. `include=all` → 400 "Incorrect parameter: include". `order-by=capture-date` → 400. Full camera metadata (camera-pos x/y/z, omega/phi/kappa, focal length, raster size) comes back inside `elements/detect` `images[].metadata`. |
| `POST /elements/detect` | open-vocabulary SAM3 detection; `wkt, buffer-meter, images[], model-input{elements[{label,model:"sam3",detection-threshold}], include[bbox,confidence,pixel-mask,pixel-bbox]}` | 200 in 3.0 s on a 70 m lot (ortho + oblique-north). See the parking section. |
| `POST /embedding/extract` | ranked tiles; `wkt` or `collection`, exactly one of `search-text / search-location / search-url / search-image / search-vector`, `include, total-records, page-size` | 200 in 2.3–2.5 s over a 2 km square. `search-text` scores are about 0.20–0.21 (relative only). `search-location` returns the query tile at score 1.0, then look-alikes at ~0.97. |
| `GET /embedding/collections` | embedding coverage | 200: 3 collections at H2 (`us-tx-houston-2026`, `us-tx-houston_rf10-2025`, `n29w95-us-tx-houston-2025`). |
| `GET /ortho/collections` | **not documented** | 200: 16 ortho collections at H2, from 2016 (`quick-ortho`) to 2026 (`final-ortho`). This is the up-front ortho coverage/history check. |
| `GET /dsm/extract` | **not documented** | **200: float32 GeoTIFF of surface elevation in metres, EPSG:3857, 7.46 cm px, nodata −9999.** XMP gives collection/dates. `image-format=png` is ignored (still TIFF). |
| `GET /dtm/extract` | **not documented** | 200: float32 GeoTIFF bare-earth terrain, 14.9 cm px (wide-area collection). |
| `ortho/extract product-type=dsm` / `nir`; `GET /elevation/extract` | not documented | 500 "Internal error" / 400 "Incorrect parameter: ortho-status" / 500. No NIR found. |

## Working calls (copy-paste; key from env)
```python
import os, requests
API = "https://api.vexcelgroup.com/v2"; H = {"X-API-KEY": os.environ["VEXCEL_API_KEY"]}
L = "urban,urban-r,wide-area,urban-g"
pt = "POINT(<lon> <lat>)"   # lon lat!
# parcel + 80+ attributes, one feature PER COLLECTION (history) even with latest=true
requests.get(f"{API}/property/extract", headers=H, params={"wkt": pt, "srid": 4326, "layer": L,
    "latest": "true", "include": "precomputed", "unit-system": "imperial"})
# ortho at native res (omit destination-dimensions); add "collection": "us-tx-houston-2022" for history
requests.post(f"{API}/ortho/extract", headers=H, json={"wkt": poly, "srid": 4326, "layer": L,
    "crop": "bounding_box", "image-format": "jpeg"})
# oblique facade view
requests.post(f"{API}/oriented/extract", headers=H, json={"wkt": pt, "buffer-meter": 40, "srid": 4326,
    "layer": "urban", "product-type": "oblique-south", "rotation": "natural", "crop": "bbox", "image-format": "jpeg"})
# coverage / dates up front
requests.get(f"{API}/oriented/collections", headers=H, params={"wkt": pt, "srid": 4326, "layer": "urban",
    "product-type": "oblique", "include": "product-type,collection,last-capture-date"})
requests.get(f"{API}/ortho/collections", headers=H, params={"wkt": pt, "srid": 4326})
# heights: DSM (surface) minus DTM (ground)
requests.get(f"{API}/dsm/extract", headers=H, params={"wkt": poly, "srid": 4326})   # float32 GeoTIFF
requests.get(f"{API}/dtm/extract", headers=H, params={"wkt": poly, "srid": 4326})
# open-vocabulary detection
requests.post(f"{API}/elements/detect", headers=H, json={"wkt": poly, "srid": 4326, "buffer-meter": 0,
    "images": [{"endpoint": "ortho/extract", "request": {"layer": L, "srid": 4326, "wkt": poly, "crop": "bounding_box"}}],
    "model-input": {"elements": [{"label": "car", "model": "sam3", "detection-threshold": 0.5}],
                    "include": ["bbox", "confidence"]}})
# semantic search
requests.post(f"{API}/embedding/extract", headers=H, json={"wkt": big_poly, "srid": 4326,
    "search-text": "large surface parking lot", "include": "score,geometry,collection", "total-records": 10, "page-size": 10})
```
Reading the TIFFs: PIL 11 crashes on the XMP tag in `getexif`. Use `tifffile` instead (installed in .venv with numpy and imagecodecs).

## (a) Ortho
- **Native resolution** is web-mercator zoom 21 = 7.46 cm/px in projected units, which is about **6.2 cm ground at LA
  and 6.5 cm at Houston**. Measured: 70 m → 1133 px, 150 m → 2316 px. `wide-area` is zoom 20 (70 m → 567 px, about 12.4 cm).
  `zoom` lowers resolution (`zoom=19` → 194 px for 50 m). There is nothing finer than native (`zoom=22` → 404).
- **Area per request:** a 1 km square at native resolution worked (7719×7719 px, 19 MB, 3.6 s; about 900 tiles, just
  under the documented 1,024-tile cap). For larger areas, set `destination-dimensions` or `zoom`. 3 km at
  `destination-dimensions=1400,1400` worked in 1.2 s.
- **Metadata:** every image embeds XMP with `Vexcel:collection, layer, product-type (spherical-ortho|quick-ortho),
  first/last-capture-date, first/last-publish-date, min/max-gsd, camera-technology (e.g. UltraCam_Osprey_4.2_f180),
  pixel-bbox, min/max-zoom`.
- **Layers at the LA test point, 70 m:** `urban` → us-ca-losangeles-2025 (captured 2025-11-29..12-10).
  `urban-r` → us-ca-losangeles_rf07-2026 (2026-07). `wide-area` → n34w118-us-ca-losangeles-2026 (2026-04, 15 cm).
  `urban-g` → us-ca-losangeles_leica-2019 (2018-19, quick-ortho). All four had data.
- **History: yes.** Pass `"collection": "<name>"`. `us-tx-houston-2022` returned the Feb-2022 capture at H2.
  `GET /ortho/collections` lists 16 collections at H2 (2016–2026). `property/extract` also returns one feature per collection.

## (b) Obliques
Yes. `oriented/extract` with `layer=urban` and `product-type=oblique-{north,south,east,west}`, plus `rotation=natural`
and `crop=bbox`. It takes a lat/lon as `POINT` + `buffer-meter`, or a polygon. Check the available directions first
with `oriented/collections`. The 120 m oblique-north at the Houston test point (H2, a tall building with a low structure next to it) clearly shows the facade: windows,
balconies, an entrance canopy and entrance drive, the open sides of the low parking structure with cars visible
inside, and pools. The available history is much deeper (all 4 directions in 2020, 2021, 2022, 2023, 2025 and 2026
at H2). The direction a view looks in is in the product-type name ("oblique-north" looks north), so it shows the
south-facing facade. `downsample=2` shrank the output about 4× (to 485×362).

## (c) Elevation / height
- `GET /dsm/extract` (undocumented) gives a real per-pixel surface model: float metres, 7.46 cm px, georeferenced.
  `GET /dtm/extract` gives the ground. At H2, DSM minus DTM clearly separated the tall building's roof from the
  much lower top deck of the parking structure next to it, at plausible heights for both. Roof shape and rooftop equipment are visible in a DSM render.
- `property/extract include=calculated` returns `roof-characteristics.height/elevation` per structure. These were
  inconsistent across collections at H2 (from under 1 m to tens of metres for the "primary" structure), so the DSM is more reliable.
- The precomputed fields `roof-characteristics.maximum-roof-height`, `eave-height`, `number-of-stories-below-eave` and
  `volume-below-eave` were null at every test point. `structures[].ground-elevation.value` is filled.

## (d) Property attributes (exact keys, `include=precomputed`)
- Parcel level: `structure.count, parcel-source (Real|Bins|Unknown), parcel-tree-cover.percent, pool.detected/score/total-area,
  pool.types.{above-ground,in-ground,hot-tub}.{detected,score,count,area,distance,enclosed.*,non-enclosed.count},
  pool.objects.{water-slide,diving-board}.*, enclosure.*, sport-court.{detected,score}, hardscapes.area, hardscapes.percent,
  vehicles.{detected,score,count}, vehicles.types.automobile.{detected,score,count}, vehicles.types.boat.*,
  playground.*, deck.*, trampoline.*, census-tract, metadata.{camera-technology,gsd,image-id,ortho-date-estimate,version,
  layer-name,collection,is-ortho-image}, request-information.{requested-wkt,inside-parcel}`. The geometry is the
  parcel MultiPolygon (GeoJSON).
- `structures[]`: `footprint.wkt, footprint.area, primary-structure, building-type.class (single_family|multiple_family|
  commercial|shed|null), building-type.score, ground-elevation.value, structure-distance, defensible-space.zone1-4-{building,tree},
  roof-characteristics.{condition (1-5), condition.precise-value, tree-cover.percent, material.class (shingle|metal|membrane…),
  material.score, shape.value (gable|hip|flat), shape.score, centroid.wkt, …}, roof-objects.{solar.value, ac-unit.count,
  chimney.count, roof-vent.count, satellite-dish.count, skylight.count, solar-panel-photovoltaic.*, solar-panel-thermal.*},
  roof-defects.{missing-material,tarp,discoloration(+types algae-staining, vent-staining, water-pooling, …),debris,patch,
  structural-damage,rust}.{detected,percent,score}`.
- Example shape (illustrative, invented round numbers, not a real parcel): 4 structures, primary 100,000 sqft, membrane/flat,
  condition 3, 30 AC units, building-type commercial, vehicles.count 5, hardscapes 10 %.
- **Gotchas:** `latest=true` still returned 5–9 features, one per collection (H1 6, H2 6, L0 9). Footprints and labels
  vary a lot between collections: the same H2 primary footprint differed by up to about 80× in sqft depending on
  collection, and the 2025 run labelled it `single_family`. Pick the feature with the newest `metadata.collection`
  and sanity-check it. `unit-system=imperial` also converts `metadata.gsd` to feet. There are **no** parking-specific
  attributes: no stall count, paved-lot polygon or entrances. The closest are `hardscapes.area/percent` and
  `vehicles.count`.

## (e) Detection and embeddings
- `elements/detect` accepts any free-text label (SAM3) and returns one feature per detection:
  `properties.label` and `detections[{imageId, bbox (WKT, map coordinates), confidence[, pixel-mask b64 PNG, pixel-bbox]}]`,
  plus `images[].metadata` (capture date, gsd, camera pose).
  On the 70 m lot at H2: `car` 11 in the ortho (conf 0.68–0.94; every visible car boxed, one in deep shadow) and 46 in
  oblique-north (a wider footprint, including cars inside the garage). `handicap parking symbol` 4 in the ortho
  (0.56–0.75, correct, at the hatched ADA stalls). `tree` 17. **`parking space`, `dumpster`, `rooftop hvac unit` and
  `light pole` returned 0** at threshold 0.5 (lower the threshold or try other wording).
- `embedding/extract`: zoom-19 tiles (about 60 m; zoom 18 for wide-area). Text search for "large surface parking lot
  with painted stalls" ranked a striped, empty surface lot #1. `search-location` works for
  "more like this". No class list: it is free text.

## (f) Coverage
Princeton → 403 on property/ortho/oriented. To check up front, call `GET /oriented/collections` or
`/ortho/collections` (or `/embedding/collections`) with the point: 403 means outside the key, and 200 with features
means covered, with collections and dates. `property/extract` 404 only means no parcel at that exact point.

## Parking-lot experiment (Houston test point H2, 150 m native ortho, 2316 px / 150 m, Jan-2026)
Visible at native resolution (looked at directly, plus native-resolution crops of two corners of the lot):
- **Individual cars:** yes, clearly. Body colour and orientation are readable, and dark cars in shadow are still distinguishable.
- **Painted stall lines:** yes, crisp white lines and yellow curb paint. Stalls can be counted by eye on both the
  surface lot and the open top deck of the garage.
- **ADA:** yes. The blue wheelchair symbol and the diagonal-hatched access aisles are visible, and SAM3 found 4.
- **Pavement arrows and "STOP" text** on the garage deck, light poles (from their long shadows), landscaped tree islands
  and medians, curbs: all visible.
- **Curb cuts / driveway entrances:** visible as gaps in the curb and landscaping where drive aisles meet the street.
  The garage entrance ramp is visible. A pedestrian is even visible.
- **Drive-thru:** none on this site, so it could not be tested. Lane striping is resolvable, so one should be visible where it exists.
- **Limits:** January low sun puts much of the lot in heavy building shadow, though objects remain visible.
  Garage levels below the roof are invisible in the ortho, but the obliques show them partly. Trees hide some stalls.
- **No endpoint returns a stall count or a parking polygon directly.** Vehicles come from `property.vehicles.count`
  (per parcel) or `elements/detect "car"`. Stalls would have to come from line detection on the ortho by our own CV,
  or from the area divided by about 30 m² per stall.

## Smoke check
The ortho smoke check passed (1400×1400, 825,753 bytes, 1.1 s).
The only issue is cosmetic: it prints "~10.0 cm/px", but that is the *resampled* scale forced by
`"destination-dimensions": "1400,1400"`. Native is about 6.2 cm ground at LA. Dropping `"destination-dimensions"`
gives 2266 px at native resolution.
