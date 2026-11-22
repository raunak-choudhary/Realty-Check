# Data source capabilities

This is the team's working reference from the build, with sponsor record values and identifiers removed.

Purpose: what each data source can and cannot do, how the sources join, and what the data can and cannot answer. Idea exploration lives in `docs/ideation/`.

**Sources:** our own live tests of the Matterport Model API, the Matterport Showcase SDK and Vexcel API 2.0; the Vexcel API tutorial; the Matterport quickstart reference; and the CoStar kit documentation.

When our live tests disagree with sponsor docs, this document follows the tests. Section 7 lists practical gotchas.

---

## 1. One-screen summary

| Source | What it is | Size |
|---|---|---|
| **CoStar data kit** | 8 JSONL datasets plus 2 starter CSVs in an encrypted zip | Commercial properties in Houston and LA; commercial listings with their spaces; tenancies; tenant company locations; sale comps; apartment rent listings; MLS home listings plus feature records |
| **Matterport Model API** (GraphQL) | 3D scans: rooms, wall graph, door and window openings, panoramas (4k skybox), defurnished views, floor plans, OBJ mesh, MatterPak point cloud | More than ten thousand models, mostly "Commercial Spaces" with a smaller "Residential Spaces" share |
| **Matterport Showcase SDK** | In-browser 3D tour you can script: camera, sweeps, screenshots, raycast | Any model; the key works only on `localhost` |
| **Hackathon site** (Matterport) | Aerial Gaussian splats, sky cubemaps and DJI drone photos | A small share of models only, mostly residential |
| **Vexcel API 2.0** | Aerial imagery: ortho at about 6.2-6.5 cm ground, 4 oblique directions, history back to 2016, parcels with 80+ attributes, open-vocabulary SAM3 detection, text/image embedding search, DSM/DTM (undocumented) | Houston and LA areas only; elsewhere returns 403 |

**Geography.** Only the city of Houston and the city of Los Angeles, the two markets in the kit. There is nothing in Orange County, the Inland Empire or the suburbs outside city limits.

**The facts that drive every decision:**
1. **The library is mostly apartments.**
   - Most kit properties are Multifamily.
   - Most scans tied to kit properties are Multifamily.
   - By name, most "commercial" models are apartment units, followed by amenity or common spaces; office/suite/retail/warehouse/industrial spaces are a small share.
2. **Retail and restaurants are a handful.**
   - Properties: only a few dozen are GeneralRetail, and only a handful have the Restaurant subtype.
   - Search: names containing retail/store/shop are only a handful, and `restaurant` matches almost nothing.
   - The room classifier has no retail or restaurant classes. A mid-size office/retail building came back as only Void and Other rooms.
3. **Join on the model id, not on the index's id columns.** Use the model index `sid` = kit CSV `MatterportModelId`; this links almost every model.
   - Index `costar_property_id` is null on about half of commercial models and disagrees with the kit on some.
   - Index `homes_listing_id` is the Homes `ResidentialListingId`, not the MLS `ListingId` (none match the jsonl `id`).
4. **Use the kit's coordinates.** `primaryAddress.latitude/longitude` is filled on every kit property. Index model lat/lon is usually off by tens of metres, sometimes by more than a kilometre.
5. **Detailed scan geometry exists on all residential models but only a minority of commercial ones.** This "Property Insights" data is room classifications, the wall graph, openings, `dimensionEstimates` and `ceiling`. In our sample every residential model had it and fewer than half of the commercial ones did.
6. **No source detects objects inside a scan, and none has traffic data.**
   - Matterport `objectAnnotations` was empty on every sampled model and Mattertags are empty.
   - The kit has no traffic counts or demographics.
   - Vexcel has no parking stall count and no parking polygon.
7. **Signed links expire, so re-query instead of caching.**
   - Matterport skybox, floor plan and mesh links last about 5 minutes and return HTTP 410 after that.
   - MatterPak links last about 24 hours.
   - Hackathon-site links last 1 hour.
8. **Sponsor data and keys must never go into the public repo.** The demo has to run from a local, git-ignored cache.

---

## 2. Per-source capability tables

### 2.1 CoStar kit

Coverage is described qualitatively; record counts and statistics computed from the kit are omitted. "Verified" here means profiled directly from the kit's jsonl by our scripts.

