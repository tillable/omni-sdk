import json


def compact_json_dump(data: dict) -> str:
    """Dumps a dictionary to a JSON string with no extra whitespace."""
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    )
