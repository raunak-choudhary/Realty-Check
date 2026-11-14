"""tools.kit: address matching against the CoStar kit index. Needs RC_PRIVATE_DIR (skips otherwise)."""
import os
import time

import pytest

from tools.kit.normalize import parse, street_key

needs_kit = pytest.mark.skipif(not os.environ.get("RC_PRIVATE_DIR"), reason="RC_PRIVATE_DIR not set")


# ---- pure normalization (no kit needed) ----

def test_parse_full_address():
    q = parse("2111 AUSTIN ST, HOUSTON, TX 77002-xxxx", ["houston"])
    assert (q["num_lo"], q["streets"][0], q["zip"], q["city"]) == (2111, "austin", "77002", "houston")


def test_parse_no_commas_and_unit():
    q = parse("2111 Austin Street #412 Houston TX", ["houston", "los angeles"])
    assert (q["num_lo"], q["streets"][0], q["zip"], q["city"], q["unit"]) == (2111, "austin", None, "houston", "412")


def test_parse_unit_first_does_not_become_zip():
    q = parse("Unit 141, 14020 Schroeder Road, Houston TX", ["houston"])
    assert (q["num_lo"], q["zip"], q["unit"]) == (14020, None, "141")


def test_street_key_peels_direction_and_type():
    assert street_key("S Sepulveda Blvd") == "sepulveda"
    assert street_key("Park Row") == "park"
    assert street_key("First Street") == "1st"


# ---- against the kit ----

@pytest.fixture(scope="module")
def kit():
    if not os.environ.get("RC_PRIVATE_DIR"):
        pytest.skip("RC_PRIVATE_DIR not set")
    from tools.kit import match_address, record_evidence
    match_address("warm up")  # loads (or builds) the index once
    return match_address, record_evidence


@needs_kit
def test_austin_matches_with_record(kit):
    match_address, record_evidence = kit
    m = match_address("2111 Austin St, Houston, TX 77002")
    assert m["status"] == "matched" and m["property_id"] == "10122224"
    assert m["record"]["stories"] == 5
    assert m["how"] == "street number + street name + zip" and m["confidence"] >= 0.9
    ev = record_evidence(m)
    assert ev["source"] == "record" and ev["status"] == "ok" and ev["observed"]["stories"] == 5
    assert set(ev["observed"]) <= {"stories", "year_built", "unit_count", "building_sf"}
    assert all(v is not None for v in ev["observed"].values())


@needs_kit
@pytest.mark.parametrize("text", ["2111 Austin Street Houston TX", "2111 AUSTIN ST, HOUSTON, TX 77002-8909",
                                  "2111 AUSTIN ST, HOUSTON, TX 77002-xxxx", "2111 Austin St #412",
                                  "2111 Austin St. Apt 412, Houston, Texas 77002"])
def test_variants_match_same_property(kit, text):
    m = kit[0](text)
    assert m["status"] == "matched" and m["property_id"] == "10122224", m


@needs_kit
def test_sepulveda_plan_e_two_beds(kit):
    m = kit[0]("3700 S Sepulveda Blvd, Los Angeles, CA 90034")
    assert m["status"] == "matched" and m["property_id"] == "5447229"
    plan_e = [f for f in m["floorplans"] if "E" in f["name"].split()]
    assert plan_e and plan_e[0]["name"] == "Plan E 1 Bedroom + Den" and plan_e[0]["beds"] == 2
    assert plan_e[0]["matterport_model_id"] in m["matterport_model_ids"]


@needs_kit
def test_no_match_never_guesses(kit):
    match_address, record_evidence = kit
    m = match_address("1 Nowhere Rd, Princeton, NJ")
    assert m["status"] == "no_match" and m["confidence"] == 0 and m["how"]
    assert record_evidence(m)["status"] == "no_evidence"


@needs_kit
def test_latlon_fallback_within_60m(kit):
    m = kit[0]("somewhere downtown", lat=29.7461, lon=-95.3679)
    assert m["status"] == "matched" and m["property_id"] == "10122224" and m["how"].startswith("nearest")
    assert kit[0]("somewhere", lat=40.35, lon=-74.66)["status"] == "no_match"


@needs_kit
def test_lookup_is_fast(kit):
    t = time.perf_counter()
    kit[0]("3700 Sepulveda Blvd Los Angeles CA")
    assert time.perf_counter() - t < 0.5


@needs_kit
def test_cold_load_from_existing_index_is_fast(kit):
    import tools.kit.match as km
    km._IDX = None
    t = time.perf_counter()
    m = kit[0]("2111 Austin St, Houston, TX 77002")
    assert m["status"] == "matched" and time.perf_counter() - t < 0.5