| Capability | What you get (fields / units) | Coverage | Verified? | Gotcha |
|---|---|---|---|---|
| Property basics | `propertyType`, `propertySubtype`, `buildingClass` (A/B/C), `buildingRating` (1-5), `grossBuildingAreaSquareFeet`, `numStoriesAboveGrade`, `constructionEvents[]` (eventType 2 = year built), `lotSize`, `zoningDescription` | GBA and stories almost always; year built on nearly all; zoning on most (includes "None"/"N/Ap") | yes | Split by `propertyType` before totaling anything; most properties are MF. `buildingHeightInFeet` has some implausible outliers, so sanity-check it |
| Location | `primaryAddress.{latitude,longitude,postcode,researchMarketId,submarketIds}` | lat/lon on every property | yes | No single-string address. **Submarket names are absent** (ids only) |
| Parking | `parking[].parkingType`, `parking[].totalSpaces`, `parkingRatio` (per 1,000 SF), `monthlyParkingFee`; apartments `residentialProfile.parkingPolicies[]` | parkingType on most; totalSpaces and ratio on many; fee rarely meaningful (mostly 0); MF policies on most | yes | A property-level total, not per space or per tenant |
| Retail frontage | `propertyRetail.frontage[].frontageInFeet`, `.numCurbCuts`, `.streetName`, `.isPrimaryFrontage`, `.footprint.shape` (a LineString) | Retail properties only: frontage on most, curb cuts on fewer than half | yes | **This is the only traffic-related field. There are no traffic counts.** |
| Retail GLA | `propertyRetail.grossLeasableAreaSquareFeet` | All retail properties | yes | — |
| Apartments | `propertyApartment.models[]` (floor plans: `numBeds`, `numBaths`, `minSquareFeet`, `maxSquareFeet`, `numUnits`, `units[]`); `vacancyPercent`; `apartmentStyleType`, `apartmentLifestyleType`, `apartmentRentType`; `residentialProfile.schools[]`, `petPolicies[]` | Vacancy, schools and pets on most MF properties | yes (docs give the counts) | Matterport keys sit on `models[].attachments[]` and `models[].units[].attachments[]`, **so a scan can be tied to one floor plan**. `vacancyPercent` has values over 100 |
| Apartment rents | apartment-listing: `minRent`, `maxRent`, `numUnitsAvailable`, `totalNumUnits`; `apartmentModels[]` (plans with `name`, `numBeds`, `numBaths`, `minRent`, `maxRent`); `propertyManagementCompanyName` | Communities in both markets; nearly all plans join to property floor plans | yes | `minRent` 0 means no rent. Rents are monthly. Some rents are placeholder values |
| Lease availabilities | `forLeaseSummary.spaces[]`: `suite`, `floorName`, `squareFeetMin/Max`, `spaceUse`, `spaceType`, `rateLow/High`, `rateBasis`, `serviceType`, `availableOnDate`, `dateOnMarket` | Mostly Office spaces, then Retail, OfficeMedical, Industrial, Flex, OfficeRetail and Medical; rent on about half | yes | HOU quotes $/SF/yr and LA $/SF/mo, so normalize. A rate of 0 means none given. Many spaces have been on the market a long time |
| Brokers and contacts | `brokerageCompanyName` (almost always), `listingContacts[].firstName/lastName`, `propertyContacts[]` (TrueOwner, PropertyManager, ...) | On the properties that have listings | yes | Names are real; **emails and phones are placeholders** (example domain, 555 area code), so they cannot be used for outreach. The property record's `contacts[]` has no names |
| Matterport tours on listings | listing `attachments[]` with ext ref 36 | A small number of listings (titled like "Suite <n> Virtual Tour"), plus a few on `spaces[].floorPlan` | yes | Mostly office suites |
| Tenants | location-occupancy `spaces[].squareFeetOccupied`, `fromDate`, `toDate`, `leaseType`, `spaces[].spacePosition` (Inline/EndCap/Corner/FoodCourt); joined to company-detail for `name`, `profile.industryType`, `numEmployees`, `officeType`, `businessStatus` | Current tenancies on most properties; name via join, employees and industry on most | yes | Occupancy `industryType` is almost always Unknown. MF "tenants" are mostly on-site management. **No NAICS** (a 28-value enum) |
| Lease terms | `leaseDeal.{signDate,commencementDate,expirationDate,askingRate,rateActual,effectiveRate,leaseTerm}` | expiration on only a small minority of current tenancies; contract rent rarely filled | yes | Too sparse for rent-roll or lease-rollover analysis |
| Sale comps | `soldForPrice`, `salePriceStatus`, `soldDate`, `pricePerUnit`, `capitalizationRateActual`, `saleConditions[]`, `entities[].propertyId/percentLeased/allocatedPrice`, `contacts[]` | Comps on many kit properties; price on about half; cap rate on a minority | yes | Texas is non-disclosure: most Houston comps have no price. No price/SF field (compute it). Buyer/seller names on a minority |
| Hotels | `propertyHospitality.numUnits`, `averageDailyPricePerRoom`, `hotelClass`, `hotelBrandName` | A small set, almost all in Houston | yes | Occupancy and RevPAR are empty |
| Industrial specs | `ceilingHeightFeet`, drive-in bays, docks, power (within type) | Ceiling height and drive-in bays on most; docks and power less often | yes | — |
| Homes | residential-listings: `currentPrice`, `originalPrice`, `closePrice`, `rentMin/Max`, `property.bedsMin/bathsMin/sqftMin`, `yearBuilt`, `dom`, `agents[]`, `remarks`, `displayPrice.latestAVM`; features: `highlights[].text`, `sections[]` | Listings in both markets, mostly Texas | yes | **No Houston sold prices.** Drop the MLS placeholder prices. `address.city` is normalized; the real place is in `cityMetadata` / `areas[]` |
| Photos | `attachmentUri` (image link) | Dozens per property is typical | yes | — |
| **Absent** | Commercial vacancy/occupancy rate; market and submarket stats and names; **demographics; traffic counts**; walk/transit score; commercial tax/assessment; **NAICS**; tenant revenue; amenity names (ids only); owner names on the property record; RevPAR | — | yes | — |

