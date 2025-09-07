from flask import Flask, render_template, request
from database import init_db
from lookup import lookup_by_code, search_hcpcs  # updated function name

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            results = search_hcpcs(query)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
