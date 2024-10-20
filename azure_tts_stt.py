import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import requests

load_dotenv()


def correct_transcription_with_gpt4(transcription):
    """Corrects transcription using GPT-4."""

    # Define a clearer and typo-free prompt
    prompt = f"""
    Please correct the following transcription, removing any grammatical errors and filler words like 'um', 'hmm', and other hesitations. 
    Keep only the necessary text, and provide the exact transcription as a single paragraph, using commas where needed. 

    Transcription to correct: 
    {transcription}
    """

    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")  # Use environment variable
    if not azure_api_key:
        raise ValueError("API key not found. Set AZURE_OPENAI_API_KEY environment variable.")

    endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    
    try:
        headers = {
            "Content-Type": "application/json", 
            "api-key": azure_api_key  # Use the API key from environment variable
        }
        data = {"messages": [{"role": "user", "content": prompt}]}
        
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)

        response_data = response.json()
        corrected_transcription = response_data['choices'][0]['message']['content']
        print(corrected_transcription)
        return corrected_transcription

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        if response is not None:
            print(f"Response: {response.text}")
        return None




def text_to_speech(text):
    temp_audio_path = "processed_audio.wav"

    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION")
    )
    speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_audio_path)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    synthesis_result = synthesizer.speak_text_async(text).get()

    if synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio = AudioSegment.from_wav(temp_audio_path)
        audio.export(temp_audio_path, format="wav")
    else:
        raise Exception("Error in speech synthesis.")

    return temp_audio_path