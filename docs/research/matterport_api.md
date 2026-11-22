# Matterport Model API: live test (2026-11-14 UTC, API access)

Working notes from the build; sponsor identifiers and record values removed.

Tested with the provided API keys against `POST https://api.matterport.com/api/models/graph` (basic auth: key = user, token = password).
About 100 API calls in total, throttled to 0.35 s or more between calls, queries only, no mutations.

Sample: the example model plus 26 commercial models (13 Houston, 13 LA; 14 with a `costar_property_id`; 10 picked on purpose for office, retail, warehouse or cafe names) plus 10 residential models. Raw responses were kept locally with signed URLs stripped.

## Headline

- **Introspection is open.** The full schema (266 types) can be pulled through introspection.
- The **wall graph has real door and window openings**: `floors.edges.openings { type width height lowerElevation relativeCenter }`, typed `doorway | window | opening | divider`, all in metres. So door widths come straight from the API.
- **"Property Insights" data covers residential fully, but only a minority of commercial models.** That data is room classifications, the wall graph, openings, `dimensionEstimates` and `ceiling`. In the sample it covered 11/11 residential models and 10/26 commercial.
- **MatterPak works, but not the way the quickstart says.** `assets.resources(format:"matterpak")` returns `status: unavailable` and no URL on every one of the 37 sampled models. `bundle(id:"mp:matterpak") { assets { ... on Resource { url } } }` returns a working URL on 37/37. The quickstart's section 8 code would wrongly report "locked".
- **The OBJ mesh is directly downloadable** through `assets.meshes { url }` at 500k and 50k faces, for 34/37 models, with textures through `assets.textures { urlTemplate }`.
- **There is no object detection.** `objectAnnotations` is 0/37, the `mp:object-detection` bundle is `unavailable`, and `objectClassifications` is `[]`. The only inference event is room classification.
- **Mattertags, notes, measurement paths and labels are empty** on 37/37 models.
- **Search** (`models(query:)`) is a full-text and field query engine. Free text, `name:`, `address.locality:`, `address.postalCode:`, `internalId:`, `rooms.tags:`, `rooms.count:>N`, `floors.count:`, `splats.count:>0`, wildcards and `AND`/`OR` all work. **Geo search does not:** `geolocation.lat:` returns 0 in every form.

## Working queries (copy-paste)

```graphql
# key check
{ rootFolder { name modelCountSummary(includeModelsInSubfolders: true)
  subfolders { results { id name modelCountSummary(includeModelsInSubfolders: true) } } } }
# -> <root folder>: more than ten thousand models = Commercial Spaces (<folder_id>, the large majority) + Residential Spaces (<folder_id>)

# look a model up by its CoStar property id (= internalId when numeric)
query { model(field: internalId, id: "<PropertyId>") { id name } }      # -> <model_id> "<model name>"
# ModelIdField enum: id | internalId | mlsId

# everything structural for one model (1 call)
query($id: ID!) { model(id: $id) {
  name internalId address { address locality postalCode status } geolocation { lat long }
  geocoordinates { latitude longitude altitude translation { x y z } rotation { x y z w } }
  generatedDescription { summary } propertyClassifications { classification type }
  dimensionEstimates(units: metric) { area areaIndoor areaIndoorWithWalls }
  floors { id label sequence vertices { id position { x y } }
    edges { id type thickness centerLineBias vertices { id }
            openings { type label width height lowerElevation relativeCenter } } }
  rooms { id tags keywords floor { id } classifications { label confidence }
    dimensionEstimates(units: metric) { area width depth height lowerElevation widthData { points { x y } } }
    dimensions(units: metric) { areaFloor areaWall width depth height volume }   # deprecated but better populated on commercial
    ceiling(units: metric) { minHeight maxHeight } boundary { edges { id } } }
  panoLocations { id label placement position { x y z } rotation { x y z w } options { format resolutions }
                  anchor { neighbors } }
  views { id type }   # includes matterport.model.defurnished when present
} }

# panoramas (6 signed face URLs, order 0=up, 1-4 horizon, 5=down)
query($id: ID!) { model(id: $id) { panoLocations { id label
  skybox(resolution: "2k") { validUntil urlTemplate children }   # also "4k", "high" (1024), "low" (256)
} } }

# MatterPak — USE THE BUNDLE, not assets.resources
query($id: ID!) { model(id: $id) {
  bundle(id: "mp:matterpak") { availability assets { ... on Resource { filename status url validUntil } } } } }

# mesh + textures + floor plans + 2D photos
query($id: ID!) { model(id: $id) { assets {
  meshes { format resolution status url validUntil }          # obj 500k / 50k
  textures { format resolution quality urlTemplate }          # replace <texture>
  floorplans { format flags width height resolution origin { x y } url validUntil floor { id } }
  photos { id type width height label url } } } }

# defurnished view: query the view id as if it were a model id (same pano ids & positions — verified 39/39)
query($id: ID!) { model(id: $id) { view(type: "matterport.model.defurnished") { id } } }

# search
query($q: String) { models(query: $q, pageSize: 100, offset: null) {
  totalResults nextOffset results { id name internalId score address { locality } rooms { count labels tags } } } }
```

