from pathlib import Path

input_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped.jsonl')

def count_json_lines(file_path):
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for _ in f:
            count += 1
    return count

if __name__ == "__main__":
    try:
        total_lines = count_json_lines(input_file)
        print(f"Total number of lines in '{input_file}': {total_lines}")
    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
