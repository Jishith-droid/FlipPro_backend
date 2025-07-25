from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "flippro-files"
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

@app.route('/')
def index():
    return "FlipPro Backend is Live!"


@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files.get('pdf')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/pdf"
    }

    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{filename}"

    response = requests.post(url, headers=headers, data=file.read())

    if response.status_code in [200, 201]:
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}"
        return jsonify({"message": "Uploaded!", "url": public_url})
    else:
        return jsonify({"error": "Upload failed", "details": response.text}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")