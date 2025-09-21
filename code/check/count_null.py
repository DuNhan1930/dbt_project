import json
from pathlib import Path


input_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/product_name_test.json')

null_count = 0
not_null_count = 0
total_lines = 0

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
            total_lines += 1
            if record.get("product_name") is None:
                null_count += 1
            else:
                not_null_count += 1
        except json.JSONDecodeError:
            print("Skipping invalid JSON line")

print("Total records:", total_lines)
print("product_name is NULL:", null_count)
print("product_name is NOT NULL:", not_null_count)
