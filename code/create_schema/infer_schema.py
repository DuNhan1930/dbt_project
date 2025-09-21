import json
from collections import defaultdict, Counter
from pathlib import Path
import time

input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary_final.jsonl")
output_schema_file = input_file.with_name("schema_summary.json")
max_lines = None  # Set to None to scan entire file, or set to a number for testing
print_limit = None  # Limit printed types per field
print_progress_every = 100000  # Log progress every N lines

field_type_counter = defaultdict(Counter)

# Recursive flattening
def flatten_json(y, prefix=""):
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            full_key = f"{prefix}.{k}" if prefix else k
            out.update(flatten_json(v, full_key))
    elif isinstance(y, list):
        for i, item in enumerate(y):
            full_key = f"{prefix}[]"  # Normalize list key
            out.update(flatten_json(item, full_key))
    else:
        out[prefix] = y
    return out

# Type Mapping to BigQuery
def to_bq_type(py_types):
    if "list" in py_types:
        return "REPEATED", "RECORD"
    if "dict" in py_types:
        return "RECORD", None
    if "float" in py_types:
        return "FLOAT"
    if "int" in py_types:
        return "INTEGER"
    if "bool" in py_types:
        return "BOOLEAN"
    if "str" in py_types:
        return "STRING"
    return "STRING"

# Scan the file
start = time.time()
line_count = 0
print(f"[Start] Scanning: {input_file}")

with input_file.open("r", encoding="utf-8") as f:
    for line in f:
        line_count += 1
        try:
            obj = json.loads(line.strip())
            flat = flatten_json(obj)
            for field, value in flat.items():
                type_name = type(value).__name__
                field_type_counter[field][type_name] += 1
        except Exception as e:
            print(f"[Warning] Error at line {line_count}: {e}")
            continue

        if line_count % print_progress_every == 0:
            print(f"[Progress] {line_count} lines scanned in {time.time() - start:.2f}s")

        if max_lines and line_count >= max_lines:
            break

# Build BigQuery Schema
bq_schema = []
for field, types in sorted(field_type_counter.items()):
    py_types = list(types.keys())
    mode = "NULLABLE"
    if "NoneType" in py_types:
        py_types.remove("NoneType")
    if "list" in py_types:
        mode = "REPEATED"
    bq_type = to_bq_type(py_types)
    if isinstance(bq_type, tuple):
        mode, bq_type = bq_type
    bq_schema.append({
        "name": field,
        "type": bq_type,
        "mode": mode
    })

# Write Schema
with output_schema_file.open("w", encoding="utf-8") as f:
    json.dump(bq_schema, f, indent=2)
print(f"\nBigQuery schema saved to: {output_schema_file}")

# Print Type Summary 
print("\n================= FLATTENED FIELD REPORT =================")
print(f"Total lines processed: {line_count}")
for field, type_counts in sorted(field_type_counter.items()):
    if print_limit and len(type_counts) > print_limit:
        type_counts = dict(list(type_counts.items())[:print_limit])
    print(f"- {field}: {dict(type_counts)}")

print(f"\n[Done] Runtime: {time.time() - start:.2f} seconds")
