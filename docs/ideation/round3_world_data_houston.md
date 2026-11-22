# Round 3 — Outside-in: what Houston's open data unlocks

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Scope: Houston / Harris County / Texas, plus federal datasets that cover it. Checked live on 2026-11-13.
Frame: sponsor data is the truth about the building; open-world data is the pressure on it; the product is the join.

**How to read the status column**
- **VERIFIED** = the page, file header or API endpoint was loaded today and data or a schema was seen.
- **SCHEMA** = the field list was read from official documentation, and the file itself was confirmed downloadable, but not opened.
- **UNVERIFIED** = could not be loaded (reason given), or known only from a search result.
- Numbers in the "evidence" lines are quoted from the linked source. Anything from memory is marked *(from memory)*.

Two findings change what earlier panels assumed:
1. **Houston 311 rows carry an HCAD account number** (`TaxID`, 13 digits) plus lat/lon. Complaints join to a parcel without geocoding.
2. **HCAD publishes, for free, its own income assumptions and every protest outcome**: per-building `occ_rt`, `lease_rt`, `tot_inc`, `units`, `nra`, quality code and depreciation, and per-account ARB hearing initial and final values. "No assessed values" is not a limit.

Things that do **not** exist as open data (checked): certificates of occupancy, the multifamily registration list, the High-Risk Rental Building registry, apartment fire-inspection results, HFD incident history, food inspections after 2015, HCFCD buyout parcels as a live layer, elevation certificates, CenterPoint outage history below county level, any Houston energy-benchmarking disclosure (not confirmed either way), and TDLR elevator data for buildings inside the City of Houston (TDLR does not regulate those).

---

## Step 1 — Inventory

### 1A. City of Houston

| # | Dataset | URL | Contents | Join key | Freshness | Access | Status |
|---|---|---|---|---|---|---|---|
| 1 | Houston 311 Public Data Extract | Index `311.houstontx.gov/servicerequestdata.html`; files `hfdapp.houstontx.gov/311/311-CRIS-Public-Data-Extract-D365-MTD-compressed.txt` and `...-YTD-compressed-{2011..2026}.txt` | Case number, `Incident Address`, `Latitude`, `Longitude`, `Created Date Local`, `Closed Date`, `Incident Case Type`, `Department`, `SLA Time`, `TaxID`, `Description`, `Resolution Notes`, `Latest Case Notes`. Case types seen this month: Water Leak, Sewer Wastewater, Illegal Dumpsite, Weeds/Trash/Stagnant Water, Building Code Violation, Drainage, **MultiFamily Habitability Violation**, Dangerous Buildings, Fire Code Complaint, Flooding | **HCAD account (`TaxID`)**, lat/lon, address | Month and year to date daily; 2011 onward | Pipe-delimited bulk text (2025 file is 382 MB) | VERIFIED |
| 2 | Permit activity weekly reports | `houstonpermittingcenter.org/sold-permits-search` (one XLSX per week); pre-Dec-2025 at `houstontx.gov/planning/DevelopRegs/dev_reports.html` | `Zip Code, Permit Date, Permit Type, Project No, Address, Comments` (comments hold SF, use, occupancy class) | Address | Weekly, 2026-01-05 to 2026-10-19 listed | XLSX | VERIFIED |
| 3 | Certificates of occupancy | — | — | — | — | Records request only | Does not exist as open data |
| 4 | DON building code violations | `data.houstontx.gov/dataset/city-of-houston-building-code-enforcement-violations-don` | Address-level violations | Address | Stale (about 2014) | XLSX | VERIFIED listing; stale |
| 5 | Multi-Family Habitability registrations, inspections, High-Risk Rental registry | `houstonpermittingcenter.org/building-code-enforcement/multi-family-habitability-inspections` | Registration needs an HCAD tax id and a CO number | — | — | None | No open data. Proxy = 311 case type in row 1 |
| 6 | HFD/HPD active incidents | `cohweb.houstontx.gov/activeincidents/combined.aspx` | Agency, address or block, call time, incident type | Address (often block) | Live, no history | HTML only | VERIFIED |
| 7 | HPD NIBRS crime | `houstontx.gov/police/cs/xls/NIBRSPublicView2026.csv` (2019–2026) | Date, hour, NIBRS class, `Premise`, street number/name, ZIP, `Map Longitude`, `Map Latitude` | Address, lat/lon | Current to 2026-07-30 (3+ months behind) | CSV | VERIFIED |
| 8 | Health Dept food inspections | `data.houstontx.gov` | Inspections and violations FY2011–2015 | Site | Ends 2015 | XLSX | VERIFIED as stale |
| 9 | City parcel layer (HCAD mirror) | `geohwp.houstontx.gov/arcgis/rest/services/03_BaseData_External/Parcels_Current/MapServer/4/query` | `PARCEL_ID`, `OWNER`, `ADDRESS`, `STATECLASS`, `LAND_VALUE`, `BUILDVALUE`, `APP_VALUE`, `MARKET_VAL`, `YEAR_BUILT`, `yr_remodel`, `IMPR_SQ_FT`, `LANDUSE_DS` | **lat/lon point-in-parcel → HCAD account** | Published 2025-04-16 | ArcGIS REST | VERIFIED (point query run by me) |
| 10 | HISD attendance zones 2026–27 | `services7.arcgis.com/YNiGsHEfQPYkIqX5/.../Elementary_School_Boundaries_2026_2027/FeatureServer/1` | Campus number, name, grades, Title I | Point-in-polygon | 2026–27 | ArcGIS REST | VERIFIED |

### 1B. Harris County and appraisal district

