import json
import re
from pathlib import Path
from typing import Any, Dict

input_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary.json")
output_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary_final.jsonl")
log_every = 100000

# Helper functions for type conversions
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

# Step 1: Flatten _id.oid → _id
def normalize_id_field(record: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(record.get("_id"), dict):
        oid = record["_id"].get("$oid")
        if oid:
            record["_id"] = oid
    return record

# Step 2: Convert $numberInt recursively
def convert_numberint(obj):
    if isinstance(obj, dict):
        if "$numberInt" in obj:
            val = obj["$numberInt"]
            if isinstance(val, str) and re.match(r"^0\d+", val):
                raise ValueError(f"Leading-zero $numberInt: {val}")
            return int(val)
        return {k: convert_numberint(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numberint(item) for item in obj]
    else:
        return obj

# Step 3: Convert $numberDouble recursively
def convert_numberfloat(obj):
    if isinstance(obj, dict):
        if "$numberDouble" in obj:
            val = obj["$numberDouble"]
            if isinstance(val, str) and re.match(r"^0\d+", val):
                raise ValueError(f"Leading-zero $numberDouble: {val}")
            return float(val)
        return {k: convert_numberfloat(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numberfloat(item) for item in obj]
    else:
        return obj

# Step 4: Final custom clean
def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(record.get("order_id"), str):
        record["order_id"] = None

    if isinstance(record.get("recommendation_product_position"), str):
        if record["recommendation_product_position"] == "":
            record["recommendation_product_position"] = None
        else:
            record["recommendation_product_position"] = to_int(record["recommendation_product_position"])

    if isinstance(record.get("utm_medium"), bool):
        record["utm_medium"] = None

    if isinstance(record.get("utm_source"), bool):
        record["utm_source"] = None

    if "cart_products" in record and isinstance(record["cart_products"], list):
        for option in record["cart_products"]:
            if "option" in option:
                if isinstance(option["option"], str):
                    option["option"] = None
    return record

# MAIN PIPELINE
total_lines = 0
written_lines = 0
skipped_lines = 0

with input_path.open("r", encoding="utf-8") as infile, output_path.open("w", encoding="utf-8") as outfile:
    for line in infile:
        total_lines += 1
        try:
            record = json.loads(line.strip())

            # Step-by-step processing
            record = normalize_id_field(record)
            record = convert_numberint(record)
            record = convert_numberfloat(record)
            record = clean_record(record)

            json.dump(record, outfile, ensure_ascii=False)
            outfile.write('\n')
            written_lines += 1
        except (ValueError, json.JSONDecodeError) as e:
            skipped_lines += 1
            print(f"[Skip] Line {total_lines} - {e}")
        except Exception as e:
            skipped_lines += 1
            print(f"[Error] Line {total_lines} - Unexpected error: {e}")

        if total_lines % log_every == 0:
            print(f"[Progress] {total_lines} lines | {written_lines} written | {skipped_lines} skipped")

# Summary
print(f"\nCompleted")
print(f"Total lines processed: {total_lines}")
print(f"Written lines: {written_lines}")
print(f"Skipped lines: {skipped_lines}")