## Field availability (sample: 26 commercial / 11 residential)

| Field | Commercial | Residential | Notes |
|---|---|---|---|
| address (street line) | 19/26 | 11/11 | 7 commercial have `status: empty`; some are not street addresses (a unit-name string like "<n> Br, <n> Ba - <n> SF") |
| geolocation / geocoordinates | 19/26 | 11/11 | geocoordinates has the ENU→model `rotation` + `translation`, and an altitude |
| generatedDescription.summary | 22/26 | 8/11 | matches the index `ai_summary` |
| propertyClassifications | 17/26 | 11/11 | values seen: `living_space` (12 commercial, 11 residential), `workspace` 3, `food_drink` 1, `factory_industrial` 1; all `type: vision` |
| rooms (any) | 26/26 | 11/11 | `label` is almost always null; use `classifications` / `tags` |
| room classifications | 10/26 models (97/178 rooms) | 11/11 (213/248 rooms) | 36-label vocabulary (residential-oriented, see below) |
| room `tags` (Cortex) | 131/178 rooms | 180/248 rooms | present even without Property Insights: `office`, `lobby`, `kitchen`, `garage`, `unfurnished`... |
| room `dimensions.areaFloor` (deprecated) | 26/26 models (139/178 rooms) | 11/11 | the only area source on non-PI commercial models |
| room `dimensions` width/depth/height | 106 / 97 / 88 of 178 rooms | 164 / 156 / 90 of 248 | |
| room `dimensionEstimates` width/height | 9/26 models | 11/11 | Property Insights only |
| room `ceiling` min/max | 8/26 | 11/11 | |
| wall graph (vertices/edges) | 10/26 | 11/11 | edge types: `wall` 605, `invisible` 8 (commercial) |
| openings (any) | 9/26 | 11/11 | |
| doorway / window | 8/26 / 2/26 | 11/11 / 9/11 | commercial openings are mostly unlabelled `opening`/`doorway` |
| floor plans: photogramy JPG/PNG, schematic PNG, DXF | 26/26 | 11/11 | 100 px/m; `origin` in metres |
| panoLocations | 26/26 (827 panos) | 11/11 (647) | `placement: auto` on all but 1, `source: vision` |
| 4k skybox | 22/26 (all panos) | 11/11 | 4 older commercial models only have `low, high, 2k` |
| defurnished view | 9/26 | 11/11 | |
| MatterPak via bundle URL | 26/26 | 11/11 | `availability: unlocked` everywhere |
| `assets.resources(format:"matterpak")` available | **0/26** | **0/11** | always `status: unavailable`, no URL |
| OBJ mesh URL (`assets.meshes`) | 23/26 | 11/11 | |
| 2D photos | 26/26 | 11/11 | e.g. 7680x4320 `photo2D` |
| mattertags / notes / measurementPaths / labels | 0 | 0 | |
| objectAnnotations | 0 | 0 | |
| `mp:imagery` bundle | locked | locked | 4k still works; "8k" is not offered |

