import json
from pathlib import Path

# Define target collections
TARGET_COLLECTIONS = {
    'product_view_all_recommend_clicked'
}

input_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/summary.json')
output_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/filtered_products_2.json')

count = 0  # Counter for matched records

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        try:
            record = json.loads(line)

            collection = record.get('collection')
            if collection in TARGET_COLLECTIONS:
                product_id = record.get('viewing_product_id')
                current_url = record.get('referrer_url')

                if product_id and current_url:
                    filtered = {
                        'product_id': product_id,
                        'current_url': current_url,
                        'collection': collection
                    }
                    outfile.write(json.dumps(filtered, ensure_ascii=False) + '\n')
                    count += 1
                    print(count)

        except json.JSONDecodeError:
            print("Skipping invalid JSON line.")
        except Exception as e:
            print(f"Unexpected error: {e}")

print(f"\nDone. Total matching records written: {count}")
