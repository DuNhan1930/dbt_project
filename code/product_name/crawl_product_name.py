import requests
import json
import re
import time
import random
from time import sleep
from collections import OrderedDict
from collections import defaultdict
from pathlib import Path

input_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped.jsonl')
output_file = Path('/media/dunhan/Extreme SSD/Glamira_Data/product_name.jsonl')

success_count = 0
null_count = 0
total_lines = 0
log_every = 10

# Currency symbol ➝ ISO 4217 code mapping
CURRENCY_SYMBOLS_TO_ISO = {
    "£": "GBP",
    "€": "EUR",
    "$": "USD",
    "Kr": "SEK",
    "CHF": "CHF",
    "¥": "JPY",
    "₫": "VND",
    "₹": "INR",
    "₩": "KRW",
    "₽": "RUB",
    "AED": "AED",
    "CAD": "CAD",
    "AUD": "AUD"
    # Add more if needed
}

def extract_price_and_currency(price_str):
    cleaned = price_str.replace(",", "").replace(" ", "").strip()
    match = re.match(r"([^\d.,]*)([\d.]+)([^\d.,]*)", cleaned)
    if match:
        currency_before = match.group(1).strip()
        currency_after = match.group(3).strip()
        number = match.group(2)
        symbol = currency_before or currency_after
        iso_code = CURRENCY_SYMBOLS_TO_ISO.get(symbol, symbol)
        try:
            price = float(number)
        except ValueError:
            price = None
        return price, iso_code
    return None, None

start_time = time.time()

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        total_lines += 1
        print(total_lines)
        final_data = None  # Reset per product
        try:
            record = json.loads(line.strip())
            product_id = record.get('product_id')
            collections = record.get('collections')
            print(product_id)
            tlds = record.get('current_url', {})

            # Insert
            final_data = OrderedDict()
            final_data["product_id"] = product_id
            final_data["collections"] = collections

            for tld in tlds:
                print(tld)
                urls = tlds.get(tld, [])
                url_sample = urls if len(urls) <= 15 else random.sample(urls, 15)
                tld_grouped = defaultdict(dict)
                for url in url_sample:
                    try:
                        response = requests.get(url, timeout=5)
                        print(url)
                        print("Status Code:", response.status_code)
                        if response.status_code == 200:
                            html_text = response.text
                            match = re.search(r"var\s+react_data\s*=\s*(\{.*?\});", html_text, re.DOTALL)
                            if match:
                                react_data = json.loads(match.group(1))
                                print("Successfully extracted react_data")

                                start_key = "name"
                                end_key = "quick_options"
                                extract = OrderedDict()
                                copying = False

                                for key, value in react_data.items():
                                    if key == start_key:
                                        copying = True
                                    if copying:
                                        if key in {"price", "min_price", "max_price", "gold_weight"}:
                                            try:
                                                extract[key] = float(value)
                                            except:
                                                extract[key] = None
                                        else:
                                            extract[key] = value
                                    if key == end_key:
                                        break

                                # Extract currency
                                currency = None
                                if "max_price_format" in react_data:
                                    _, currency = extract_price_and_currency(react_data["max_price_format"])
                                elif "min_price_format" in react_data:
                                    _, currency = extract_price_and_currency(react_data["min_price_format"])

                                for key, value in extract.items():
                                    tld_grouped[key] = value
                                    if key == "max_price" and currency:
                                        tld_grouped["currency"] = currency

                                tld_grouped["media_image"] = react_data.get("media_image", {}).get("images", [])

                                required_keys = {"name", "price", "min_price", "max_price"}
                                if required_keys.issubset(tld_grouped.keys()):
                                    final_data[tld] = tld_grouped
                                    break  # Only break if all required fields are satisfied
                            else:
                                print("Variable 'react_data' not found in HTML.")
                        else:
                            print("Invalid status code:", response.status_code)
                    except requests.RequestException as e:
                        print("Request error:", e)
                        continue
            # Success check based on required keys
            required_keys = {"name", "price", "min_price", "max_price"}

            # Only one TLD needs to be complete
            has_success = False
            for tld, data in final_data.items():
                if tld in ("product_id", "collections"):
                    continue
                if required_keys.issubset(data.keys()):
                    has_success = True
                    break  

            if has_success:
                success_count += 1
                outfile.write(json.dumps(final_data, ensure_ascii=False) + '\n')
                print("Write success")
            else:
                null_count += 1
                print(f"[{total_lines}] No TLD block has all required fields.")

            if total_lines % log_every == 0:
                print(f"[{total_lines}] Processed. Success: {success_count}, Null: {null_count}")

        except json.JSONDecodeError as e:
            print(f"[{total_lines}] JSON decode error: {e}")
            null_count += 1
        except Exception as e:
            print(f"[{total_lines}] Unexpected error: {e}")
            null_count += 1

        sleep(random.uniform(0.3, 1.5))  # Sleep to avoid being blocked

print("\n Done! Product data has been saved.")
print(f"Total lines: {total_lines}, Success: {success_count}, Null: {null_count}")
print(f"Runtime: {time.time() - start_time:.2f} seconds")
