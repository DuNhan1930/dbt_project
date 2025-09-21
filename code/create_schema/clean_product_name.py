from pathlib import Path
import json
from typing import Any, Dict
from collections import OrderedDict

input_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name.json")
output_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name_cleaned.jsonl")

# Helper functions for type conversions
def to_str(value):
    try:
        return str(value)
    except (ValueError, TypeError):
        return None

def to_int(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None

def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def to_none(_):
    return None

# Process a single record
def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(record.get("product_id"), str):
        record["product_id"] = to_str(record["product_id"])

    if isinstance(record.get("category"), str):
        record["category"] = to_int(record["category"])

    if isinstance(record.get("fixed_silver_weight"), int):
        record["fixed_silver_weight"] = float(record["fixed_silver_weight"])

    if isinstance(record.get("gender"), bool):
        record["gender"] = None

    if isinstance(record.get("none_metal_weight"), (int, str)):
        record["none_metal_weight"] = to_float(record["none_metal_weight"])

    if "quick_options" in record and isinstance(record["quick_options"], list):
        for option in record["quick_options"]:
            if "request_values" in option and isinstance(option["request_values"], list):
                for req in option["request_values"]:
                    if "optionPrice" in req and isinstance(req["optionPrice"], str):
                        req["optionPrice"] = to_int(req["optionPrice"])
                    if "value" in req and isinstance(req["value"], str):
                        req["value"] = to_int(req["value"])
    return record

# Read, clean, and write unique records
seen_ids = set()
output_lines = 0

with input_path.open("r", encoding="utf-8") as infile, output_path.open("w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            record = json.loads(line.strip())
            pid = record.get("product_id")
            if pid in seen_ids:
                continue
            seen_ids.add(pid)

            cleaned = clean_record(record)
            outfile.write(json.dumps(cleaned, ensure_ascii=False) + "\n")
            output_lines += 1
        except Exception as e:
            print(f"Error processing line: {e}")

print(output_lines, output_path.name)
