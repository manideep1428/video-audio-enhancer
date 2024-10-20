import os
import requests

def correct_transcription_with_gpt4(transcription):
    """Corrects transcription using GPT-4."""

    # Define a clearer and typo-free prompt
    prompt = f"""
    Please correct the following transcription, removing any grammatical errors and filler words like 'um', 'hmm', and other hesitations. 
    Keep only the necessary text, and provide the exact transcription as a single paragraph, using commas where needed. 

    Transcription to correct: 
    {transcription}
    """

    azure_api_key = "22ec84421ec24230a3638d1b51e3a7dc"
    # Use environment variable
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



from utils import add_audio_to_video

add_audio_to_video(video_path="data/uploaded_video.mp4", audio_path="processed_audio.wav", output_path="final_video.mp4")