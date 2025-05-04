# speak_module.py
from gtts import gTTS
import streamlit as st
import os
import uuid

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    
    # Streamlit audio player
    audio_file = open(filename, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

    # Cleanup the file after use
    audio_file.close()
    os.remove(filename)
