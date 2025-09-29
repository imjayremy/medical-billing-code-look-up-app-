from flask import Flask, render_template, request, jsonify, send_file, session
import csv
import io
from urllib.parse import quote
from lookup import search_by_keyword, lookup_by_code  # <-- Import your lookup functions

app = Flask(__name__)
app.secret_key = "supersecret"  # Replace with a safe value in production


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            # Use lookup.py to search
            results = search_by_keyword(query)

        # Store results in session for export
        session['last_results'] = results

    return render_template('index.html', results=results)


@app.route('/export/csv')
def export_csv():
    if 'last_results' not in session or not session['last_results']:
        return "No results to export", 400

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Code', 'Short Description', 'Long Description'])

    # Write data
    for result in session['last_results']:
        writer.writerow([result[0], result[1], result[2]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='hcpcs_codes.csv'
    )


@app.route('/share/<code>')
def share_code(code):
    code_data = None
    if 'last_results' in session:
        for result in session['last_results']:
            if result[0] == code:
                code_data = {
                    'code': result[0],
                    'short_desc': result[1],
                    'long_desc': result[2]
                }
                break

    if not code_data:
        return "Code not found", 404

    message = f"HCPCS Code {code_data['code']}: {code_data['short_desc']}"
    encoded_message = quote(message)

    return jsonify({
        'slack': f"https://slack.com/intent/share?text={encoded_message}",
        'teams': f"https://teams.microsoft.com/share?href={request.host_url}?code={code}&msgText={encoded_message}",
        'message': message
    })


if __name__ == "__main__":
    app.run(debug=True)