### 2.2 Matterport Model API

Sample: a few dozen commercial and residential models, about 100 calls.

| Capability | What you get | Coverage (sample) | Verified? | Gotcha |
|---|---|---|---|---|
| Address / location | `address`, `geolocation`, `geocoordinates` (ENU rotation/translation, altitude) | Most commercial, all residential | yes | Some commercial models have no API address or location. Use kit coordinates |
| AI summary / type | `generatedDescription.summary`; `propertyClassifications` (`living_space`, `workspace`, `food_drink`, `factory_industrial`) | Summary on most models (also most of the index) | yes | Classification is not a searchable field path |
| Rooms | `rooms { classifications{label confidence} tags dimensions(areaFloor width depth height) dimensionEstimates ceiling }` | Classified: a minority of commercial models, all residential. `dimensions.areaFloor` on every commercial model (most rooms) | yes | 36-label residential vocabulary; commercial rooms come back as Void/Other. `rooms.label` is almost always null; use `classifications` and `tags` |
| Wall graph | `floors { vertices edges { type thickness } }`, in metres | A minority of commercial, all residential | yes | Wall thickness roughly 0.1-0.3 m |
| **Door and window openings** | `edges.openings { type width height lowerElevation relativeCenter }`, in metres; type is doorway, window, opening or divider | Openings and doorways on a minority of commercial and all residential; windows on few commercial and most residential | yes | Typical doorway widths are roughly 0.7-0.9 m; very small values are noise. No swing, accessibility flag or hardware |
| Ceiling heights | `rooms.ceiling { minHeight maxHeight }` | A minority of commercial, all residential | yes | — |
| Panoramas | `panoLocations { position rotation skybox(resolution: "4k" or "2k") anchor{neighbors} }`; 6 cube faces (0 up, 1-4 horizon, 5 down) | All sampled models (hundreds of panos); 4k on most | yes | Skybox only, no equirectangular (stitch it yourself). URLs last about 5 min |
| **Defurnished views** | `view(type:"matterport.model.defurnished") { id }`; query that id as a model. It has the same pano ids and positions (on every one checked) | A minority of commercial and all residential in the sample. Index: a large share of models | yes | `not.found` when absent; alias the field so the rest of the query survives |
| Floor plans | `assets.floorplans` (JPG/PNG/DXF, 100 px/m, `origin` in metres) | All sampled models | yes | Same frame as the wall graph and panos |
| Mesh | `assets.meshes` (OBJ, 500k and 50k faces), `assets.textures` | Nearly all sampled models | yes | — |
| MatterPak (point cloud) | `bundle(id:"mp:matterpak") { assets { ... on Resource { url } } }` gives `cloud.xyz` | Every sampled model had a URL | yes | `assets.resources(format:"matterpak")` reported `unavailable` on every sampled model. Use the bundle |
| 2D photos | `assets.photos` (e.g. 7680x4320) | All sampled models | yes | — |
| Search | `models(query:)`: free text, `name:`, `address.locality:`, `address.postalCode:`, `internalId:`, `rooms.tags:`, `rooms.count:>N`, `splats.count:>0`, wildcards, AND/OR | All models | yes | `rooms.tags:kitchen` gives thousands of hits; `rooms.label:` gives 0. **No geo search** (`geolocation.lat:` returns 0); use the model index |
| Lookup by CoStar id | `model(field: internalId, id: "<PropertyId>")` | Only when `internalId` is numeric | yes | About half of commercial models have no numeric CoStar id; join through the kit CSV |
| Rate limits | None hit at 3/s or less | — | yes | Errors arrive as HTTP 200 with partial `data`. One invalid field name fails the whole response |
| **Absent** | Object or fixture detection (`objectAnnotations` empty on every sampled model, `mp:object-detection` unavailable); Mattertags, notes, measurements and labels (empty); retail/restaurant room taxonomy; equirectangular panos; E57; `mp:imagery` bundle (locked) | — | yes | Counters, fixtures and stall-like geometry would need our own vision on panos, mesh or point cloud |

