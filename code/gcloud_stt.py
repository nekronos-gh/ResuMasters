from google.cloud import speech_v1p1beta1 as speech
import io

def speech_to_text(audio_content):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    # Get user input
    audio_file_path = input("Enter the path to the audio file you want to transcribe: ")

    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    # Perform speech-to-text
    speech_to_text(content)

