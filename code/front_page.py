from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from PyPDF2 import PdfReader
from docx2txt import process
from open_interface import load_api_keys_from_json
# from google.cloud import texttospeech
import wave
import markdown
import re
import os
#import pyaudio
import pygame

from resume_functions import gap_finder, get_recommendations, write_cover, get_interview_questions_prompt, get_interview_performance, get_projects
import gcloud_stt
import gcloud_tts

app = Flask(__name__)
'''
p = pyaudio.PyAudio()
recording_status = {1: False, 2: False, 3: False}
pygame.mixer.init()
'''

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
    
    session['resume'] =  resume
    
    return redirect(url_for('display_jobs'))
    
    #return render_template('display_content.html', filename=improvement_file)
    #return redirect(url_for('display_content', relative_path=suggestions))

def display_resume_improvement(resume, job_description):
    # Add logic to display resume improvement suggestions based on file_content and job_description
    improvement_file = gap_finder(resume, job_description)
    
    session['resume'] =  resume
    session['job_description'] =  job_description
    #return render_template('display_content.html', filename=improvement_file)
    return redirect(url_for('display_content', relative_path=improvement_file, title="Resume gaps", button="true"))

def display_cover_letter(resume,job_description):
    cover_letter_file = write_cover(resume,job_description)
    return redirect(url_for('display_content',relative_path=cover_letter_file, title="Cover letter", button="false"))
    
def get_interview_questions(resume, job_description):

    context, filename = get_interview_questions_prompt(resume, job_description)
    
    session['context'] = context
    
    questions = extract_file_content(filename)
    
    #print("interview questions")
    #print(questions)
    
    # Use regular expressions to extract questions
    questions_parsed = [re.sub(r'\bQuestion\b', '', part).strip() for part in re.split(r'(?=\bQuestion\b)', questions)][1:]
    
    #print(questions_parsed)

    # Print the separated questions
    for i, question in enumerate(questions_parsed, start=1):
        output = "question" + str(i) + ".wav"
        question = question.split(')')[0]
        question = question.split(':')[1]
        gcloud_tts.text_to_speech(question, output_file=output)
        print(f"Question {i}: {question.strip()}")


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

@app.route('/record_resp')
def record_resp():
    return render_template('response_rec.html')
'''
# Route to handle button clicks
@app.route('/button_click/<int:row>/<int:button>')
def button_click(row, button):
    global recording_status

    if button == 1:  # Play audio button
        play_audio(row)
        status = f"Playing audio for Row {row}"
    elif button == 2:  # Start recording button
        recording_status[row] = True
        start_audio(row)
        status = f"Recording started for Row {row}"
    elif button == 3:  # Stop recording button
        recording_status[row] = False
        save_audio(row)
        status = f"Recording stopped for Row {row}"

    return {"status": status}

def play_audio(row):
    # Generate the filename for the audio file
    filename = os.path.join(app.config['UPLOAD_FOLDER'],f"q{row}_tts.wav")

    # Load and play the audio file
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def start_audio(row):
     # Implement code to save the recorded audio to a wav file for the specified row
    global stream
    global frames
    global filename
    filename = os.path.join(app.config['UPLOAD_FOLDER'],f"response{row}_recording.wav")
    frames = []  # List to store audio frames
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    while recording_status[row]:
        data = stream.read(1024)
        frames.append(data)

def save_audio(row):
    stream.stop_stream()
    stream.close()

    # Save the recorded audio to a wav file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
'''
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

        file = request.files['file']
        job_description = request.form['job_description']
        
             # Save job description in a separate file
        job_description_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
        with open(job_description_filename, 'w') as job_file:
            job_file.write(job_description)
            
        if file.filename == '':
            return render_template('upload_page_interview.html', message='No selected file')

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Extract information from the uploaded file
            resume = extract_file_content(filename)
            
            return get_interview_questions(resume, job_description)
            
        return render_template('upload_page_interview.html', message='Invalid file format')
        
        

    
@app.route('/display_content/<path:relative_path>')
def display_content(relative_path):
    # Extract information from the uploaded file
    #file_content = extract_file_content_relative_path(relative_path)
    
    file_name = os.path.basename(relative_path)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    markdown.markdownFromFile(input=file_path, output=file_path)
    file_content = extract_file_content(file_path)
    
    if request.args['button'] == "true":
    
        return render_template('display_content.html', file_content=file_content, title = request.args['title'])
        
    else:
    
        return render_template('display_content_no_button.html', file_content=file_content, title = request.args['title'])
    

'''

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        input_text = request.form['text_input']
        text_to_speech(input_text)
        return render_template('result.html')
'''


@app.route('/projects')
def display_projects():
    path = get_projects(session.get("resume"), session.get("job_description"))
    file_name = os.path.basename(path)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    markdown.markdownFromFile(input=file_path, output=file_path)
    file_content = extract_file_content(file_path)
    return render_template('display_content.html',file_content=file_content, title="Projects", button="false")

@app.route('/display_jobs')
def display_jobs():
    suggestions = get_recommendations(session.get("resume"))
    title = "Suggested Jobs"
    if not suggestions or len(suggestions) == 0:
        suggestions = [[],0]

    return render_template('display_jobs.html', job_list=suggestions[0], number=suggestions[1], title="No suitable jobs found")


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
