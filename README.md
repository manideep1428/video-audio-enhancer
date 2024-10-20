# AI-Powered Video Audio Enhancer

This project enhances the audio of a video by extracting the audio, transcribing it, correcting the transcription, synthesizing new audio, and then replacing the original audio in the video. It leverages GPT-4 for transcription correction and Azure for text-to-speech.

## Table of Contents
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Functions Overview](#functions-overview)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/video-audio-enhancer.git
cd video-audio-enhancer
```

2. Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
```
# or for Windows:
```bash
# venv\Scripts\activate
```

3. Install required dependencies
```bash
pip install -r requirements.txt
```

4. Set up your environment variables

Create a .env file in the root directory and add the required keys. For example:
```bash

AZURE_API_KEY=<your-azure-api-key>
AZURE_REGION=<your-azure-region>
SPEECH_REGION=<your-api-region>
SPEECH_KEY=<same-your-azure-api-key>


```
5. Run the Streamlit app
```bash
streamlit run app.py
```

Example .env file:

```bash
AZURE_API_KEY=your_azure_api_key
AZURE_REGION=your_azure_region
SPEECH_API=same_as_azure_apikey
SPEECH_REGION=yourregion (#example: swedencentral)
```

Project Structure

video-audio-enhancer/
│
├── app.py                     
├── utils.py                    
├── azure_tts_stt.py          
├── test.py                    
├── styles.css                 
├── data/                      
├── requirements.txt           
└── .env                       

How It Works

The application allows you to upload a video file, extracts its audio, and processes it step-by-step:

1. Upload a video: Users upload a video file (.mp4, .avi, .mov).


2. Audio Extraction: The app extracts audio from the video.


3. Audio Compression: The extracted audio is compressed using FFmpeg.


4. Transcription: The app transcribes the audio using an external API (e.g., Azure STT).


5. GPT-4 Correction: The transcription is corrected using GPT-4.


6. Text-to-Speech: The corrected transcription is synthesized into audio using Azure TTS.


7. Audio Replacement: The new audio is then added to the original video, replacing the original audio.

