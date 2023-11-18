from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader
from docx2txt import process
import re
import os

## import resume_functions from backend, knowing backend is in the parent directory
import sys
sys.path.append('..')
from backend.resume_functions import *

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf','docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def extract_file_content(filename):
    if filename.endswith('.pdf'):
        # Extract text content from PDF
        with open(filename, 'rb') as file:
            pdf_reader = PdfReader(file)
            text_content = ''
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            text_content = scrub_NoEmailLinkedin(text_content)
            return text_content
    elif filename.endswith('.docx'):
        text_content = scrub_NoEmailLinkedin(process(filename))
        return text_content
    
    elif filename.endswith('.txt'):
        # Read text content from a text file
        with open(filename, 'r') as file:
            text_content = scrub_NoEmailLinkedin(file.read())
            return text_content
    else:
        return 'Unsupported file type'

def scrub_NoEmailLinkedin(content):
    content = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*','', content)
    content = re.sub(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+','', content)
    return content
    
@app.route('/')
def front_page():
    return render_template('front_page.html')
    
@app.route('/job_matches')
def job_matches():
    #return render_template('upload_page_job_suggest.html')
    return redirect(url_for('upload', category='job_matches'))

@app.route('/skill_improvement')
def skill_improvement():
    #return render_template('upload_page_skill_suggest.html')
    return redirect(url_for('upload', category='skill_improvement'))
    
@app.route('/upload/<category>', methods=['GET', 'POST'])
def upload(category):

    if category == "job_matches":
    
        if 'file' not in request.files:
            return render_template('upload_page_job_suggest.html', message='Upload your files here')

        file = request.files['file']

        if file.filename == '':
            return render_template('upload_page_job_suggest.html', message='No selected file')

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Extract information from the uploaded file
            file_content = extract_file_content(filename)

            
            return redirect(url_for('display_content', filename=file.filename))

        return render_template('upload_page_job_suggest.html', message='Invalid file format')
    
    if category == "skill_improvement":
            
        if 'file' not in request.files:
            return render_template('upload_page_skill_suggest.html', message='Upload your files here')

        file = request.files['file']
        job_description = request.form['job_description']
        
             # Save job description in a separate file
        job_description_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
        with open(job_description_filename, 'w') as job_file:
            job_file.write(job_description)

        if file.filename == '':
            return render_template('upload_page_skill_suggest.html', message='No selected file')

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Extract information from the uploaded file
            file_content = extract_file_content(filename)

            
            return redirect(url_for('display_content', filename=file.filename))

        return render_template('upload_page_skill_suggest.html', message='Invalid file format')
    
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



if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
