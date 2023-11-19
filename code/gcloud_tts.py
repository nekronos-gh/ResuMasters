from google.cloud import texttospeech
import wave
import os

UPLOAD_FOLDER = 'uploads'

def text_to_speech(input_text, output_file='output.wav'):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=input_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    output_file = os.path.join(UPLOAD_FOLDER, output_file)

    with wave.open(output_file, 'w') as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)
        wave_file.setframerate(24000)  # Adjust as needed
        wave_file.writeframes(response.audio_content)

if __name__ == "__main__":
    # Get user input
    input_text = input("Enter the text you want to convert to speech: ")

    # Specify the output file name (optional)
    output_file_name = "output.wav"

    # Perform text-to-speech and save the result as a .wav file
    text_to_speech(input_text, output_file=output_file_name)

