from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import requests
import tempfile

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    pdf_url = data.get('pdf_url')
    if not pdf_url:
        return jsonify({'error': 'Missing pdf_url'}), 400

    response = requests.get(pdf_url)
    if response.status_code != 200:
        return jsonify({'error': 'Could not download PDF'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    result = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        result.append({'page': i + 1, 'text': text})
    return jsonify(result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
