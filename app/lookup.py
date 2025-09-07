import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "codes.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def lookup_by_code(code):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT code, short_desc, long_desc FROM hcpcs WHERE code = ?", (code,))
    result = c.fetchone()
    conn.close()
    return result

def search_hcpcs(term, limit=50):
    term = f"%{term}%"
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT code, short_desc, long_desc FROM hcpcs WHERE code LIKE ? OR short_desc LIKE ? OR long_desc LIKE ? LIMIT ?",
        (term, term, term, limit)
    )
    results = c.fetchall()
    conn.close()
    return results

# This is the new function for your main.py to import
def search_by_keyword(keyword, limit=50):
    return search_hcpcs(keyword, limit)

# ======= CLI block =======
if __name__ == "__main__":
    while True:
        user_input = input("Enter code or keyword to search (or 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue
        results = search_hcpcs(user_input)
        if results:
            print(f"Found {len(results)} results:\n")
            for code, short_desc, long_desc in results:
                print(f"{code} | {short_desc} | {long_desc}")
            print("\n" + "="*50 + "\n")
        else:
            print("No results found.\n")