| # | Dataset | URL | Contents | Join key | Freshness | Access | Status |
|---|---|---|---|---|---|---|---|
| 11 | HCAD real property roll | `download.hcad.org/data/CAMA/2026/Real_acct_owner.zip` (213 MB), `Real_building_land.zip`; codebook `hcad.org/assets/uploads/pdf/pdataCodebook.pdf` | `real_acct`: `acct`, `site_addr_1`, `state_class`, `land_val`, `bld_val`, `tot_appr_val`, `tot_mkt_val`, `prior_tot_appr_val`, `prior_tot_mkt_val`, `new_own_dt`, `protested`. `building_other`: `impr_tp`, `qa_cd`, `date_erected`, `yr_remodel`, `im_sq_ft`, `gross_ar`, **`units`, `nra`, `lease_rt`, `occ_rt`, `tot_inc`, `accrued_depr_pct`**. Also `owners`, `deeds`, `permits.txt`, `extra_features` | `acct` | Files last modified 2026-11-09 | Tab-delimited bulk | SCHEMA (codebook read; HTTP 200 on the zips confirmed by me) |
| 12 | HCAD ARB protest and hearing files | `download.hcad.org/data/CAMA/2026/Hearing_files.zip` (18.8 MB) | `arb_hearings_real`: `acct`, `Tax_Year`, `Hearing_Type`, `Scheduled_for_Date`, `Actual_Hearing_Date`, `Letter_Type`, `Agent_Code`, **`Initial_Appraised_Value`, `Initial_Market_Value`, `Final_Appraised_Value`, `Final_Market_Value`**. `arb_protest_real`: `acct`, `protested_by`, `protested_dt` | `acct` | Last modified 2026-11-09 | Bulk | SCHEMA (HTTP 200 confirmed by me) |
| 13 | Harris County JP courts public extract | `jpwebsite.harriscountytx.gov/PublicExtracts/search.jsp`; layout `docs/CivilFileSpec.pdf` | Case type (Eviction), style, plaintiff address, **defendant address lines**, judgment text/date/amount, attorney fees | Defendant address (the unit), plaintiff name | Daily, any date range | Self-serve TXT/CSV/XML | VERIFIED (form and layout) |
| 14 | Texas Housers Harris eviction table, 2024 | `texashousers.org/harriscountyevictions/` (`/wp-content/uploads/2025/09/exporttable.xlsx`) | Property- and owner-linked filing counts | Property name, tract | 2024 | XLSX | VERIFIED (page) |
| 15 | January Advisors eviction dashboard | `januaryadvisors.com/evictions/` | Daily JP data since 2020 | Not stated | Daily | Dashboard, no download found | UNVERIFIED |
| 16 | Eviction Lab tracking, Houston | `evictionlab.org/eviction-tracking/get-the-data/` | Weekly/monthly filings | Tract | 06/2026 per snippet | CSV | UNVERIFIED (403) |
| 17 | HCFCD GIS services | `gis.hctx.net/arcgishcpid/rest/services/HCFCD` | 21 services incl. `Building_Footprints_2018`, `FloodZone10yr`, `Contours_2018`, and a mirror of FEMA layers | lat/lon | 2018 vintage | ArcGIS REST | VERIFIED. No buyout layer |
| 18 | Harris County Flood Warning System | `harriscountyfws.org` | Rainfall and stream gauges | Gauge id | Real time | Per-gauge Excel export; **no API** | VERIFIED |
| 19 | MAAPnext (new floodplain maps) | `maapnext.harriscountytx.gov` | Draft maps; "cannot be used for insurance or regulatory decisions" | Web map only | Draft; no download | — | VERIFIED (status) |

### 1C. State of Texas

| # | Dataset | URL | Contents | Join key | Freshness | Access | Status |
|---|---|---|---|---|---|---|---|
| 20 | Active Sales Tax Permit Holders | `data.texas.gov/resource/jrea-zgmq.json` | `taxpayer_name`, `outlet_name`, `outlet_address`, `outlet_zip_code`, `outlet_county_code` (101 = Harris), **`outlet_naics_code`**, `outlet_permit_issue_date`, `outlet_first_sales_date` | Address + name | Live | Socrata | VERIFIED (queried by me) |
| 21 | Mixed Beverage Gross Receipts | `data.texas.gov/resource/naix-2893.json` | `location_name`, `location_address`, `tabc_permit_number`, monthly `liquor_receipts`, `wine_receipts`, `beer_receipts`, **`total_receipts`** | Address | Monthly; latest 2026-10-31 | Socrata | VERIFIED |
| 22 | TABC License Information | `data.texas.gov/resource/7hf9-qc9f.json` | Licence type/status, trade name, owner, address, issue and expiry dates | Address | Not checked | Socrata | VERIFIED |
| 23 | Hotel Tax Permits | `data.texas.gov/resource/hdzd-884n.json` | `loc_name`, `address_text`, `loc_city`, `naics`, `resp_begin_date`, `out_of_business_date` | Address | Updated 2026-11-07 | Socrata | VERIFIED (catalog). Per-hotel room receipts: not found as open data |
| 24 | HHSC child-care operations | `data.texas.gov/resource/bc5r-88dy.json` | Operation type, name, address, deficiencies by severity, inspections, adverse actions | Address | Live | Socrata | VERIFIED |
| 25 | TDLR elevators | `tdlr.texas.gov/Elevator_SearchApp/Elevator/ExportCsv` | Building name, address, last and next inspection, equipment type, floors, year installed | Address | Not stated | CSV | SCHEMA. **Excludes City of Houston** — useless here |
| 26 | TDLR architectural barriers (TABS) | `tdlr.texas.gov/TABS/Search` | Project, address, dates, estimated cost, scope, owner | Address | Live | Lookup only, no export | VERIFIED |
| 27 | TDHCA Housing Tax Credit inventory | `tdhca.texas.gov/.../HTCPropertyInventory_0.xlsx` | State LIHTC property list | Address, name | 2026-10-30, monthly | XLSX | VERIFIED link; columns not opened |
| 28 | TxDOT AADT annual counts | `services.arcgis.com/KTcxiTD9dsQw4r7Z/ArcGIS/rest/services/TxDOT_AADT_Annuals_(Public_View)/FeatureServer/0` | Count stations with `AADT_RPT_QTY` (2025) and `AADT_RPT_HIST_01..19_QTY` back to 2006 | lat/lon (nearest station) | Edited Oct 2026 | ArcGIS REST | VERIFIED (queried by me) |
| 29 | TCEQ air emission events | `www2.tceq.texas.gov/oce/eer/` | Events by county and date | Facility | From 2003 | Web form + RSS, no bulk | VERIFIED |
| 30 | TEA school ratings | `rptsvr1.tea.texas.gov/perfreport/account/acct_download?year=2026` | Campus A–F ratings | Campus number (links to row 10) | 2026 | Download | VERIFIED link |
| 31 | Texas PACE project list | `texaspaceauthority.org/tx-pace-projects-in-texas/` | Project title, year, city, amount; no street address | Name | — | Web list | VERIFIED (11 Houston projects) |

