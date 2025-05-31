import os
import pdfplumber
from flask import request, jsonify
from werkzeug.utils import secure_filename
from docx import Document

ALLOWED_EXTENSIONS = {'pdf', 'docx'}


def extract_text_from_pdf(filepath):
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
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            return jsonify({"message":
                            f"File '{filename}' uploaded successfully"}), 200
        else:
            return jsonify({"error": "Unsupported file type"}), 400

    @app.route('/extract/<filename>', methods=['GET'])
    def extract_from_file_text(filename):
        """
        Extract text from files - PDF OR docx
        """
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        ext = filename.rsplit('.', 1)[-1].lower()

        try:
            if ext == 'pdf':
                text = extract_text_from_pdf(filepath)
            elif ext == 'docx':
                text = extract_from_docx(filepath)
            else:
                return jsonify({"error": "Unsuported file"}), 404

            return jsonify({
                "filename": filename,
                "text_preview": text[:1000]
                })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