### 2.3 Matterport Showcase SDK

Verified in a real browser on 2026-11-13 with two sample models.

| Capability | What you get | Verified? | Gotcha |
|---|---|---|---|
| Connect / embed | `Model.getData` returns `sid`, `sweeps`, `modelSupportsVr` (no name) | yes (3 runs; connect takes about 10 s) | **The key's domain is `localhost` only** (not 127.0.0.1 or file://). Each teammate uses their own key |
| Navigation | `Sweep.data`, `Sweep.moveTo` (FLY), `Camera.rotate`, `Camera.getPose` (rotation in degrees) | yes | SDK is Y-up; the API is Z-up, so convert |
| Rooms / floors | `Room.data` (bounds, floorInfo, label), `Floor.data` | yes (17 and 7 rooms) | The floor id was identical across two models, so it is not a global key |
| Capture | `Camera.takeScreenShot` (base64 JPEG, 84-98 KB at 640x360), `Renderer.takeEquirectangular(1024)` | yes | `Camera.takeEquirectangular` does not exist; it is on `Renderer` |
| Raycast | `Renderer.getWorldPositionData({x,y})` | yes | — |
| Tags | `Mattertag.getData` / `Tag.data` (read and write) | read yes (empty); write not tested | Lets an agent write its annotations into the tour |
| Scene objects, pointer events | `Scene` namespace | no | — |
| Not tested | Wrong-host rejection, a model refused by the key, a non-embeddable model | — | — |

### 2.4 Hackathon site: splats and drone photos

| Capability | What you get | Coverage | Verified? | Gotcha |
|---|---|---|---|---|
| Catalog | A per-model JSON record (segment, `splatBytes`, drone photo names) | Only the splat models | yes | Every other model returns non-200 |
| Drone photos | Each photo link redirects to a signed link (1 h). DJI XMP in the first 48 KB has `GpsLatitude`, `GimbalYawDegree`, `GimbalPitchDegree` and `RelativeAltitude` | Splat models only; an example model has hundreds of high-resolution photos (tens of MB each) | yes (downloaded one) | The flight path costs one 48 KB range request per photo |
| Gaussian splat | `splat/splat.ply` (INRIA layout, 68 B per Gaussian, SH degree 0 only) and `splat/envmap/{px,nx,py,ny,pz,nz}.jpg` | Mostly residential. Commercial splats are few, almost all Multifamily, on a handful of properties | from docs (sponsor reference only) | Tens to hundreds of MB per model. Local frame, Z up, **not north-aligned**; georeference from drone GPS. Gaussians are unordered, so the first N MB is a fair sample |
| MatterPak on splat models | Point cloud plus OBJ; the example is over 100 MB with a point cloud of millions of points | — | yes (bundle route) | — |
| **Absent** | Splats or drone imagery for the vast majority of models; commercial retail or office exteriors almost never | — | — | — |