### 1D. Federal

| # | Dataset | URL | Contents | Join key | Freshness | Access | Status |
|---|---|---|---|---|---|---|---|
| 32 | FEMA NFHL flood zones (layer 28) | `hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query` | `FLD_ZONE`, `ZONE_SUBTY`, `SFHA_TF`, `STATIC_BFE`, `DEPTH` | lat/lon point or polygon | Continuous | ArcGIS REST | VERIFIED (point query run by me) |
| 33 | OpenFEMA NFIP claims v3 | `fema.gov/api/open/v3/NfipClaims?$filter=countyCode eq '48201'` | `buildingDamageAmount`, `amountPaidOnBuildingClaim`, `occupancyType`, `numberOfFloorsInTheInsuredBuilding`, `yearOfLoss`, `waterDepth`, `numberOfUnits`, `rentalPropertyIndicator` | Block group, ZIP, 0.1° grid. **No address** | 2026-09-08 | REST | VERIFIED (v2 path is 404) |
| 34 | OpenFEMA NFIP policies v3 | `fema.gov/api/open/v3/NfipPolicies` | `policyCost`, `totalBuildingInsuranceCoverage`, `ratedFloodZone`, `tenantIndicator` | Block group | 2026-09-08 | REST | VERIFIED |
| 35 | FEMA historical damage-assessment points (incl. Harvey) | `services.arcgis.com/XG15cJAlne2vxtgt/ArcGIS/rest/services/FEMA_Historical_Geospatial_Damage_Assessment_Database/FeatureServer/0` | Damage level, inundation depth | lat/lon | Archive | ArcGIS REST | VERIFIED (layer) |
| 36 | FEMA Individual Assistance, Harvey (DR-4332) | `fema.gov/api/open/v2/IndividualsAndHouseholdsProgramValidRegistrations?$filter=disasterNumber eq 4332` | `ownRent`, `residenceType`, `waterLevel`, `floodDamageAmount` | Block group, ZIP | 2026-11-13 | REST | VERIFIED |
| 37 | NOAA Storm Events | `ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/` | Hail, wind, tornado, flash flood details | County, lat/lon | 2026 file dated 2026-10-26 | CSV | VERIFIED |
| 38 | SPC hail/wind/tornado reports | `spc.noaa.gov/wcm/` | Point reports, 1955–2025 | lat/lon | 2026-04-23 | CSV | VERIFIED |
| 39 | MRMS maximum hail size grids | `noaa-mrms-pds.s3.amazonaws.com` prefix `CONUS/MESH_Max_1440min_00.50/` | Daily hail-size raster | Grid cell | Daily since 2020-10-14 | GRIB2 on S3 | VERIFIED |
| 40 | NOAA Atlas 14 | `hdsc.nws.noaa.gov/cgi-bin/new/fe_text_mean.csv?lat=..&lon=..` | Rainfall frequency (downtown 24 h 100-year = 17.0 in) | lat/lon | — | CSV | VERIFIED |
| 41 | USGS 3DEP elevation | `epqs.nationalmap.gov/v1/json?x=lon&y=lat&wkid=4326&units=Feet` | Ground elevation, 1 m | lat/lon | — | REST | VERIFIED |
| 42 | Census ACS 5-year 2020–2024 | `api.census.gov/data/2024/acs/acs5` | Rent burden, gross rent, year built, vehicles, disability, age, language | Tract, block group | Released 2026-01-29 | REST, free key | VERIFIED listing |
| 43 | LEHD LODES8 | `lehd.ces.census.gov/data/lodes/LODES8/tx/` | Jobs by workplace and residence block | 2020 block | 2024 data, files dated 2026-10-14 | CSV | VERIFIED |
| 44 | County/ZIP Business Patterns | `api.census.gov/data/2023/cbp` | Establishments, employment, payroll by NAICS | County, ZIP | 2023 | REST | VERIFIED listing |
| 45 | HUD FMR / Small Area FMR | `huduser.gov/hudapi/public/fmr/statedata/TX` | Rent by bedroom count by ZIP | ZIP | FY2026 | REST, free token | 401 without token; token required |
| 46 | HUD vouchers by tract | `services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/Housing_Choice_Vouchers_by_Tract/FeatureServer/0` | `HCV_PUBLIC`, `HCV_PUBLIC_PCT` | Tract | To 12/2025 | ArcGIS REST | VERIFIED |
| 47 | HUD LIHTC properties | same host, `LIHTC/FeatureServer/0` | `PROJECT`, `PROJ_ADD`, `LAT`, `LON`, `N_UNITS`, `LI_UNITS`, `YR_PIS` | Address, lat/lon | Modified 2026-04-20 | ArcGIS REST | VERIFIED (362 Harris records) |
| 48 | HUD Multifamily Assisted Properties | same host, `MULTIFAMILY_PROPERTIES_ASSISTED/FeatureServer/0` | Name, address, **`REAC_LAST_INSPECTION_SCORE` and date**, `TROUBLED_CODE`, contract expiry, `RENT_TO_FMR_RATIO1`, management agent | Address, lat/lon | Monthly; 2026-11-03 | ArcGIS REST | VERIFIED |
| 49 | HUD Insured Multifamily | same host, `HUD_Insured_Multifamily_Properties/FeatureServer/0` | FHA number, loan program, original loan amount | Address, lat/lon | 2026-10-25 | ArcGIS REST | VERIFIED |
| 50 | CDC PLACES / SVI | `data.cdc.gov/resource/cwsq-ngmh.json?countyfips=48201` | Tract health measures; SVI 2022 | Tract | 2023 BRFSS | REST | VERIFIED |
| 51 | EPA TRI and ECHO | `data.epa.gov/efservice/tri_facility/...`; `echodata.epa.gov/echo/echo_rest_services.get_facilities` | Facilities, releases, violations, penalties | lat/lon, address | Live | REST | VERIFIED |
| 52 | EJScreen 2.3 | `pedp-ejscreen.azurewebsites.net` (EPA access ended 2025-02-05) | Block-group indexes | Block group | Frozen 2024 | Mirror map; no API | VERIFIED (mirror) |
| 53 | DOE EAGLE-I outages | `doi.org/10.13139/OLCF/2500278` | Customers out, 15-minute | **County only** | Through 2024 | Download | VERIFIED. Too coarse for a building |
| 54 | CenterPoint outage history | — | — | — | — | No machine-readable feed found | Does not exist as open data |
| 55 | H3AT heat mapping 2020 and 2024 | `h3at.org` | Heat Watch traverses and rasters | lat/lon raster | 2020, 2024 | Download link not seen; request by email | Site VERIFIED |
| 56 | USFS/NLCD tree canopy | `mrlc.gov/data/type/tree-canopy` | 30 m canopy, annual 1985–2025 | Raster | 2025 | Download, WMS | VERIFIED |
| 57 | METRO GTFS static and realtime | static via `mobilitydatabase.org/feeds/gtfs/mdb-2060`; realtime `api-portal.ridemetro.org` | Stops, routes, schedules, predictions | lat/lon | Snapshot 2026-10-09 | ZIP; realtime needs free key | VERIFIED |
| 58 | OpenStreetMap / Overture | `overpass-api.de`; `stac.overturemaps.org` | Footprints, POIs with categories; `height` often null | lat/lon | Overture 2026-10-21 | API / Parquet | VERIFIED up; Houston quality not assessed |
| 59 | State energy / weatherization at building level | — | TDHCA weatherization, SECO, CenterPoint multifamily programme | — | — | Nothing building-level found | Not available / not reached |

