# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:51:42 2021

@author: Megha
"""
import requests
import json
import pyttsx3
import speech_recognition as sr
import pyaudio
import re
import threading
import time



API_KEY='tw47WyN1TETg'
PROJECT_TOKEN='tVm0BJwkLfeB'
RUN_TOKEN='tMzZMeTj4a5v'


class Data:
    def __init__(self, api_key, project_token):
        self.api_key=api_key
        self.project_token=project_token
        self.params={"api_key":self.api_key}
        self.data=self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params=self.params)
        self.data=json.loads(response.text)
        return self.data

    def get_total_cases(self):
         data=self.data['total']
         for content in data:
             if content['name']=='Coronavirus Cases:':
                 return content['values']

    def get_total_deaths(self):
         data=self.data['total']
         for content in data:
             if content['name']=='Deaths:':
                 return content['values']
         return "0"

    def get_country_data(self, country):
        data = self.data["country"]
        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return "0"

    def get_list_of_countries(self):
    		countries = []
    		for country in self.data['country']:
    			countries.append(country['name'].lower())

    		return countries
    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)
        t = threading.Thread(target=poll)
        t.start()




#print(data.get_country_data("india")['total_cases'])

def speak(text):
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id )
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        audio=r.listen(source)
        said=""

        try:
            said=r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception :",str(e))
    return said.lower()


#print(get_audio())

def main():
    print("Started running")
    data=Data(API_KEY,PROJECT_TOKEN)
    END_PHRASE="stop"
    TOTAL_PATTERNS={
        re.compile("[\\w\s]+total[\w\s]+cases"):data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths
                    }
    COUNTRY_PATTERNS={
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths']
        }
    country_list=data.get_list_of_countries()

    UPDATE_COMMAND="update"

    while True:
        print("listening...")
        text=get_audio()
        result=None

        for pattern, func in COUNTRY_PATTERNS.items():
            #print("Entered for")
            if pattern.match(text):
                words=set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result=func(country)
                        break


        for pattern, func in TOTAL_PATTERNS.items():
            #print("Entered for")
            if pattern.match(text):
                #print("in if stmt")
                result = func()
                break

        if text==UPDATE_COMMAND:
            result="Data is being updated. This may take a moment!"
            data.update_data()

        if result:
                speak(result)

        if text.find(END_PHRASE)!=-1:
            print("Exit")
            break

main()
