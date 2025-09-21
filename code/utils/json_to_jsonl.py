import json
from pathlib import Path

input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary.json")      # Replace with your JSON file path
output_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary.jsonl")   # Desired .jsonl output

def convert_json_to_jsonl(input_path, output_path):
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)  # Should be a list of dicts

    with output_path.open("w", encoding="utf-8") as out_f:
        for record in data:
            json.dump(record, out_f)
            out_f.write('\n')

    print(f"[Done] Converted {len(data)} records to {output_path}")

if __name__ == "__main__":
    convert_json_to_jsonl(input_file, output_file)
