import json
import random
from pathlib import Path

# Input and output file paths
input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped.json")
output_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped_test.json")

sample_size = 10

# Load entire JSON array
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

total_records = len(data)
sampled = random.sample(data, min(sample_size, total_records))

# Write as JSON Lines (.jsonl)
with open(output_file, "w", encoding="utf-8") as f:
    for obj in sampled:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"Sampled {len(sampled)} records from {total_records} total into: {output_file}")