Gaps in my own coverage: Texas PUC Beryl outage report (paywalled response), TxDOT crash records (login rules not seen), PVWatts (domain did not resolve), TDLR boilers, Harris County Clerk deeds, National Housing Preservation Database. Two research passes hit the web-search quota before finishing the heat, energy and voucher evidence.

---

## Step 2 — What each dataset's owner cannot do without the building

One line each. "Join gives" = what neither side has alone.

| # | Problem | Owner | Evidence it is real | Open data + sponsor layers | Join gives |
|---|---|---|---|---|---|
| P1 | Apartment owners are taxed on an income model they have never seen, and protest it with hand-built evidence | Apartment owners, tax agents; on the other side HCAD | About 516,205 Harris protests in 2024 and 5,539 commercial lawsuits challenging $84.1B (consultant figures, not HCAD: `poconnor.com/property-taxes-Harris-county-2024`); 2025: 60% of commercial accounts raised (`bisnow.com/news/houston/...-129296`) | HCAD roll + ARB files (11, 12, 9); A rents/vacancy/comps, C roof condition over time, B interior finish | HCAD's assumed occupancy and rent against the property's actual rent roll and dated physical condition, plus what the ARB did to this account before |
| P2 | 15 inspectors, 3,300–3,600 complaints a year, a 4-year cycle goal, and a new high-risk programme with no way to pick buildings before a visit | Houston Public Works multifamily habitability team; tenants | City deck 2026-03-30: "3 SENIOR INSPECTORS, 12 INSPECTORS", "1,200 INSPECTIONS PER YEAR", "3,300 TO 3,600 311 COMPLAINTS PER YEAR" (`cohips.houstontx.gov/council/committees/econdev/20260330-joint-hac/Overview-Apartment-Inspection-Ordinance.pdf`); high-risk = "10 or more qualifying code violations within a six-month period" (click2houston 2026-07-31) | 311 (1), NIBRS (7), JP evictions (13), HCAD owner (11); A units/manager/year built/vacancy, C roof defects, tarps, pool, debris over time, B marketed-condition baseline | Complaints per unit (311 has no unit count), exterior evidence before the drive, and roll-up by manager across a portfolio |
| P3 | A Texas landlord must tell a renter if the unit is in the 100-year floodplain or flooded in the last 5 years, but the parcel-level answer is wrong for a 20-building complex; and NFIP caps cover per building | Apartment owners and managers, renters, lenders | Property Code 92.0135 (leases from 2022-01-01; SB 2349 adds both signatures from 2025-09-01); NFIP "other residential" cap $500,000 per building; HCFCD: 154,170 homes flooded in Harvey and about 36% of flooded homes insured (`communityimpact.com/news/2018/06/08/hurricane-harvey-damage-report-harris-county`) | NFHL (32), 3DEP (41), FEMA damage points (35), 311 Flooding/Drainage (1), NFIP claims (33); C footprints, DSM/DTM, **Harvey 2017 imagery**, A units/stories/floor plans/listings, B ground-floor unit scans | Flood status per building and per ground-floor unit, not per parcel; uninsured gap per building |
| P4 | A housing authority must document that a voucher rent is reasonable against comparable unassisted units, and voucher holders cannot tell which listed units fit the payment standard | Houston Housing Authority (about 19,000 voucher households, Planetizen 2026-05), voucher holders | Source-of-income refusal is legal in Texas (SB 267, 2015: `nlihc.org/resource/texas-legislature-bans-local-ordinances-protecting-voucher-holders-discrimination`); HHA still reconciling lost voucher records in 2026 (search snippet, unconfirmed) | SAFMR (45), vouchers by tract (46), ACS (42), TEA/HISD (10, 30); A floor-plan rents and availability, B bedroom count/room sizes/openings, C site condition | Unit-level comparables with measured size and bedroom count, under the ZIP payment standard, in buildings whose exterior does not fail on sight |
| P5 | After hail or wind, owner and insurer argue about which storm did the damage and whether it pre-existed; insurers now non-renew from aerial photos | Apartment owners, public adjusters, carriers | Houston multifamily premiums +45% year over year to Q1 2023 (RealPage via Multifamily Dive); TDI records of aerial-photo nonrenewals (`hppr.org/hppr-news/2025-05-13/...`); derecho May 2024, Beryl July 2024 | MRMS hail grids (39), SPC reports (38), Storm Events (37), HCAD `permits.txt` and city permits (2, 11); C roof defects by collection date, A units/value/year built | Roof state bracketed by dated imagery either side of a dated storm, checked against roof permits |
| P6 | Houston's Right-to-AC ordinance (passed 2026-08-19) is enforced only on complaint; nobody knows which rentals lack cooling | Houston Health Department, tenants | `texashousers.org/2026/08/25/houston-right-to-ac-ordinance-passed/`; 61 Harris heat deaths in 2023 (abc13) | 311 (1), tree canopy (56), H3AT (55), ACS age 65+ (42); C roof AC unit counts, obliques for window units, B panoramas for vents/units, A year built | A candidate list of complexes with no visible cooling plant in hot, low-canopy tracts |
| P7 | A tenant facing eviction soon after a repair complaint has a retaliation defence, but nobody assembles the dates | Legal aid lawyers, tenants | 76,321 filings in 2024; top 30 properties filed 5,817; 37% default judgments (`texashousers.org/harriscountyevictions/`); median 24 days to judgment | JP extract (13), 311 (1); A rents (claim vs asking rent), units, C dated condition evidence | Filing, complaint and physical-condition timeline for one address, in under the 24-day window |
| P8 | Independent senior apartments have no backup-power rule; emergency managers do not know which towers trap residents when power fails | Houston/Harris emergency management | 36 Beryl-linked deaths, 75% aged 60+; Scott Street Lofts senior apartments without power 4 days (`texasstandard.org/stories/hurricane-beryl-deaths-houston-area-seniors-heat-centerpoint-outage/`) | ACS (42), EAGLE-I county (53), METRO (57); A lifestyle type senior, stories, units, C generator/plant detection, B corridor and stair geometry | A ranked wellness-check list. Limited by county-level outage data |
| P9 | HUD-assisted owners face NSPIRE inspections whose site and exterior items are visible from the air | HUD-assisted owners, tenant advocates | Coppertree Village scored 31 in 2018 (`projects.propublica.org/hud/properties/800020793`); HUD OIG 2026 on 1,323 properties scoring 60–70 | HUD assisted (48), LIHTC (47); C roof, hardscape, debris; B unit scans; A match by name/address | Pre-inspection deficiency list. Kit overlap with HUD properties unknown |
| P10 | HCAD cannot see sale prices (non-disclosure state) or interiors; its roll has wrong unit counts and missed improvements | HCAD | Texas non-disclosure (many kit sale comps carry no price) | HCAD (11), permits (2); A units/GBA/comps, C footprint change, B measured area | Roll corrections: omitted improvements, unit-count errors. Mirror image of P1 |
| P11 | Unpermitted additions and re-roofs are found only by complaint | Houston Permitting Center | 311 "Building Code Violation" 199 cases in a partial month sample | Permits (2), HCAD `permits.txt` (11), 311 (1); C footprint/roof change between collections | Change seen from above with no matching permit. Noisy footprints |
| P12 | Landlords and lenders cannot see a bar or restaurant tenant's sales until it stops paying | Retail/mixed-use landlords, lenders | CoStar has no tenant revenue | Mixed beverage receipts (21), sales tax permits with NAICS (20), TABC (22); A tenancies, space SF, rents | Monthly sales per SF for licensed tenants and a NAICS code for most tenants |
| P13 | Hotel lenders have room rate but no occupancy for the Houston hotels in the kit | Hotel lenders/appraisers | Kit RevPAR field empty | Hotel tax permits (23), mixed beverage receipts (21); A ADR, rooms; C parking cars over time | Partial revenue proxy only; per-hotel room receipts not found as open data |
| P14 | Listings name schools that the 2026–27 boundaries no longer assign | Renters, listing platforms | Unconfirmed that errors exist; boundaries are redrawn yearly | HISD zones (10), TEA ratings (30); A `residentialProfile.schools[]` | A correction list. Low cost of error |
| P15 | Child-care operators need space near apartments with children; licensing sets indoor and outdoor area minimums | Operators, HHSC | Area rule not checked today | HHSC operations (24), ACS under-5 (42); A available spaces, B measured room areas, C outdoor play area | Fit test for a space. Close to site selection; low priority |
| P16 | Dangerous-building backlog: "1,806 residential properties", half pending a year or more; $30M of stormwater money voted for demolition | Houston Department of Neighborhoods | click2houston 2025-10-30; `houstontx.gov/moc/2026/stormwater-funding-dangerous-structures.html` | 311 Dangerous Buildings (1), HCAD owner (11); C roof collapse over time | Decay timeline per parcel. Mostly houses outside the kit, so only one sponsor layer |
| P17 | Tenants near industrial plants are not told about releases | Renters, managers | ECHO lists 29,164 Houston-area facility rows | TRI/ECHO (51), TCEQ events (29); A units, B window openings | Exposure note per building. No clear action |

