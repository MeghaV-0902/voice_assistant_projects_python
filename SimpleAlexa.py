import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser

webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

keep_going=True

listener = sr.Recognizer()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id )

#engine.say("hi i am your personal assistant. what can i do for you?")

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source,duration=1)
            print("listening...")
            voice=listener.listen(source)
            command= listener.recognize_google(voice)
            #print(command)
            command=command.lower()
            if 'alexa' in command:
                command=command.replace('alexa ','')
                #print(command.capitalize())
            print("", end='')
    except:
        pass
    return command

def run_alexa():
    command=take_command()
    print("YOU: "+command.capitalize())
    if'play' in command:
        song= command.replace('play ','')
        talk("playing"+song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time=datetime.datetime.now().strftime('%I:%M %p')
        talk("The time is " + time)
        print("ALEXA: "+time)
    elif ('who is ' in command or 'information' in command or 'info' in command or 'about' in command):
        person=command.replace("who is ",'')
        info=wikipedia.summary(person,1)
        talk(info)
        print(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'how are you' in command:
        talk("I'm fine. Hope you are doing great too")
    elif 'hi' in command or 'hello' in command:
        talk("HEY great to hear from you")
    elif 'search' in command:
        text=command.replace("search ",'')
        webbrowser.get('chrome').open_new(text)
        talk("ALEXA: Search found")
        print("ALEXA: window open")
    elif 'ok thank you' in command or 'see you later' in command:
        global keep_going
        keep_going=False
        talk("my pleasure. see you later")

    else:
        talk("I didnt understand")
while keep_going:
    run_alexa()
