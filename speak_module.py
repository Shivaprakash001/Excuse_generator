import pyttsx3

engine = pyttsx3.init(driverName='sapi5')
def speak(text):
    engine.setProperty('rate', 150)  # Speed of speech
    engine.say(text)
    engine.runAndWait()

