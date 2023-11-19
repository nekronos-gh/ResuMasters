from google.cloud import speech_v1p1beta1 as speech
import io
import os

UPLOAD_FOLDER = 'uploads'

def speech_to_text(audio_file_path):

    output_file = os.path.join(UPLOAD_FOLDER, audio_file_path)
    
    with io.open(output_file, "rb") as audio_file:
        content = audio_file.read()
        
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        #sample_rate_hertz=24000,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    
    text = ""

    for result in response.results:
        text = text + result.alternatives[0].transcript
        #print("Transcript: {}".format(result.alternatives[0].transcript))
        
    return text

if __name__ == "__main__":
    # Get user input
    audio_file_path = input("Enter the path to the audio file you want to transcribe: ")
    
    audio_file_path = "question1.wav"

    #with io.open(audio_file_path, "rb") as audio_file:
    #    content = audio_file.read()

    # Perform speech-to-text
    speech_to_text(audio_file_path)