Room classification labels seen: Commercial: Void 22, Bedroom 19, Bathroom 15, Closet 10, Kitchen 9, Other 9, Living Room 7, Dining 3, Hallway 3, Pantry 2, Laundry 1 (81 rooms had none). Residential: Void 37, Bedroom 35, Bathroom 35, Closet 27, Hallway 21, Living Room 15, Staircase 13, Kitchen 11, Dining 8, Garage 6, Other 4, Laundry 3, Office 2, Pantry, Bonus Room, Patio, Entrance (35 none).
Confidence quantiles (0/10/25/50/75/90/100%): commercial 0.12/0.72/0.89/1.0/1.0/1.0/1.0; residential 0.28/0.76/0.87/1.0/1.0/1.0/1.0.
The full vocabulary has 36 labels: Balcony, Basement, Bathroom, Bedroom, Bonus Room, Closet, Den, Dining Room, Driveway, Entrance, Exercise Room, Exterior, Facade, Family Room, Game Room, Garage, Garden, Great Room, Gym, Hallway, Kitchen, Laundry, Library, Living Room, Loft, Media Room, Office, Other, Pantry, Patio, Pool, Sauna, Staircase, Utility Room, Void, Workshop. It has no retail, restaurant, dining-area or storefront classes. A multi-floor office/retail building came back as 14 Void and 8 Other.

## Answers

### (a) Door, opening and counter measurements
- **Door and opening widths and heights: yes, from the API alone, where Property Insights exists.**
  - `Opening.width` and `height` are in metres, and `lowerElevation` gives the sill or threshold z.
  - `relativeCenter` (0..1) places the opening along its edge; the edge vertices give its 2D position, so you can locate the door in plan.
  - The example model has 22 doorways and 19 windows. A sample door-pivot is 0.78 m wide by 2.03 m high. A window is 2.69 m wide, 1.26 m high, with its sill at 0.82 m.
  - Doorway widths across the sample, in quantiles (0/10/25/50/75/90/100%): 0.16/0.57/0.71/0.81/0.94/1.38/4.43 m. The small values look like noise, and the wide ones are cased openings or garage doors.
  - Labels are `door-pivot`, `door-unknown`, `window-unknown`, `divider`, or none. There is no explicit swing direction, accessibility flag or hardware data.
  - Commercial coverage is only 9/26 models. One office/retail model has 19 unlabelled `opening`s, from 0.01 to 5.04 m wide.
  - Wall `thickness` is per edge (0.10 to 0.28 m).
  - Room `ceiling` min/max height and room `dimensionEstimates` width/depth/height are also available, with `widthData.points` giving the measured line.
- **Counter heights and fixture heights: no.** The API has no object or fixture geometry: `objectAnnotations` is empty, object detection is unavailable, and there are no mattertags or measurements. You need the OBJ mesh (`assets.meshes`, 500k faces), the MatterPak `cloud.xyz` point cloud, or vision on the panoramas plus depth from the mesh.
- On models without Property Insights (most commercial models in the sample), even door widths need the mesh, point cloud or panoramas.

### (b) Search
`models(query:)` is Elasticsearch-like over a flattened `ModelSearchResult`. Counts are `totalResults`.

