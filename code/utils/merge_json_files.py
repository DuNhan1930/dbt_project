import json
from pathlib import Path

file1_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name_1_single.json")
file2_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name_2_single.json")
output_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name.json")

# Load JSON Lines file
def load_jsonl_file(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid line in {path}: {e}")
    return records

# Load and merge
data1 = load_jsonl_file(file1_path)
data2 = load_jsonl_file(file2_path)
merged_data = data1 + data2

# Save merged output
with open(output_path, 'w', encoding='utf-8') as out:
    for item in merged_data:
        out.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Merged {len(data1)} + {len(data2)} records → {output_path}")