### 2.5 Vexcel API 2.0

About 60 live calls.

| Capability | What you get | Coverage | Verified? | Gotcha |
|---|---|---|---|---|
| Ortho | `POST /ortho/extract` (JPEG/PNG/TIFF). Native zoom 21 = 7.46 cm projected (about **6.2 cm ground in LA, 6.5 cm in Houston**); `wide-area` about 12.4 cm. XMP has collection, capture dates and camera | Up to 1 km square at native resolution (7719 px, 19 MB, 3.6 s; 1,024-tile cap) | yes | WKT is **lon lat**; always send `srid=4326`. The layer list is a priority order, not "newest" (LA: `urban` gave Dec 2025 while `urban-r` held Jul 2026) |
| History | `"collection": "<name>"`; `GET /ortho/collections` (undocumented) | 16 ortho collections at a Houston test point (2016-2026). Obliques in all 4 directions in 2020, 2021, 2022, 2023, 2025 and 2026; 312 raw oriented images at that point, including a named event collection | yes | — |
| Obliques | `POST /oriented/extract` with `product-type=oblique-{north,south,east,west}` or `nadir`, `rotation=natural`, `crop=bbox` | All 4 directions plus nadir; about 1,900x1,400 px for a 120 m box; 1.3-1.8 s | yes | "oblique-north" looks north, so it shows south facades. Check `oriented/collections` first. Drawing colors are bare `"r,g,b"` |
| Parcel attributes | `GET /property/extract` with `include=precomputed`. Parcel: `pool.*`, `vehicles.count`, `hardscapes.area/percent`, `parcel-tree-cover.percent`, `sport-court`, `census-tract`. Per structure: `footprint.area`, `building-type.class`, `roof-characteristics.{condition (1-5), material.class, shape.value}`, `roof-objects.{ac-unit.count, solar.*, skylight.count}`, `roof-defects.{tarp, missing-material, discoloration, rust, ...}.{detected, percent}` | 200 at 4 of 5 test points; 404 when not on a parcel (`buffer-meter=30` fixed it); area query plus `page-size` up to 500 | yes | **`latest=true` still returns one feature per collection (5-9).** Footprints vary by collection (by orders of magnitude for the same building). Pick the newest `metadata.collection` and sanity-check it |
| Roof height (calculated) | `include=calculated` gives `roof-characteristics.height/elevation` | 200 in 1.1 s | yes | Varies widely (from under 1 m to tens of metres for one building). Precomputed `maximum-roof-height`, `eave-height` and stories were null everywhere |
| **DSM / DTM** | `GET /dsm/extract` (float32 GeoTIFF, 7.46 cm, EPSG:3857) and `GET /dtm/extract` (bare earth, 14.9 cm). Both undocumented | Worked at a Houston test point: a tall building and a low structure next to it were clearly separated | yes | Read with `tifffile`; PIL crashes on the XMP tag |
| Detection | `POST /elements/detect`, free-text labels with SAM3; returns bbox (WKT), confidence, pixel mask; runs on ortho and/or oblique | On a 70 m lot: `car` 11 (ortho, conf 0.68-0.94) and 46 (oblique); `handicap parking symbol` 4; `tree` 17 | yes | **`parking space`, `dumpster`, `rooftop hvac unit` and `light pole` returned 0** at 0.5. About 3 s per call. Large areas are silently downsampled |
| Embedding search | `POST /embedding/extract` with `search-text` or `search-location` | About 60 m tiles (zoom 19); 2 km square in 2.3-2.5 s; 3 Houston embedding collections at a Houston test point | yes (text, location) | Scores are relative only (about 0.20-0.21 for text). `search-image`, `search-url` and `search-vector` were not tested |
| Visual parking read | Cars, painted stalls, ADA symbols and aisles, curb cuts and driveway entrances, garage ramp: all visible at native resolution (checked by eye) | — | yes (manual) | No stall count, paved-lot polygon or entrances from any endpoint. Stalls need our own line detection or area ÷ about 30 m² |
| Coverage check | `GET /oriented/collections`, `/ortho/collections` or `/embedding/collections` at the point: 403 = outside the key | Houston and LA | yes | Points outside the two cities return 403 |
| **Absent** | Parking stall count or polygon; entrances; traffic; NIR (`product-type=nir` errors); `/elevation/extract` (500); precomputed eave/roof heights (null) | — | yes | Attribution: keep "Imagery © Vexcel Imaging US, Inc." on anything shown |

