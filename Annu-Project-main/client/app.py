from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
CORS(app)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=600)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def uploadedImage():
    print("Hello")

    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']

    print("File is",file)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print("bice nice")
        # Here you can process the file (apply virtualisation, etc.)
        return jsonify({'message': f'File {filename} uploaded successfully.', 'filename': filename}), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
