import pyttsx3


def speak(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('rate', 250)  # Speed of speech
    engine.say(text)
    engine.runAndWait()

