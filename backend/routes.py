import os
import pdfplumber
from flask import request, jsonify
from werkzeug.utils import secure_filename
from docx import Document


def extract_text_from_file(filepath):
    """
    Extract text from a PDF file using pdfplumber
    """
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(filepath):
    """
    Extract text from Docx file using python-docx
    """
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])



def allowed_file(filename):
    """ check if file is PDF Or Docx """
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def register_routes(app):

    @app.route('/')
    def home():
        """ simple route to test if server is running """
        return{"message": "Backend is running"}

    @app.route('/upload', methods=['POST'])
    def upload_file():
        """
        Admin uploads a file.
        The file is saved in the uploads directory if valid
        """
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']

        # if file is empty
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # if file is found and file extension is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"message": f"File '{filename}' uploaded successfully"}), 200
        else:
            return jsonify({"error": "Unsupported file type"}), 400