---

## Step 3 — Ranking

Realness = how costly and well-evidenced the problem is. Fit = harsh score across **both** the sponsor layers and the open data (do the fields exist, at building level, for the properties in the kit).

| Rank | Problem | Realness | Fit | Why the fit score |
|---|---|---|---|---|
| 1 | P1 Tax protest evidence | 5 | 4 | HCAD files are complete and per-account; A rents/vacancy cover the Houston communities in the kit; C gives dated condition. B is supporting only. Multi-parcel complexes complicate the match |
| 2 | P2 Inspection triage | 5 | 4 | 311 joins by account number; A gives units and manager; C gives exterior evidence. No open violation or inspection data to validate against; B is a baseline, not evidence |
| 3 | P3 Flood per building | 4 | 4 | NFHL, 3DEP, damage points all query by point; C has footprints, DSM/DTM and Harvey imagery. Claims are block-group only; ground-floor scans are not flagged as such |
| 4 | P4 Voucher match and rent reasonableness | 4 | 4 | Per-plan rents and SAFMR line up exactly; B measures bedrooms. Landlord acceptance is unknowable from data |
| 5 | P5 Storm-loss attribution | 4 | 3 | C collections are annual, so brackets are a year wide; B and A contribute little |
| 6 | P7 Eviction retaliation timeline | 4 | 3 | Mostly an open-data join; sponsor layers add rent and condition context only |
| 7 | P6 Right-to-AC candidates | 4 | 2 | Buildings without AC are likely small, old and outside the kit; detection of window units untested |
| 8 | P10 Roll corrections for HCAD | 3 | 4 | Same data as P1, weaker action |
| 9 | P12 Tenant sales from beverage receipts | 3 | 3 | Good open data; only licensed tenants; retail is thin in the kit |
| 10 | P9 NSPIRE pre-inspection | 4 | 2 | Kit overlap with HUD-assisted stock unknown |
| 11 | P8 Senior tower outage list | 4 | 2 | Outage data is county-level |
| 12 | P11 Unpermitted work | 3 | 2 | Footprints vary wildly between collections |
| 13+ | P13, P14, P15, P16, P17 | 2–4 | 1–2 | One sponsor layer, or no action |