| query | total | verdict |
|---|---|---|
| `*` or empty | all | all models |
| `kitchen` (free text) | about 10,000 | broad; matches names and room tags |
| `rooms.label: kitchen` | 0 | **wrong field name** |
| `rooms.labels:Kitchen` | 1 | `labels` = user room labels (almost always null) |
| `rooms.tags:kitchen` | about 9,000 | **use `rooms.tags`** (Cortex classifier tags) |
| `rooms.tags:office` / `rooms.tags:lobby` | about 700 / about 500 | works |
| `rooms.tags:kitchen AND address.locality:Houston` | about 4,000 | boolean works |
| `Houston` / `address.locality:Houston` | about 6,000 / about 6,000 | works |
| `address.locality:"Los Angeles"` | about 5,000 | phrase works |
| `address.postalCode:<zip>` | about 100 | works |
| `name:Warehouse` / `Warehouse` | about 40 / about 60 | works |
| `name:warehouse AND address.locality:Houston` | about 30 | works |
| `name:*afe*` | about 20 | wildcards work |
| `cafe OR restaurant OR bar` | about 60 | works; `restaurant` alone gives almost nothing |
| `retail` / `office` / `workspace` / `factory_industrial` / `food_drink` | about 100 / 900 / 700 / 200 / 300 | free text hits the hidden propertyClassification and summary text |
| `propertyClassifications:workspace` and `propertyClassifications.classification:food_drink` | 0 / 0 | not a searchable field path |
| `generatedDescription.summary:restaurant` | 0 | no |
| `publication.summary:office` | about 20 | works |
| `internalId:<PropertyId>` / `internalId:Loopnet*` | 1 / about 100 | works |
| `id:<model_id>` | 1 | works |
| `splats.count:>0` | about 200 | works (the index lists somewhat more splat models) |
| `rooms.count:>30` / `rooms.count:[1 TO 2]` / `floors.count:>2` | about 300 / about 4,000 / about 400 | numeric ranges work |
| `geolocation.lat:[<lat> TO <lat>]`, `geolocation.lat:><lat>`, exact lat | 0 | **no geo search**; use the model index CSV's lat/lon |
| `listingIds:*`, `cameraModels:*` | 0 | |

### (c) What commercial models look like
The "Commercial Spaces" folder is mostly multifamily apartment listings (Apartments.com and CoStar multifamily), not stores or restaurants.
- **Index-wide, by name heuristic over the commercial models:**
  - most are apartment units (`2BR, 2BA - <n>SF`, Studio, floor plans)
  - the next largest group is amenity or common spaces (fitness, pool, lobby, clubhouse, leasing office, courtyard)
  - office, suite, retail, warehouse or industrial spaces are a small share
  - the rest are other names (street addresses, misc.)
  - Names containing `retail`, `store` or `shop` are only a handful. `restaurant` matches almost nothing through search.
- **In our sample of 26** (deliberately biased towards business names):
  - 14 apartment units
  - 2 hotel suites
  - 3 amenity spaces (leasing office, courtyard, lobby/cafe)
  - 6 real commercial spaces (3 office suites, 1 office floor, 1 warehouse, 1 office/retail building)
  - 1 ambiguous: named as a unit, but its summary says commercial space
- **Ten concrete examples** were recorded (sid, name, address, propertyClassification, rooms, panos); the rows are removed here. Row shape:
  1. `<model_id>` "<model name>", <street address>. <propertyClassification>; <n> rooms, <n> panos. CoStar <PropertyId>.

### (d) Signed URLs, errors and rate limits
- **Signed URLs** are on Matterport's CDN with query `?t=2-<hash>-<unix_expiry>-<n>&k=<path>`, with no `Expires` parameter. Expiry is encoded in `t` and matches `validUntil`.
  - Skybox faces, floor plans, meshes and textures: `validUntil` is about **5 minutes** after the query (a query at 03:02:55Z gave 03:07:56Z).
  - MatterPak bundle URL: about **24 hours** (`validUntil` 2026-11-15T03:02:56Z).
  - **Tested:** a skybox face and a floor-plan URL returned 200 at t0. At t+400 s both returned **HTTP 410** `{"code":"content.gone","message":"Gone","retry":false}`. Re-query rather than cache.
- **Errors seen** (all HTTP 200 with partial `data`, except auth):
  - Unknown model: `{"message":"Error fetching data (path: /model, code: not.found): Not Found","extensions":{"code":"not.found","retry":"false","httpCode":404}}`
  - No defurnished view: the same `not.found` at path `/model/defurn`. If you alias the field, the rest of the query still returns.
  - 4k on older models: `request.invalid` "Unsupported resolution, use one of [2k, high, low]". On new models, asking for "8k" lists `[2k, 4k, low, high]`.
  - `image(format: equirectangular)`: `request.invalid` "Unsupported image format". Only skybox exists.
  - Schema mistake: `Validation error (FieldUndefined@[model/assets/resources/contentType])`. The whole query fails with no `data`, so use inline fragments for type-specific fields.
  - Bad key: HTTP **403** `{"code":"request.unauthorized","message":"invalid key/secret"}`. No auth: HTTP **401** `{"code":"request.unauthorized","message":"Unauthorized"}`.
