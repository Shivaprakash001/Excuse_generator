import platform
import pyttsx3

def get_engine():
    system = platform.system()
    if system == 'Windows':
        return pyttsx3.init('sapi5')
    elif system == 'Darwin':
        return pyttsx3.init('nsss')  # macOS
    else:
        return pyttsx3.init('espeak')  # Linux

engine = get_engine()

def speak(text):
    engine.say(text)
    engine.runAndWait()