**My pick: P1**, with P2 as the public-interest alternative. They share one spine (kit lat/lon → HCAD account → everything keyed on that account), so the first 6 hours of build are common.

---

## Top 4 developed

### 1. P1 — Property-tax protest evidence for apartment owners

**Problem in the owner's words.** "HCAD raised my value again. I do not know what occupancy and rent they assumed, I do not know what my neighbours are appraised at, and my agent takes a share of whatever he saves me."

**What they do today and what it costs.**
- Harris County saw about 516,205 protests in 2024, and 5,539 commercial lawsuits challenging $84.1B of board-set value with a $10.7B commercial reduction. These are tax-consultant figures (`poconnor.com/property-taxes-Harris-county-2024`), not HCAD's, and the same firm's 2023 figures are inconsistent. Treat them as order of magnitude.
- The Houston Chronicle reported more than 371,500 protests in 2018.
- The work is manual: pull the HCAD record, choose comparable accounts, compute a median appraised value per square foot, build an income statement, add photos of deferred maintenance. Agents commonly work on a contingency share of the saving *(from memory; rate not sourced)*.

**Open data.** HCAD `real_acct` (`tot_appr_val`, `tot_mkt_val`, `prior_tot_*`, `state_class`, `protested`), `building_other` (`units`, `nra`, `lease_rt`, `occ_rt`, `tot_inc`, `qa_cd`, `accrued_depr_pct`, `date_erected`, `yr_remodel`), `arb_hearings_real` (initial and final values, `Letter_Type`, `Agent_Code`), `arb_protest_real`; city parcel layer for point-in-parcel; NFHL zone as an external-obsolescence argument; 311 counts as corroboration of condition.

**Sponsor fields.**
- A: `propertyApartment.models[]` (plans, unit counts), apartment-listing `minRent/maxRent`, `numUnitsAvailable`, `vacancyPercent`, `buildingClass`, `constructionEvents[]`, `grossBuildingAreaSquareFeet`; sale comps `soldForPrice`, `pricePerUnit`, `capitalizationRateActual`, `saleConditions[]`.
- C: `roof-characteristics.condition`, `roof-defects.*` by collection, ortho and oblique crops, with capture dates.
- B: panoramas and defurnished views of unit interiors as finish-quality evidence against HCAD's `qa_cd`.

**Reasoning — where sources disagree.**
1. *Occupancy and rent.* HCAD's `occ_rt` and `lease_rt` against the kit's `vacancyPercent` and unit-weighted asking rent. Asking rent is not collected rent, so the agent must discount it and say so.
2. *Size and unit count.* HCAD `units` and `nra` against kit unit totals and GBA. A difference can help or hurt the owner; the agent must check direction before using it.
3. *Valuation date.* Texas values property as of January 1 *(from memory)*. The agent must pick the aerial collection nearest January 1 of the tax year, not the newest, and must not cite damage that appeared later.
4. *Equal and uniform.* Choose comparable accounts (same class, age band, unit count band, same HCAD neighbourhood or kit submarket id), take the median appraised value per unit or per SF, and justify each inclusion. Comparable choice is where an agent earns its place: too few and the board rejects it, cherry-picked and the appraiser dismantles it.
5. *History.* `arb_hearings_real` shows what the board did to this account and to the comparables in earlier years. If the account was already cut last year, the argument changes.
6. *Multi-parcel complexes.* One community can sit on several accounts. The agent must find all accounts under the footprints and sum them.

**Action at the end.** A filled Notice of Protest (Comptroller Form 50-132) with an evidence packet: income reconstruction, comparable grid, dated aerial exhibits, hearing history. Protests are normally due May 15 or 30 days after the notice *(from memory)*. In November the live routes are a late correction motion under Tax Code §25.25 for substantial over-appraisal, which must be filed before the tax delinquency date *(from memory; thresholds not checked)*, and preparing the January 1 evidence for next year. The demo should state which route it is drafting.

**Worked example (illustrative values, marked as such).** A 1970s garden community of about 250 units in southwest Houston.
1. Kit lat/lon → city parcel layer → two HCAD accounts.
2. HCAD `building_other` shows `occ_rt` 0.93 and a `lease_rt` *(illustrative)*; the kit shows `vacancyPercent` 14 and plan rents that weight to a lower figure *(illustrative)*.
3. Vexcel collections nearest January 1 show `roof-defects.tarp.detected` true on three structures in two consecutive years.
4. Nine comparable accounts chosen; the subject's appraised value per unit sits above the median.
5. `arb_hearings_real`: subject not protested in the last two years; six of nine comparables were, and five were reduced.
6. Output: a requested value with two independent supports, the exhibits, and a list of what the appraiser will attack (asking rent is not collected rent; one comparable is in a floodplain).

**Build effort, 2 engineers, about 28 hours.**
| Piece | Hours |
|---|---|
| Load HCAD roll, buildings and hearing files into SQLite/DuckDB; index by account | 3 |
| Kit lat/lon → parcel account(s), including multi-parcel handling | 4 |
| Income reconstruction from kit rents/vacancy vs HCAD assumptions | 4 |
| Comparable selection and equal-and-uniform grid | 5 |
| Vexcel condition by collection, January 1 date logic, exhibit crops | 5 |
| Interior exhibits from scans | 2 |
| Packet and form generation | 3 |
| Review screen and rehearsal | 2 |

