import requests
from bs4 import BeautifulSoup
import json
import re
import time
import datetime
from collections import OrderedDict

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

url = "https://www.glamira.co.uk/glamira-men%27s-bracelet-aleen.html?alloy=white-silber&leather=red&stone1=diamond-Brillant"
output_file = "extracted_product_bs4.json"

start_time = time.time()

try:
    response = requests.get(url, timeout=5)
    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")

    react_data_json = None

    for script in scripts:
        if script.string and "var react_data" in script.string:
            match = re.search(r"var\s+react_data\s*=\s*(\{.*?\});", script.string, re.DOTALL)
            if match:
                react_data_json = match.group(1)
                break

    if react_data_json:
        react_data = json.loads(react_data_json)

        # Extract từ product_id đến quick_options
        start_key = "product_id"
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
                        extract[key] = value
                else:
                    extract[key] = value

                if key == "product_id":
                    extract["timestamp"] = int(time.time())

            if key == end_key:
                extract["url"] = url
                break

        # Tách currency từ min_price_format / max_price_format
        currency = None
        if "max_price_format" in react_data:
            _, currency = extract_price_and_currency(react_data["max_price_format"])
        elif "min_price_format" in react_data:
            _, currency = extract_price_and_currency(react_data["min_price_format"])

        final_data = OrderedDict()
        for key, value in extract.items():
            final_data[key] = value
            if key == "max_price" and currency:
                final_data["currency"] = currency

        # Lấy ảnh ví dụ từ media_image
        media_images = react_data.get("media_image", {}).get("images", [])
        final_data["media_image"] = media_images

        # Lưu kết quả
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)

        print(f"Đã lưu dữ liệu sản phẩm vào {output_file}")

    else:
        print("Không tìm thấy biến react_data.")

except requests.RequestException as e:
    print("Lỗi request:", e)

end_time = time.time()
print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
