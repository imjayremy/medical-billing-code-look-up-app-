import csv
import os

CSV_PATH = os.path.join("data", "hcpcs_alpha.csv")

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print("CSV headers:", headers)
