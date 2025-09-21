import json
from pathlib import Path
from typing import Any, Dict, List

input_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/schema_summary.json")        # Input: flattened schema format
output_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/nested_schema_summary.json")          # Output: nested schema format


def insert_nested(schema: List[Dict[str, Any]], path: List[str], field_type: str, mode: str):
    head = path[0].rstrip("[]")
    is_repeated = "[]" in path[0]

    # Find or create the field
    for field in schema:
        if field["name"] == head:
            if "fields" not in field:
                field["fields"] = []
            if is_repeated:
                field["mode"] = "REPEATED"
            break
    else:
        new_field = {
            "name": head,
            "type": "RECORD" if len(path) > 1 else field_type,
            "mode": "REPEATED" if is_repeated else mode,
        }
        if len(path) > 1:
            new_field["fields"] = []
        schema.append(new_field)
        field = new_field

    if len(path) > 1:
        insert_nested(field["fields"], path[1:], field_type, mode)
    else:
        field["type"] = field_type


def build_schema(flattened_fields: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    schema: List[Dict[str, Any]] = []
    for field in flattened_fields:
        parts = field["name"].split(".")
        insert_nested(schema, parts, field["type"], field["mode"])
    return schema


def main():
    with open(input_path, "r") as f:
        flattened_fields = json.load(f)

    nested_schema = build_schema(flattened_fields)

    with open(output_path, "w") as f:
        json.dump(nested_schema, f, indent=2)

    print(f"✅ Nested schema saved to {output_path}")


if __name__ == "__main__":
    main()
