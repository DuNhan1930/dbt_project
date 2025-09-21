import json
import re
import time
from pathlib import Path
from typing import Any, Dict
from collections import defaultdict, Counter

INPUT_PATH  = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary.json")     
OUTPUT_JSONL = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary_final.jsonl")
OUTPUT_SCHEMA = OUTPUT_JSONL.with_name("schema_summary.json")
LOG_EVERY = 100000  # progress log step

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

# Step 1: _id.$oid -> _id
def normalize_id_field(record: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(record.get("_id"), dict):
        oid = record["_id"].get("$oid")
        if oid:
            record["_id"] = oid
    return record

# Step 2: {"$numberInt": "..."} -> int
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

# Step 3: {"$numberDouble": "..."} -> float(...)
def convert_numberdouble(obj):
    if isinstance(obj, dict):
        if "$numberDouble" in obj:
            val = obj["$numberDouble"]
            if isinstance(val, str) and re.match(r"^0\d+", val):
                raise ValueError(f"Leading-zero $numberDouble: {val}")
            return float(val)
        return {k: convert_numberdouble(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numberdouble(item) for item in obj]
    else:
        return obj

# Step 4: Custom cleans
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
                elif not isinstance(option["option"], list):
                    option["option"] = None
    return record

# Flatten for schema typing - arrays noted as field[] to normalize element types
def flatten_json(y: Any, prefix: str = "") -> Dict[str, Any]:
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            full_key = f"{prefix}.{k}" if prefix else k
            out.update(flatten_json(v, full_key))
    elif isinstance(y, list):
        # represent all list elements under the same key with [] suffix
        full_key = f"{prefix}[]"
        if not y:
            # empty list → still record the list existence for schema inference
            out[full_key] = []
        else:
            for item in y:
                out.update(flatten_json(item, full_key))
    else:
        out[prefix] = y
    return out

# Map Python types to BQ
def to_bq_type(py_types):
    if "list" in py_types:
        # arrays become REPEATED RECORD if nested objects were observed,
        # otherwise REPEATED of scalar; we’ll mark type as RECORD and mode REPEATED,
        # which is safest; downstream can refine if needed.
        return ("REPEATED", "RECORD")
    if "dict" in py_types:
        return ("NULLABLE", "RECORD")
    if "float" in py_types:
        return ("NULLABLE", "FLOAT")
    if "int" in py_types:
        return ("NULLABLE", "INTEGER")
    if "bool" in py_types:
        return ("NULLABLE", "BOOLEAN")
    if "str" in py_types:
        return ("NULLABLE", "STRING")
    # default fallback
    return ("NULLABLE", "STRING")

# STREAMING PIPELINE
def main():
    total = 0
    written = 0
    skipped = 0

    # field -> Counter of python type names
    field_type_counter = defaultdict(Counter)

    start = time.time()
    print(f"[Start] Reading {INPUT_PATH} → writing {OUTPUT_JSONL}")

    with INPUT_PATH.open("r", encoding="utf-8") as infile, OUTPUT_JSONL.open("w", encoding="utf-8") as outfile:
        for raw in infile:
            total += 1
            line = raw.strip()
            if not line:
                continue
            try:
                record = json.loads(line)

                # 1) id normalize
                record = normalize_id_field(record)
                # 2) numeric conversions
                record = convert_numberint(record)
                record = convert_numberdouble(record)
                # 3) custom cleans
                record = clean_record(record)

                # write cleaned
                outfile.write(json.dumps(record, ensure_ascii=False) + "\n")
                written += 1

                # update schema counters on-the-fly
                flat = flatten_json(record)
                for field, value in flat.items():
                    t = type(value).__name__
                    field_type_counter[field][t] += 1

            except (ValueError, json.JSONDecodeError) as e:
                skipped += 1
                # comment out if too noisy
                print(f"[Skip] Line {total}: {e}")
            except Exception as e:
                skipped += 1
                print(f"[Error] Line {total}: {e}")

            if total % LOG_EVERY == 0:
                elapsed = time.time() - start
                print(f"[Progress] {total} lines | {written} written | {skipped} skipped | {elapsed:.1f}s")

    # Build BQ schema from counters
    bq_schema = []
    for field in sorted(field_type_counter.keys()):
        type_counts = field_type_counter[field]
        py_types = set(type_counts.keys())
        # drop NoneType if present (we represent nullability via mode)
        py_types.discard("NoneType")

        mode, bq_type = to_bq_type(py_types)
        bq_schema.append({
            "name": field,
            "type": bq_type,
            "mode": mode
        })

    with OUTPUT_SCHEMA.open("w", encoding="utf-8") as f:
        json.dump(bq_schema, f, indent=2, ensure_ascii=False)

    print("\n================ SUMMARY ================")
    print(f"Total lines processed: {total}")
    print(f"Written (cleaned) lines: {written}")
    print(f"Skipped lines: {skipped}")
    print(f"Clean JSONL: {OUTPUT_JSONL}")
    print(f"BigQuery schema: {OUTPUT_SCHEMA}")
    print(f"Elapsed: {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()
