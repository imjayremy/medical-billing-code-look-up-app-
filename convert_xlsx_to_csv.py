import pandas as pd
import os

xlsx_path = "/Users/Remy/Desktop/HCPC2020_TRANS_ALPHA_w_disclaimer.xlsx"
csv_dir = "data"
csv_path = os.path.join(csv_dir, "hcpcs_alpha.csv")

# Make sure data/ exists
os.makedirs(csv_dir, exist_ok=True)

# Load Excel
df = pd.read_excel(xlsx_path)

# Save CSV
df.to_csv(csv_path, index=False)
print(f"✅ Converted {xlsx_path} → {csv_path}")

