import json
import sys

def is_jsonl(file_path, sample_lines=2000000):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= sample_lines:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"[Line {i + 1}] Invalid JSON: {e}")
                    return False
        print(f"File '{file_path}' appears to be valid JSONL (checked up to {sample_lines} lines).")
        return True
    except Exception as e:
        print(f"Error reading file: {e}")
        return False


if __name__ == "__main__":
    file_path = "/media/dunhan/Extreme SSD/Glamira_Data/summary.json"
    is_jsonl(file_path)
