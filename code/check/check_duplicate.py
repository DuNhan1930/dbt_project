import json
from collections import Counter
from pathlib import Path

input_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/product_name.json')

product_ids = []
check = 0
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        check += 1
        print(check)
        try:
            record = json.loads(line)
            product_id = record.get('product_id')
            if product_id is not None:
                product_ids.append(product_id)
        except json.JSONDecodeError:
            print("Skipping invalid JSON line.")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Count occurrences
counter = Counter(product_ids)

# Find duplicates
duplicates = {pid: count for pid, count in counter.items() if count > 1}

print(f"Total unique product_id: {len(counter)}")
print(f"Total duplicate product_id: {len(duplicates)}")
print(f"Examples of duplicate product_ids:")
for pid, count in list(duplicates.items()):
    print(f"  {pid}: {count} times")