**Hardest part.** Matching a kit community to the right set of HCAD accounts, then producing comparables a real appraiser would not laugh at.

**Cheapest check that would kill it.** Open `building_other` and `arb_hearings_real` for 30 kit apartment communities. If `occ_rt`/`lease_rt`/`units` are blank for apartments, or fewer than about 20 of 30 match cleanly to accounts, the income argument and the match both fail. One hour.

---

### 2. P2 — Pre-inspection triage for Houston's apartment inspectors

**Problem in the owner's words.** The city's own deck: 3 senior inspectors and 12 inspectors, about 1,200 inspections a year, 3,300 to 3,600 habitability complaints a year, and a goal of inspecting every apartment on a 4-year cycle. The fire chief: "There have been apartment complexes that HFD has cited over and over again."

**What they do today and what it costs.**
- Inspections are driven by complaints through 311. Residents called "more than 2,400 times for multifamily habitability concerns" in 2024 (Community Impact, 2025-11-05).
- The High-Risk Rental Building programme (approved 2026-05-06) targets a property with 10 or more qualifying violations in six months. No public registry exists, and a property enters only after violations are written, which needs inspections that there is no staff for.
- Fines were proposed at $250–$2,000 per day per violation.

**Open data.** 311 extract filtered to MultiFamily Habitability Violation, Building Code Violation, Fire Code Complaint, Water Leak, Sewer, Stagnant Water, Dumpster, Flooding, by `TaxID`, 2011 onward, with `Description` and `Resolution Notes`; HPD NIBRS by address and premise; JP eviction filings by defendant address; HCAD owner name and mailing address; NFHL zone.

**Sponsor fields.**
- A: unit totals (denominator), `propertyManagementCompanyName`, year built, `buildingClass`, `vacancyPercent`, rent level, number of stories.
- C: `roof-defects.{tarp, missing-material, discoloration}` by collection; `pool.*` (a green or empty pool matches the 311 stagnant-water type); free-text detection for debris piles, boarded windows, burned structures; obliques of stairs and balconies.
- B: marketing scans as the "as advertised" baseline; where openings exist, a check that each room labelled bedroom has a window.

**Reasoning — where sources disagree.**
1. Raw complaint counts favour large complexes; per-unit rates favour small ones with one angry tenant. The agent must report both and prefer repeated distinct complainants, read from descriptions.
2. A complex with zero complaints and a tarped roof for three years is either vacant or has tenants who do not call. Vacancy from the kit and eviction filings help decide which.
3. 311 `Resolution Notes` may say "no violation found" while the aerial shows the defect persisting. The agent flags the conflict; it does not overrule the inspector.
4. Complaints are often filed against the leasing-office address while the defect is in another building on another account. Roll up all accounts under one community.
5. Roll up by manager and by HCAD owner: three mid-ranked properties under one manager may matter more than one top-ranked property.

**Action at the end.** A weekly inspection docket: ranked properties, a one-page dossier each (complaint timeline, aerial exhibits with dates, which buildings on the site to walk first, owner of record and mailing address for the notice), and a suggested route. For a property that meets a documented threshold, a draft referral to the high-risk programme for a human to sign.

**Worked example (illustrative).** A 400-unit complex in the Gulfton area: several dozen 311 cases in 12 months across habitability, sewer and water leak; eviction filings well above the county's 9.7% rate; Vexcel shows tarps on two roofs in 2023 persisting in 2025 and a pool that changes from blue to green. The dossier names the two buildings and gives the owner's HCAD mailing address.

**Build effort.**
| Piece | Hours |
|---|---|
| Stream and load 311 files 2023–2026; classify building-related types | 4 |
| Kit property → HCAD account set → 311 by `TaxID` (+ lat/lon fallback) | 4 |
| Eviction and crime joins by address | 4 |
| Vexcel condition time series and exhibit crops for the top 100 | 6 |
| Scoring with stated rules, manager/owner roll-up | 4 |
| Dossier and docket output | 4 |
| Rehearsal | 2 |

**Hardest part.** No open ground truth. Violation and inspection results are not published, so the ranking cannot be validated except against news-reported bad actors and the Texas Housers top-evictor list.

**Cheapest check that would kill it.** Count 2025 habitability-type 311 cases whose `TaxID` falls on a kit multifamily property. If only a handful of the kit's Houston communities have any, the kit does not contain the troubled stock and the join is empty. Two hours.

---

### 3. P3 — Flood status per building: lease disclosure and insurance gap

**Problem in the owner's words.** "My site plan has 18 buildings. FEMA's line cuts through the car park. Which leases need the flood notice, and how much of each building is actually insurable?"

**What they do today and what it costs.**
- Property Code 92.0135 requires a written notice if the dwelling is in a 100-year floodplain or flooded within five years. The only remedy is that a tenant with a substantial flood loss may terminate; there is no fine. No compliance data was found.
- Flood determinations are bought per parcel. Elevation certificates cost roughly $500–800 in Houston (low-quality sources) and no open certificate dataset exists.
- An apartment building is NFIP "other residential", capped at $500,000 building coverage. Large buildings are underinsured by design.
- Harvey flooded an estimated 14,852 to about 43,000 apartment units depending on the source (ApartmentData.com; RealPage). The spread shows nobody has a building-level record.

**Open data.** NFHL layer 28 by polygon; MAAPnext status (draft, not usable for regulation); 3DEP ground elevation; FEMA damage-assessment points with depth; 311 Flooding and Drainage cases by account with dates (the "last five years" test); NFIP claims by block group for context; Atlas 14.

**Sponsor fields.**
- C: building footprints on the parcel, DSM and DTM (ground at each building corner against `STATIC_BFE`), oriented imagery from a named storm event collection (Harvey 2017), obliques for entry thresholds and ground-floor doors.
- A: unit counts by plan, `numStoriesAboveGrade`, available units and rents, year built.
- B: scans tied to plans; door `lowerElevation`; which scans are ground-floor is not flagged and must be inferred.

