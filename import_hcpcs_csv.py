import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "codes.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS hcpcs (
    code TEXT PRIMARY KEY,
    short_desc TEXT,
    long_desc TEXT
)
""")
conn.commit()

# Load CSV starting from row 20
csv_path = os.path.join("data", "hcpcs_alpha.csv")
df = pd.read_csv(csv_path, header=19)  # header=19 → row 20 in Excel (0-indexed)

# Grab only the columns you need by position
codes = df.iloc[:, 0]      # Column A
shorts = df.iloc[:, 2]     # Column C
longs = df.iloc[:, 3]      # Column D

count = 0
for code, short, long in zip(codes, shorts, longs):
    code = str(code).strip()
    short = str(short).strip()
    long = str(long).strip()
    if code and short:
        c.execute("INSERT OR REPLACE INTO hcpcs (code, short_desc, long_desc) VALUES (?, ?, ?)",
                  (code, short, long))
        count += 1

conn.commit()
conn.close()
print(f"✅ Imported {count} HCPCS codes into '{DB_PATH}'")

