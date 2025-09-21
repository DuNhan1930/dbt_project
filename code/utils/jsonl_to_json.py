import json
from pathlib import Path

input_file = Path("input.jsonl")     # Replace with your JSONL file path
output_file = Path("output.json")    # Desired output path

def convert_jsonl_to_json(input_path, output_path):
    data = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line.strip()))

    with output_path.open("w", encoding="utf-8") as out_f:
        json.dump(data, out_f, indent=4)

    print(f"[Done] Converted {len(data)} lines to {output_path}")

if __name__ == "__main__":
    convert_jsonl_to_json(input_file, output_file)
