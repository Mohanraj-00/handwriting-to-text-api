from flask import Flask, request, jsonify
import easyocr
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Initialize EasyOCR reader with multiple languages
reader = easyocr.Reader(['en', 'ta', 'hi'])  # Add more languages as needed

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    language = request.form.get('language', 'en')  # Default language is English
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    # Perform OCR using EasyOCR
    try:
        result = reader.readtext(file_path, detail=0, paragraph=True)
        os.remove(file_path)  # Clean up after processing
        return jsonify({'text': ' '.join(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)  # Create upload folder if not exists
    app.run(debug=True)
