
import os

from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader
#from google.cloud import storage

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Instantiates a client
#storage_client = storage.Client()

#PROJECT_ID = 'your-project-id'
BUCKET_NAME = 'your-bucket-name'
#KEY_FILE = 'path/to/your/key.json'

#storage_client = storage.Client.from_service_account_json(KEY_FILE)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('upload_page.html')
    
@app.route('/upload', methods=['POST'])
def upload_file():
            
    if 'file' not in request.files:
        return render_template('upload_page.html', message='No file part')

    file = request.files['file']
    job_description = request.form['job_description']
    
         # Save job description in a separate file
    job_description_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
    with open(job_description_filename, 'w') as job_file:
        job_file.write(job_description)

    if file.filename == '':
        return render_template('upload_page.html', message='No selected file')

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Extract information from the uploaded file
        file_content = extract_file_content(filename)

        
        return redirect(url_for('display_content', filename=file.filename))

    return render_template('upload_page.html', message='Invalid file format')
    
@app.route('/display_content/<filename>')
def display_content(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    job_description_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
    
    # Extract information from the uploaded file
    file_content = extract_file_content(file_path)
    
    # Read job description from the file
    with open(job_description_filename, 'r') as job_file:
        job_description = job_file.read()

    return render_template('display_content.html', file_content=file_content, job_description=job_description)


def extract_file_content(filename):
    if filename.endswith('.pdf'):
        # Extract text content from PDF
        with open(filename, 'rb') as file:
            pdf_reader = PdfReader(file)
            text_content = ''
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            return text_content
    elif filename.endswith('.txt'):
        # Read text content from a text file
        with open(filename, 'r') as file:
            return file.read()
    else:
        return 'Unsupported file type'
    

@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
