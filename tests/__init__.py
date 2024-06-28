import vcr

omni_vcr = vcr.VCR(
    cassette_library_dir="cassettes",
    record_mode="once",
    match_on=["uri", "method"],
    filter_headers=["authorization"],
)
