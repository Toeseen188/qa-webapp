import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename


# initialize flask app
app = Flask(__name__)
CORS(app)

# create upload folder path
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow only PDf and Docx files
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """ check if file is PDF Or Docx """
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


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



if __name__== '__main__':
    app.run(debug=True)