- **Rate limits:** none hit in about 100 calls at no more than 3/s. There are no rate-limit headers (behind Cloudflare; only `X-Request-Id` and `CF-RAY`).

### (e) Panoramas for vision models
- **Format.** Each panorama is a skybox of 6 JPEG cube faces (RGB):
  - `children[0..5]` = up, then 4 horizon faces, then down. `urlTemplate` has a `<face>` placeholder.
  - Sizes: `4k` = 4096x4096 (1.2 MB per face), `2k` = 2048x2048 (456 KB), `high` = 1024, `low` = 256 (all verified by download).
  - No equirectangular or cylindrical versions are served.
- **Stitching.** `equirect()` in section 4 of the sponsor's Matterport quickstart script maps the faces to equirectangular, with y up and z forward:
  - face 1 is +z, face 2 is +x, face 3 is -z, face 4 is -x, face 0 is +y (up), face 5 is -y (down)
  - cross layout: up above face 1; horizon row 4, 1, 2, 3; down below face 1
- **Pose.** `position {x y z}` is in metres in the model frame (z up). Camera height is about 1.47 m above the floor. `rotation {x y z w}` is a quaternion; the example's is close to identity plus a yaw. `placement` is auto or unplaced, `source` is vision, and `anchor.neighbors` gives a navigation graph.
- **Same frame as everything else.** The wall graph, the floor-plan `origin` and `resolution` (100 px/m), the mesh and the point cloud share that frame. `geocoordinates.rotation` and `translation` map the model frame to East-North-Up and lat/lon.
- **Defurnished.** The defurnished panoramas (`view(type:"matterport.model.defurnished")`) use the same pano ids and positions (39/39 verified), so you can pair them with the originals.
- **Volume.** About 827 panos across 26 commercial models (up to 222 in one model). Pull at 2k unless you need fine detail.

## Gotchas

- Null fields are omitted, not returned as `null`. One invalid field name fails the whole response, but resolver errors (`not.found`, `request.invalid`) are partial.
- `rooms.label` is the user label and is nearly always null. `classifications[].label` is the model's label, and `tags` are the search-indexed classifier tags.
- Deprecated `rooms.dimensions` is populated more often on commercial than `dimensionEstimates`.
- `assets.resources(format:"matterpak")` is misleading (`unavailable`). Use `bundle(id:"mp:matterpak").assets`. The MatterPak zip for the example model is about 138 MB; a 1 KB range request returned 206 and `PK\x03\x04`.
- The `mp:obj` and `mp:obj-low-res` resources are also `unavailable`, but `assets.meshes` gives the OBJ directly (range GET returned `v <x> <y> <z> ...`).
- Some commercial models have no geolocation or address in the API; the index CSV's lat/lon fills some of these.

## What you can and cannot do

**Can:**
- address, lat/lon, ENU transform, AI summary and property type for most models
- room polygons, areas, ceiling heights, wall thickness, and door and window widths, heights and sill heights (all residential, a minority of commercial)
- 4k cube-face panoramas with poses, plus defurnished variants
- aligned floor-plan rasters and DXF
- the OBJ mesh and textures
- the MatterPak point cloud (all models sampled)
- 2D marketing photos
- full-text and field search, including by CoStar id (`internalId`) and room tags

**Cannot:**
- geo search
- object or fixture detection (counters, sinks, shelving, ramps): it is empty or unavailable
- mattertags, notes or measurements: empty
- a retail or restaurant room taxonomy: the classifier is residential (Void and Other for commercial)
- equirectangular panoramas from the API
- E57
- caching signed URLs beyond about 5 minutes (24 hours for MatterPak)
- the wall graph or openings on most commercial models
