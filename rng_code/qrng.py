import requests
import csv
import json
import os
import time
from datetime import datetime

API_URL = "https://api.quantumnumbers.anu.edu.au"
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

ARRAY_SIZE = 1024
MAX_REQUESTS = 100
REQUEST_DELAY = 1.05  # seconds (safe buffer)

HEADERS = {"x-api-key": API_KEY}

RAW_CSV = "raw_qrng_logs.csv"
CONCAT_CSV = "concatenated_qrng.csv"
JSON_LOG = "api_request_logs.json"


def fetch_uint16():
    params = {"length": ARRAY_SIZE, "type": "uint16"}
    response = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data.get("success", False):
        raise RuntimeError("API returned success = false")

    return data["data"]


def append_raw_csv(values, timestamp):
    exists = os.path.exists(RAW_CSV)
    with open(RAW_CSV, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["uint16", "binary", "timestamp"])
        for v in values:
            w.writerow([v, f"{v:016b}", timestamp])


def concatenate_uint64(values, timestamp):
    out = []
    for i in range(0, len(values), 4):
        chunk = values[i:i+4]
        if len(chunk) < 4:
            break
        binary = "".join(f"{v:016b}" for v in chunk)
        out.append((int(binary, 2), binary, timestamp))
    return out


def append_concat_csv(rows):
    exists = os.path.exists(CONCAT_CSV)
    with open(CONCAT_CSV, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["number", "binary", "timestamp"])
        w.writerows(rows)


def append_json_log(entry):
    if os.path.exists(JSON_LOG):
        with open(JSON_LOG, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(JSON_LOG, "w") as f:
        json.dump(logs, f, indent=2)


def main():
    print("Starting QRNG automation (safe mode)…")

    for request_number in range(1, MAX_REQUESTS + 1):
        timestamp = datetime.utcnow().isoformat()

        try:
            uint16_values = fetch_uint16()

            append_raw_csv(uint16_values, timestamp)

            uint64_rows = concatenate_uint64(uint16_values, timestamp)
            append_concat_csv(uint64_rows)

            append_json_log({
                "timestamp": timestamp,
                "request_number": request_number,
                "length": ARRAY_SIZE,
                "type": "uint16",
                "generated": {
                    "uint16": len(uint16_values),
                    "uint64": len(uint64_rows)
                },
                "status": "success"
            })

            print(f"Request {request_number} successful")

            time.sleep(REQUEST_DELAY)

        except Exception as e:
            append_json_log({
                "timestamp": timestamp,
                "request_number": request_number,
                "status": "failed",
                "error": str(e)
            })

            print(f"Stopping early — failure on request {request_number}")
            break

    print("Automation finished safely.")


if __name__ == "__main__":
    main()