**Reasoning — where sources disagree.**
1. Effective NFHL (2007-era in Harris County) against Harvey observation against draft MAAPnext. The legal disclosure test uses the effective map plus actual flooding; the agent applies that and reports the others as risk, not as law.
2. Parcel centroid against building footprint: a building is "in" only if its footprint intersects the zone.
3. DTM ground against base flood elevation: a building inside the zone on fill may sit above it; the agent recommends an elevation certificate rather than asserting.
4. "Flooded in the last five years" has no dataset. 311 flooding cases and post-storm imagery are evidence, not proof; the agent asks the manager a direct question and records the answer.
5. Units per building is not in any source. Estimate from footprint area × stories ÷ average plan size and say it is an estimate.

**Action at the end.** (a) A per-building flood schedule; (b) pre-filled lease flood notices for the affected buildings, ready for both signatures; (c) a list of buildings where an elevation certificate would likely pay for itself; (d) a per-building coverage-gap table to send to the insurance broker.

**Worked example (illustrative).** A 300-unit community beside Brays Bayou: 6 of 16 footprints intersect zone AE; DTM puts 2 of those above base flood elevation by a small margin; Harvey imagery shows standing water at 9 buildings; three 311 flooding cases since 2022 at the same account. Output: notices for 6 buildings by law, a recommendation to disclose for 3 more, certificates suggested for 2, and a coverage gap for each two-storey building whose estimated replacement cost exceeds $500,000.

**Build effort.**
| Piece | Hours |
|---|---|
| Vexcel footprints per parcel, newest-collection choice, sanity checks | 5 |
| NFHL polygon intersect per footprint | 3 |
| DTM/3DEP ground elevation vs base flood elevation | 4 |
| Harvey imagery retrieval and standing-water read | 5 |
| 311 flooding history by account | 2 |
| Unit estimate per building, coverage-gap table | 3 |
| Notice and schedule generation | 4 |
| Rehearsal | 2 |

**Hardest part.** Reading water in the Harvey imagery reliably, and whether that collection covers the chosen property at peak water rather than days later.

**Cheapest check that would kill it.** Query NFHL at the kit's Houston multifamily coordinates and count those in a special flood hazard area; then request the Harvey collection at five of them. If fewer than about 50 are in the zone or the Harvey frames show dry ground, the demo has no subject. One to two hours.

---

### 4. P4 — Voucher unit matching with a rent-reasonableness file

**Problem in the owner's words.** Voucher holder: "I have a deadline to find a unit under my payment standard, and landlords can legally say no." Housing authority: "For every tenancy I must document that the rent is reasonable against comparable unassisted units."

**What they do today and what it costs.**
- Texas bars cities from protecting voucher holders from refusal (SB 267, 2015).
- HHA serves about 19,000 voucher households and uses ZIP-level payment standards (FY2026 plan; site not loadable today, UNVERIFIED).
- Rent reasonableness is done from purchased comparables databases or staff surveys; cost not sourced. HHA's voucher success rate was not found.

**Open data.** HUD Small Area FMR by ZIP and bedroom count; vouchers by tract (where vouchers are already accepted); ACS rent distributions; HISD zones and TEA ratings; METRO stops and frequencies; HPD crime; LIHTC list (LIHTC owners may not refuse vouchers *(from memory)*).

**Sponsor fields.**
- A: `apartmentModels[]` rents by plan, `numUnitsAvailable`, bedroom and bath counts, plan SF, `propertyManagementCompanyName`, year built, class.
- B: measured room areas and bedroom classification (is the advertised second bedroom a room with a door and a window?), door widths for mobility needs.
- C: site condition (roof defects, debris) as a predictor of failing the initial inspection.

**Reasoning — where sources disagree.**
1. Payment standard covers rent plus utilities; kit rents exclude utilities. The agent must subtract a utility allowance and state the figure used.
2. Advertised bedroom count against the scan: a den marketed as a bedroom changes the applicable standard.
3. A unit under the standard in a tract with zero vouchers suggests refusal; LIHTC status or existing vouchers in the tract raise the odds. The agent ranks by likelihood and says it is a guess.
4. Comparables for the authority must be unassisted and similar; the agent excludes LIHTC and HUD-assisted properties using the HUD layers.

**Action at the end.** For the tenant: a shortlist and a drafted inquiry to each manager. For the authority: a rent-reasonableness memo with three comparable unassisted units, measured size, and the determination, ready to attach to the tenancy file.

**Worked example (illustrative).** A two-bedroom voucher in a southwest ZIP: of the plans with availability under the standard after the utility allowance, the scan shows one "2BR" has an interior room without a window; four communities remain; two sit in tracts with existing vouchers; one has a persistent roof tarp. Three inquiries drafted.

**Build effort.**
| Piece | Hours |
|---|---|
| SAFMR token, ZIP join, utility allowance table | 3 |
| Plan-level filter and availability | 3 |
| Scan bedroom and area verification on linked plans | 6 |
| HUD layers for assisted/LIHTC exclusion and tract voucher counts | 3 |
| Site condition from Vexcel | 3 |
| Comparable selection and memo | 5 |
| Shortlist, inquiry drafts, rehearsal | 5 |

**Hardest part.** The share of floor plans with a linked scan that has room classification is uncounted.

**Cheapest check that would kill it.** Pull FY2026 two-bedroom SAFMRs for the ZIPs of the kit's Houston communities with rents and count plans under the standard with units available. If the count is near zero, or all are in a few ZIPs, there is nothing to match. One hour once the token arrives.

---

## Gap-closers worth keeping whatever idea is built

- **NAICS for tenants:** sales tax permits carry `outlet_naics_code` per outlet address.
- **Tenant revenue:** monthly mixed-beverage receipts per licensed location.
- **Traffic counts:** TxDOT AADT with history to 2006.
- **Assessed values and ownership:** HCAD roll, plus the mailing address of the owner of record.
- **Demographics:** ACS by block group; jobs by block from LODES.
- **Hazards:** NFHL, 3DEP, hail grids, Atlas 14.
- **Complaints:** 311 by HCAD account.