**Described in the Vexcel tutorial but not tested by us:**
- `search-url`, `search-image` and `search-vector` embedding queries.
- The default 6 km x 6 km embedding search (we tested 2 km).
- The `collect-year` parameter for change detection.
- The `include=pool,roof-characteristics,footprint-wkt` field subset.
- `request-information.inside-parcel` as a check.
- Detection on oblique-south, oblique-east and oblique-west.

---

## 3. Cross-source joins

```
model index sid ──= MatterportModelId── properties CSV ──PropertyId── properties file id
        │                                  listings CSV ──ListingId── listings file id
        │                                                                                    │
  Matterport API model(id: sid)                                     primaryAddress.latitude/longitude (every property)
  Showcase SDK ?m=sid                                                 │
  hackathon site (splat models only)                                  ▼
                                                     Vexcel POINT(lon lat) → property/extract parcel (+buffer-meter=30 if 404)
                                                                     → ortho/oblique/detect/DSM on the parcel polygon
kit-internal: listing.propertyId, occupancy.propertyId → company-detail via tenantLocationId,
              sale-comp entities[].propertyId, apartment-listing.propertyId and apartmentModels[].id ↔ propertyApartment.models[].id
```

| Link | Coverage | Reliability |
|---|---|---|
| `sid` ↔ kit CSV `MatterportModelId` | Almost every index model links; every commercial and residential CSV id is in the index | **Primary key; trust it** |
| CSV ↔ jsonl `videoKey` (ext ref 36/234) | Commercial and residential media both carry keys; some residential media items have a null `videoKey` (parse `m=` from `uri`) | Exclude ext ref 60 (CoStar documents) |
| Index `costar_property_id` | Null on about half of commercial models; disagrees with the kit on some | **Do not use** |
| Index `homes_listing_id` | It is the `ResidentialListingId`: most match the CSV; none match the jsonl `id` | Go sid → CSV → `ListingId` |
| Models per kit property | Most properties have several scans; few have none or one; a handful have more than 20 | Most properties have several unit/amenity scans, not one building scan |
| Floor plan ↔ scan | Keys on `propertyApartment.models[].attachments[]` and `.units[].attachments[]`; nearly all apartment-listing plans join to property plans | Count of plans with a key **not measured** |
| Coordinates | Kit lat/lon on every property. Index model vs kit: usually tens of metres apart, with a tail of large errors (some over 1 km). Residential models are closer. Some commercial models have no API geolocation | Use kit coordinates for Vexcel |
| Kit point → Vexcel parcel | `property/extract` 200 at 4 of 5 points; a 404 means the point is not on a parcel | Several features come back, one per collection; choose the newest |

**Worked chain** (every step except the last is verified):
1. Index `sid` `<model_id>` (an apartment unit scan named by beds, baths and SF).
2. In the properties CSV: `MatterportModelId` `<model_id>` → `PropertyId` `<PropertyId>`.
3. In the properties file, `id` `<PropertyId>`: Multifamily, LA, `primaryAddress` `<lat>`, `<lon>`. It has several models, the same set in the index and the CSV.
4. Kit joins on that id: apartment-listing `propertyId`, sale-comp `entities[].propertyId` and location-occupancy `propertyId` (whether this property has rows in each was not checked).
5. Matterport: `model(id:"<model_id>")` gives rooms, openings and panos.
6. Vexcel: `POINT(<lon> <lat>)`. A neighbouring LA test point about 50 m away returned all four layers (urban Dec 2025, urban-r Jul 2026, wide-area Apr 2026, urban-g 2018-19). `property/extract` at this exact point was **not tested**.

A residential example on the same block joins the same way through the CSV `ListingId` / `ResidentialListingId`. It has a splat with drone photos and a MatterPak.

---

## 4. Data density by property type

Notes:
- Listings are counted by host property type; tenancies are counted by host type.
- Matterport field coverage by type was **not** measured. The sample suggests Property Insights is complete on residential and on fully classified apartment units, and missing on several office/warehouse models (one had no wall graph).

