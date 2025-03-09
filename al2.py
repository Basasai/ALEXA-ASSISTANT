import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import webbrowser

# Initialize the recognizer and the text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Get the available voices
voices = engine.getProperty('voices')

# Set the voice to the second voice if available, otherwise use the first voice
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

def engine_talk(text):
    print(f"Alexa is saying: {text}")  # Debug statement
    engine.say(text)
    engine.runAndWait()

def user_commands():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(f"User said: {command}")  # Debug statement
                return command
    except Exception as e:
        print(f"Error: {e}")  # Debug statement
        return ""
    
def open_website(site_name):
    # Mapping of keywords to websites
    websites = {
        'google': 'https://www.google.com',
        'youtube': 'https://www.youtube.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://www.twitter.com',
        'gmail': 'https://mail.google.com',
    }
    if site_name in websites:
        url = websites[site_name]
        engine_talk(f"Opening {site_name} in your browser")
        webbrowser.open(url)
    else:
        engine_talk(f"I don't have a website mapped for {site_name}. Please try again.")

def run_alexa():
    command = user_commands()
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            engine_talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            engine_talk('The current time is ' + time)
        elif 'who is' in command:
            name = command.replace('who is', '')
            info = wikipedia.summary(name, 1)
            print(info)
            engine_talk(info)
        elif 'joke' in command:
            engine_talk(pyjokes.get_joke())
        elif 'open' in command:
            site_name = command.replace('open', '').strip()
            open_website(site_name)
        elif 'stop' in command:
            engine_talk('Goodbye!')
            sys.exit()
        else:
            engine_talk('I could not hear you properly')
    else:
        engine_talk('I did not catch that. Please speak again.')

while True:
    run_alexa()
