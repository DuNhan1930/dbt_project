import json
from collections import defaultdict
from pathlib import Path

input_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/filtered_products_1.json')
output_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/filtered_grouped_1.json')

# Using defaultdict to store sets for URLs and collections
grouped_data = defaultdict(lambda: {"current_url": set(), "collection": set()})

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            record = json.loads(line)
            pid = record.get('product_id')
            url = record.get('current_url')
            collection = record.get('collection')

            if pid and url and collection:
                grouped_data[pid]["current_url"].add(url)
                grouped_data[pid]["collection"].add(collection)

        except json.JSONDecodeError:
            print("Skipping invalid JSON line.")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Convert sets to lists and prepare output
with open(output_file, 'w', encoding='utf-8') as out:
    for pid, data in grouped_data.items():
        out.write(json.dumps({
            "product_id": pid,
            "current_url": list(data["current_url"]),
            "collection": list(data["collection"])
        }, ensure_ascii=False) + '\n')

print(f"Done. Grouped data written to: {output_file}")
