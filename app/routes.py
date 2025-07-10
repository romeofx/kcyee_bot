import os
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from .chatbot import get_response

# Optional: Install these libraries
from PyPDF2 import PdfReader
from docx import Document

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_response(user_input)
    return jsonify({'response': response})

@main.route('/upload', methods=['POST'])
def upload():
    if 'document' not in request.files:
        return jsonify({'response': '❌ No file uploaded.'}), 400

    file = request.files['document']

    if file.filename == '':
        return jsonify({'response': '❌ No selected file.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            ext = filename.rsplit('.', 1)[1].lower()
            extracted_text = ""

            if ext == 'pdf':
                extracted_text = extract_text_from_pdf(filepath)
            elif ext == 'docx':
                extracted_text = extract_text_from_docx(filepath)
            elif ext == 'txt':
                with open(filepath, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()

            if not extracted_text.strip():
                return jsonify({'response': '❌ No readable content found in the document.'})

            # Analyze text using AI
            result = get_response(f"Analyze this document:\n\n{extracted_text[:3000]}")
            return jsonify({'response': result})

        except Exception as e:
            return jsonify({'response': f'❌ Error processing file: {str(e)}'}), 500

    return jsonify({'response': '❌ Invalid file type. Only PDF, DOCX, or TXT allowed.'}), 400

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(filepath):
    text = ""
    doc = Document(filepath)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
