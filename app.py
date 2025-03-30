import os
import io
import easyocr
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize EasyOCR reader with multiple languages
reader = easyocr.Reader(["en", "hi", "ta", "te", "kn", "mr", "gu", "bn"])  # Add more languages if needed

@app.route("/")
def home():
    return "📝 Handwriting to Text API is Running!"

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Secure the filename
    filename = secure_filename(file.filename)
    
    # Convert file to an image
    image = Image.open(io.BytesIO(file.read()))

    # Process with EasyOCR
    extracted_text = reader.readtext(image, detail=0)  # Extract text without bounding box details

    return jsonify({"text": " ".join(extracted_text)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the PORT from environment variables
    app.run(host="0.0.0.0", port=port)  # Bind to all network interfaces