| Type | Props | Scanned props / models | Listings | Tenancies | Sale comps | Rents | Defurnished props | Splat props | What Vexcel adds | Demo-ready? |
|---|---|---|---|---|---|---|---|---|---|---|
| **Multifamily** | The large majority, in both markets | Nearly all scanned; most of the scans | Some (mostly ground-floor commercial space; mostly direct lease) | Many (mostly on-site management) | Most comps (`pricePerUnit` on about half) | **Per floor plan** on rent-listed communities; `vacancyPercent` on most | Many | A handful | Pools, roof condition and defects, parking cars, tree cover, DSM height vs `numStoriesAboveGrade`, history | **Yes, the richest by far** |
| **Office** | A small share, more in Houston | Most scanned | Most listings and most spaces; some listings carry suite tours | Most tenancies (large rosters per building) | Some | Asking rent per space (normalize HOU $/SF/yr and LA $/SF/mo) | Some | Almost none | Facade obliques, garage/lot cars, roof, DSM height | **Yes, for leasing and tenant demos** (scans are suites, lobbies and floors) |
| Industrial | A small share, mostly Houston | Most scanned | Some | Some | Some | Some space rents | Some | Almost none | Truck courts, trailers/cars, roof area, yard hardscape | Thin; possible as a niche |
| **Retail** (GeneralRetail) | A few dozen; only a handful with the Restaurant subtype | Most scanned, few scans each (often suites, pools or building exteriors rather than the shop floor) | Some | A few per property | Few | Asking rent on some retail-use spaces | Some | None | Parking lot cars, ADA symbols, curb cuts (by eye), facades | **No, as a property type.** Retail is richer as **tenants**: many scanned properties of other types have a current food or retail-use tenant |
| Hotel | A small set, almost all Houston | All scanned | Few | — | Some (`pricePerRoom` on about half) | ADR on almost all; no occupancy or RevPAR | Few | None | Pools, garage decks, facade, height | Narrow (Houston only) |
| Flex | Few | Most scanned | Some | Some | — | — | Few | None | As industrial | No |
| Land / Specialty / Healthcare | A handful each | Few | Few | — | — | — | Few | None | — | No |
| **Residential homes** | MLS listings in both markets, mostly Texas | CSV model ids on nearly all homes | — (MLS) | — | LA `closePrice` only; no Houston sold prices | Some rentals | Most residential models | **Most splats** | Pool, roof, trees, defensible space, solar: the tutorial's residential attributes | **Yes, for Matterport-heavy demos** (full Property Insights, splats, defurnished). The CoStar side is MLS data, not commercial |

**Plainly:**
- Multifamily is rich in all three sources. Rents per floor plan, vacancy, comps, unit scans with geometry, and parcel/roof/pool data from the air.
- Office is good for leasing and tenant work: spaces, rents, brokers, tenant rosters, some suite tours.
- Residential homes are best for Matterport depth.
- Retail, restaurant, hotel and industrial cannot carry a demo whose core is the scan.

---

## 5. What the data can answer vs cannot

**Can answer:**
- What does a 2BR in community X ask per month, how many are available, and what is the vacancy? (`apartmentModels[].minRent`, `numUnitsAvailable`, `vacancyPercent`)
- Does this unit's scan agree with the advertised floor plan? Compare `models[].minSquareFeet` and `numBeds` with Matterport `rooms.dimensions.areaFloor` sums and bedroom classifications.
- How wide is every doorway on the route from the entry to the bathroom, and what are the ceiling heights? (`openings.width`, `ceiling`, on Property Insights models)
- What does this room look like empty? (defurnished pano, same pano id)
- Which office suites of 2,000-4,000 SF are available in LA, at what normalized $/SF/yr, from which broker, and are any toured in 3D? (`spaces[]`, `listingContacts`, tour listings)
- Who are the current tenants of building X, in which industries, and how big are they? (occupancy plus company-detail)
- What did comparable apartment buildings sell for per unit, and at what cap rate? (sale comps)
- What is the roof condition, material and defect share of a property, and has it changed since 2016? (Vexcel property/extract by collection, ortho history)
- How tall is the building really, and does that match `numStoriesAboveGrade`? (DSM minus DTM)
- How many cars are in the lot right now, and where are the ADA stalls? (`elements/detect`)
- Which nearby parcels look like this one? Where are the large surface lots in this 2 km area? (embeddings)
- How many apartment units and tenant employees are within 400 m of a storefront? (kit lat/lon, `totalNumUnits`, company-detail `numEmployees` on most)

