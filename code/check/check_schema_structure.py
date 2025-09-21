import json
from collections import defaultdict, Counter
from pathlib import Path
import time

input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary_cleaned.jsonl")  
max_lines = None  
print_limit = None  
print_progress_every = 100000 

# Result
field_type_counter = defaultdict(Counter)

def flatten_json(y, prefix=""):
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            full_key = f"{prefix}.{k}" if prefix else k
            out.update(flatten_json(v, full_key))
    elif isinstance(y, list):
        for i, item in enumerate(y):
            full_key = f"{prefix}[{i}]"
            out.update(flatten_json(item, full_key))
    else:
        out[prefix] = y
    return out

start = time.time()
line_count = 0
print(f"[Start] Scanning file: {input_file}")

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
            print(f"[Warning] JSON decode error at line {line_count}: {e}")
            continue

        if line_count % print_progress_every == 0:
            elapsed = time.time() - start
            print(f"[Progress] {line_count} lines scanned in {elapsed:.2f}s")

        if max_lines and line_count >= max_lines:
            break

print("\n================= FLATTENED FIELD REPORT =================")
print(f"Total lines processed: {line_count}")

for field, type_counts in sorted(field_type_counter.items()):
    if print_limit and len(type_counts) > print_limit:
        type_counts = dict(list(type_counts.items())[:print_limit])
    print(f"- {field}: {dict(type_counts)}")

print("\n[Done] Runtime: {:.2f}s".format(time.time() - start))

print("\n================= FIELDS WITH MULTIPLE DATA TYPES (Excluding NoneType) =================")

for field, type_counts in sorted(field_type_counter.items()):
    # Remove NoneType for comparison
    filtered_types = {t for t in type_counts if t != "NoneType"}
    if len(filtered_types) > 1:
        print(f"- {field}: {dict(type_counts)}")
