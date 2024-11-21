import yt_dlp as youtube_dl
from moviepy.editor import AudioFileClip
import streamlit as st
import openai
import os

# Define API key for OpenAI (replace 'YOUR_OPENAI_API_KEY' with your actual key)
openai.api_key = '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'

# Function to download YouTube audio
def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return 'downloaded_audio.wav'
    except Exception as e:
        st.write(f"An error occurred while downloading audio: {e}")
        return None

# Function to transcribe audio using OpenAI's Whisper model
def audio_to_text(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            return response['text']
    except Exception as e:
        st.write(f"An error occurred during transcription: {e}")
        return None

# Function to summarize text using OpenAI's language model
def summarize_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n\n{text}",
            max_tokens=50,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.write(f"An error occurred during summarization: {e}")
        return None

# Streamlit app layout and functionality
st.title("YouTube Video Summarizer")
st.write("Welcome to the YouTube Video Summarizer app!")

# Input field for the YouTube video URL
video_url = st.text_input("Enter YouTube video URL:")

if st.button("Summarize"):
    if video_url:
        st.write("Downloading audio...")
        audio_file_path = download_audio(video_url)

        if audio_file_path:
            st.write("Transcribing audio...")
            transcription = audio_to_text(audio_file_path)
            st.write("Transcription:")
            st.write(transcription)

            st.write("Summarizing transcription...")
            summary = summarize_text(transcription)
            st.write("Summary:")
            st.write(summary)
        else:
            st.write("Audio download failed. Please check the video URL.")
    else:
        st.write("Please enter a valid YouTube video URL.")
