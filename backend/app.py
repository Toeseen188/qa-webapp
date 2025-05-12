import os
from flask import Flask
from flask_cors import CORS
from routes import register_routes


# initialize flask app
app = Flask(__name__)
CORS(app)

# Create folder path
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Allow only PDf and Docx files
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register route
register_routes(app)


# Run app
if __name__== '__main__':
    app.run(debug=True)