**Cannot answer:**
- How many cars pass this site per day? (no traffic counts anywhere)
- What is the household income or population around a site? (no demographics; Vexcel has a `census-tract` id only)
- What is the vacancy rate of office or retail in a submarket, and what is the submarket called? (absent)
- How many parking stalls does this lot have, and where are its entrances? (no endpoint; only our own CV or area ÷ 30 m²)
- What is the counter height, how many seats, and where is the hood or drive-thru in this restaurant? (no object detection; almost no restaurant scans)
- What is the NAICS code or revenue of this tenant? (absent)
- When do current leases expire, and at what contract rent? (expiration and contract rent are rarely filled)
- What did this Houston home sell for? (non-disclosure)
- Which amenities does this community have, by name? (ids only)
- Find every model within 500 m of a point using the API. (No geo search; use the model index)

---

## 6. Open questions and untested items

1. **Property Insights coverage by property type.** Only 26 commercial models were sampled. Measure wall graph and openings coverage on about 100 apartment-unit scans and about 50 office scans before relying on scan geometry.
2. **Scan area vs advertised SF.** Is Matterport `areaFloor` (sum over non-Void rooms) close enough to `minSquareFeet` to flag real mismatches? This is untested and is the core of the listing-vs-scan check.
3. **How many apartment floor plans have a linked scan** (`models[].attachments[]` or `units[].attachments[]` with ext ref 36/234)? Not counted.
4. **Splat PLY download and rendering by us.** Only the catalog and drone photos were verified. For commercial use, splats exist on only a handful of properties, almost all Multifamily.
5. **Vexcel features the tutorial describes but we did not test:**
   - `search-image`, `search-url` and `search-vector`
   - `collect-year`
   - detection on oblique-south, east and west
   - lower thresholds or other wording for `parking space`, `dumpster`, `light pole` and `drive-thru`
   - `oriented/query` for time series on a kit property
   - quotas under sustained load (no 429 in about 60 calls)
6. **`property/extract` hit rate at kit coordinates.** It was tested at 5 points, none confirmed to be a kit property except near the LA example. Run it on about 50 kit properties to see 404 rates and how much footprints vary.
7. **The SDK outside localhost.** The key is limited to localhost, so the demo must run on a laptop. Wrong-host behaviour and Tag writes are untested.
8. **What the retail spaces' `spaces[].floorPlan` values are.** Only a few floor-plan Matterport items exist across all spaces.
9. **Detected cars as a demand proxy.** Is `vehicles.count` or SAM3 `car` on a street segment across several collections stable enough to use, even as a stated proxy? Untested.
10. **Repo hygiene for the demo.** Every artifact derived from sponsor data, whether cached JSON, images or the memo, stays out of the public repo. The demo runs from a local, git-ignored cache, the README states that the private dataset and keys are not in this repo, and `tests/test_no_sponsor_data.py` guards against sponsor data being committed.

---

## 7. Practical gotchas

| Topic | In practice |
|---|---|
| Kit join | The commercial kit has no per-property archive members to match by name. Join on `sid` = `MatterportModelId` |
| `homes_listing_id` | It behaves like `ResidentialListingId`, not the residential-listings jsonl `id` |
| `costar_property_id` | It is null on about half of commercial models and sometimes disagrees with the kit, so join through the kit CSV |
| MatterPak | `assets.resources(format:"matterpak")` reported `unavailable` on every sample model; `bundle(id:"mp:matterpak")` gave a URL on every one |
| Splat count | The `splats.count:>0` search returns somewhat fewer models than the index lists as splat models |
| Vexcel `latest=true` | It still returns 5-9 features, one per collection |
| Vexcel layer list | It behaves like a priority order, not newest-first (LA: urban Dec 2025 chosen over urban-r Jul 2026) |
| Vexcel resolution | 7.46 cm projected, about 6.2 cm ground in LA and 6.5 cm in Houston |
| Vexcel endpoints | `/ortho/collections`, `/dsm/extract` and `/dtm/extract` also work, though the quick reference does not list them |
| Kit contacts | Names are on listing `propertyContacts[]` and `listingContacts[]`. The property record's `contacts[]` has no names |
| Space counts | Counts in the kit's concept pages differ from counts profiled from the jsonl; profile the data before relying on a count |
| Frames | The API is Z-up; the SDK returned Y-up |
