import os
from groq import Groq
from moviepy.editor import VideoFileClip, AudioFileClip
from dotenv import load_dotenv
import subprocess

load_dotenv()


def extract_audio(video_path, output_audio_path):
    """
    Extracts audio from a video file
    """
    video = VideoFileClip(video_path)
    duration = video.duration
    audio = video.audio

    audio.write_audiofile(output_audio_path)

    return output_audio_path


def compress_audio_with_ffmpeg(input_audio_path, output_audio_path):
    """
    Compresses the audio using FFmpeg by setting sample rate to 16000 Hz and converting to mono (1 channel).

    """
    os.remove(output_audio_path)
    command = [
        "ffmpeg",
        "-i",
        input_audio_path,
        "-ar",
        "16000",
        "-ac",
        "1",
        "-map",
        "0:a",
        output_audio_path,
    ]

    subprocess.run(command, check=True)
    print(f"Compressed audio saved to {output_audio_path}")


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_file_path):
    """
    Transcribes audio using Groq's Whisper model.
    """
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=("extracted_audio.wav", audio_file.read()),
            model="distil-whisper-large-v3-en",
            response_format="json",
            language="en",
            temperature=0.0,
        )
        return transcription.text



def add_audio_to_video(video_path, audio_path, output_path):
    try:
        command = [
            "ffmpeg",
            "-y",                   # Overwrite output file without asking
            "-i", video_path,        # First input: the video file
            "-i", audio_path,        # Second input: the audio file
            "-c:v", "copy",          # Copy the video stream without re-encoding
            "-c:a", "aac",           # Encode audio as AAC (widely supported)
            "-strict", "experimental",  # Enable experimental features for AAC
            "-map", "0:v:0",         # Map the video from the first input (video file)
            "-map", "1:a:0",         # Map the audio from the second input (audio file)
            "-shortest",             # Ensure output duration matches the shortest input
            output_path              # The output file
        ]

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        if process.returncode != 0:
            print(f"FFmpeg error: {process.stderr}")
            raise Exception(f"FFmpeg failed with error: {process.stderr}")
            
        print(f"Audio added successfully! Output saved to {output_path}")

    except Exception as e:
        print(f"Error adding audio to video: {str(e)}")


def correction_with_llama(transcription):

    prompt = f"""
    Please correct the following transcription, removing any grammatical errors and filler words like 'um', 'hmm', and other hesitations. 
    Keep only the necessary text, and provide the exact transcription as a single paragraph, using commas where needed. 

    Transcription to correct: 
    {transcription}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
