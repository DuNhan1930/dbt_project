import json
from pathlib import Path


input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name_1_single.json")

# Read and print first 10 JSON lines
with open(input_file, "r") as f:
    print("\nFirst 10 IP location records:")
    for i, line in enumerate(f):
        if i >= 10:
            break
        try:
            record = json.loads(line)
            print(record)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Line {i+1} is not valid JSON: {e}")
