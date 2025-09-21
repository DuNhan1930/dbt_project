import json
from collections import defaultdict
from pathlib import Path


# Input files
file1 = Path("/media/dunhan/Extreme SSD/Glamira_Data/filtered_grouped_1.json")
file2 = Path("/media/dunhan/Extreme SSD/Glamira_Data/filtered_grouped_2.json")

# Output file
output_file = "/media/dunhan/Extreme SSD/Glamira_Data/filtered_grouped.json"

# Use a dict to store merged data by product_id
merged = defaultdict(lambda: {"current_url": set(), "collection": set()})

# Function to load and merge a file into the merged dict
def merge_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            pid = data["product_id"]
            merged[pid]["current_url"].update(data.get("current_url", []))
            merged[pid]["collection"].update(data.get("collection", []))

# Merge both files
merge_file(file1)
merge_file(file2)

# Write merged result to output
with open(output_file, "w", encoding="utf-8") as out:
    for pid, values in merged.items():
        out.write(json.dumps({
            "product_id": pid,
            "current_url": list(values["current_url"]),
            "collection": list(values["collection"])
        }, ensure_ascii=False) + '\n')

print(f"Merged file saved to: {output_file}")
