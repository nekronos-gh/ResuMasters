from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from PyPDF2 import PdfReader
from docx2txt import process
from open_interface import load_api_keys_from_json
# from google.cloud import texttospeech
import wave
import markdown
import re
import os
import torchaudio

from resume_functions import gap_finder, get_recommendations, write_cover

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf','docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.secret_key = "162de504fbde477d81799c7edecbf9c73e1eda932104548bc64caa8f1d0b9cbf"
load_api_keys_from_json("keys.json")


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

'''
def display_job_suggestions(resume):
    # Add logic to display job suggestions based on file_content and job_description
    suggestions = get_recommendations(resume)
    return render_template('job_suggestions.html', suggestions=suggestions)
'''

def display_job_suggestions(resume):
    # Add logic to display resume improvement suggestions based on file_content and job_description
    
    session['recommendations'] =  get_recommendations(resume)
    
    return redirect(url_for('display_jobs'))
    
    #return render_template('display_content.html', filename=improvement_file)
    #return redirect(url_for('display_content', relative_path=suggestions))

def display_resume_improvement(resume, job_description):
    # Add logic to display resume improvement suggestions based on file_content and job_description
    improvement_file = gap_finder(resume, job_description)
    
    #return render_template('display_content.html', filename=improvement_file)
    return redirect(url_for('display_content', relative_path=improvement_file, title="Resume gaps"))

def display_cover_letter(resume,job_description):
    cover_letter_file = write_cover(resume,job_description)
    return redirect(url_for('display_content',relative_path=cover_letter_file, title="Cover letter"))
    
def get_interview_questions(job_description):

    return "we are placeholder for now"
    

    # Add logic to display resume improvement suggestions based on file_content and job_description
    #improvement_file = gap_finder(resume, job_description)
    

    #return redirect(url_for('display_content', relative_path=improvement_file))

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
    
@app.route('/cover_letter')
def cover_letter():
    #return render_template('upload_page_skill_suggest.html')
    return redirect(url_for('upload', category='cover_letter'))
    
@app.route('/sample_interview')
def sample_interview():
    #return render_template('upload_page_skill_suggest.html')
    return redirect(url_for('upload', category='sample_interview'))

@app.route('/record_audio')
def record_audio():
    return render_template('audiorec.html')

@app.route('/transcribe/<response>', methods=['POST'])
def transcribe_audio(response):
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio']

    # Save the audio file temporarily
    temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_audio_{response}.wav')
    audio_file.save(temp_audio_path)

    # Load the audio file
    waveform, sample_rate = torchaudio.load(temp_audio_path)
    print(waveform)
    print(sample_rate)
    # put google code thing here
    transcription = 'placeholder blah blah'
    # Remove the temporary audio file
    # os.remove(temp_audio_path)

    return jsonify({'transcription': transcription})
    
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
            resume = extract_file_content(filename)
            
            
            return display_job_suggestions(resume)
            
            #return redirect(url_for('display_content', filename=file.filename))

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
            resume = extract_file_content(filename)
            
            return display_resume_improvement(resume, job_description)

            
            #return redirect(url_for('display_content_skill', filename=file.filename))

        return render_template('upload_page_skill_suggest.html', message='Invalid file format')
    
    if category == "cover_letter":
            
        if 'file' not in request.files:
            return render_template('upload_page_cover_letter.html', message='Upload your files here')

        file = request.files['file']
        job_description = request.form['job_description']
        
             # Save job description in a separate file
        job_description_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
        with open(job_description_filename, 'w') as job_file:
            job_file.write(job_description)

        if file.filename == '':
            return render_template('upload_page_cover_letter.html', message='No selected file')

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Extract information from the uploaded file
            resume = extract_file_content(filename)
            
            #print("debug in upload")
            #print(resume)
            
            return display_cover_letter(resume,job_description)

            
            #return redirect(url_for('display_content_skill', filename=file.filename))

        return render_template('upload_page_cover_letter.html', message='Invalid file format')
        
    if category == "sample_interview":
            
        if 'file' not in request.files:
            return render_template('upload_page_interview.html', message='Upload your files here')

        job_description = request.form['job_description']
        
             # Save job description in a separate file
        job_description_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
        with open(job_description_filename, 'w') as job_file:
            job_file.write(job_description)
            
        return get_interview_questions(job_description)
        
        

    
@app.route('/display_content/<path:relative_path>')
def display_content(relative_path):
    # Extract information from the uploaded file
    #file_content = extract_file_content_relative_path(relative_path)
    
    file_name = os.path.basename(relative_path)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    markdown.markdownFromFile(input=file_path, output=file_path)
    file_content = extract_file_content(file_path)
    

'''

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        input_text = request.form['text_input']
        text_to_speech(input_text)
        return render_template('result.html')
'''



@app.route('/display_jobs')
def display_jobs():
    suggestions = session.get("recommendations")
    title = "Suggested Jobs"
    if not suggestions or len(suggestions) == 0:
        suggestions[0] = []
        suggestions[1] = 0

    return render_template('display_jobs.html', job_list=suggestions[0], number=suggestions[1], title="No suitable jobs found")


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
