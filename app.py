

import streamlit as st
import time
from utils import extract_audio, transcribe_audio, compress_audio_with_ffmpeg, add_audio_to_video
from azure_tts_stt import text_to_speech
from test import correct_transcription_with_gpt4
from dotenv import load_dotenv

load_dotenv()



# Page configuration
st.set_page_config(page_title="AI-Powered Video Audio Enhancer", layout="wide")

def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("styles.css")


st.markdown("<h1 class='title'>AI-Powered Video Audio Enhancer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enhance your video's audio with cutting-edge AI technology</p>", unsafe_allow_html=True)

st.markdown("<p class='upload-text'>Upload your video file:</p>", unsafe_allow_html=True)
video_file = st.file_uploader("", type=["mp4", "avi", "mov"])

if video_file is not None:
    with open("data/uploaded_video.mp4", "wb") as f:
        f.write(video_file.read())
    
    st.success("Video uploaded successfully!")

    if st.button("Enhance Audio"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        spinner = st.empty()

        def update_progress(step, total_steps, message):
            progress = int((step / total_steps) * 100)
            progress_bar.progress(progress)
            status_text.markdown(f"<p class='status-text'>{message}</p>", unsafe_allow_html=True)
            spinner.markdown("🔄", unsafe_allow_html=True)

        total_steps = 6
        current_step = 0

        try:
            # Audio extraction
            update_progress(current_step, total_steps, "Extracting audio...")
            extract_audio("data/uploaded_video.mp4", "data/extracted_audio.wav")
            current_step += 1

            # Audio compression
            update_progress(current_step, total_steps, "Compressing audio...")
            compress_audio_with_ffmpeg("data/extracted_audio.wav", "data/compressed_audio.wav")
            current_step += 1

            # Transcription
            update_progress(current_step, total_steps, "Transcribing audio...")
            transcription = transcribe_audio("data/compressed_audio.wav")
            current_step += 1

            # GPT-4 correction
            update_progress(current_step, total_steps, "Correcting transcription...")
            corrected_transcription = correct_transcription_with_gpt4(transcription=transcription)
            current_step += 1

            # Speech synthesis
            update_progress(current_step, total_steps, "Synthesizing speech...")
            text_to_speech(corrected_transcription)
            current_step += 1

            # Final video processing
            update_progress(current_step, total_steps, "Finalizing video...")
            add_audio_to_video(video_path="data/uploaded_video.mp4", audio_path="processed_audio.wav", output_path="data/final_video.mp4")
            current_step += 1

            update_progress(current_step, total_steps, "Video processing completed!")
            time.sleep(1)
            status_text.empty()
            progress_bar.empty()
            spinner.empty()

            st.success("Video enhanced successfully!")
            
            # Display the enhanced video
            st.markdown("<div class='video-container'>", unsafe_allow_html=True)
            st.video("data/final_video.mp4")
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}. Please try again.")