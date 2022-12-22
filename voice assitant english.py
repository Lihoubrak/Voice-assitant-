import ctypes
import json
import os
import re
import subprocess
import time
import urllib
import webbrowser
from datetime import datetime
from time import strftime
import requests
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
from youtube_search import YoutubeSearch



def get_audio():
    robot_aer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("AI: Listening.....!")
        audio = robot_aer.listen(mic, phrase_time_limit=5)
        try:
            text = robot_aer.recognize_google(audio)
            print("You: ", text)
            return text
        except:
            print("AI : Wrong...")
            return 0

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("AI can't hear you, can you say it again?")
    time.sleep(3)
    stop()
    return 0


def speak(text):
    print("AI:", text)
    robot_mouth = pyttsx3.init()
    # voices = robot_mouth.getProperty('voices')
    # robot_mouth.setProperty('voice', voices[1].id)
    robot_mouth.say(text)
    robot_mouth.runAndWait()

    # for voice in voices:
    #     # to get the info. about various voices in our PC
    #     print("Voice:")
    #     print("ID: %s" % voice.id)
    #     print("Name: %s" % voice.name)
    #     print("Age: %s" % voice.age)
    #     print("Gender: %s" % voice.gender)
    #     print("Languages Known: %s" % voice.languages)


def help_me():
    speak("""AI can help you with the following:
    <<........>>>
    1. Greeting
    2. Time display
    3. Open website, desktop application
    4. Search with google
    5. Search videos with youtube
    6. Weather forecast
    7. Read the paper
    8. Change desktop wallpaper
    9. Definition (Wikipedia)
    10. Play music with youtube
    <<.........>>>
    """)


def stop():
    speak("Goodbye, see you later")


def hello(name):
    day_time = int(strftime('%I'))
    if 0 <= day_time < 13:
        speak(f'Hello {name}. Good morning to you <..>')
    elif 13 <= day_time < 18:
        speak(f'Hello {name}. good afternoon <..>')
    elif 18 <= day_time < 22:
        speak(f'Hello {name}. Good evening, have you eaten yet? <..>')
    elif 22 <= day_time < 23:
        speak(f'Hello{name}. Its late ,you should go to bed go to bed early to have beautiful skin <..>')
    else:
        speak(f'Hello {name}. Have a good night <..>')


def get_time(text):
    now = datetime.now()
    if "time" in text:
        speak(f" It's {now.hour} hours  {now.minute} minutes {now.second} seconds")
    elif "day" in text:
        speak(f" Today is  {now.day} month {now.month} year {now.year}")
    else:
        speak("I don't understand <'-'>")


def open_app(text):
    if "google" in text:
        speak("Open google chrome")
        # subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "Telegram" in text:
        speak(" Open telegram ")
        # subprocess.Popen("C:\\Users\\Brak Lihou\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
        os.startfile("C:\\Users\\Brak Lihou\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
    elif "zalo" in text:
        speak(" Open zalo")
        #subprocess.Popen("C:\\Users\\Brak Lihou\\AppData\\Local\\Programs\\Zalo\\Zalo.exe")
        os.startfile("C:\\Users\\Brak Lihou\\AppData\\Local\\Programs\\Zalo\\Zalo.exe")
    else:
        speak("Application not yet install :)")


def open_web(text):
    reg_ex = re.search('open (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("The website you requested has been opened. ")
        if input("enter 'a' to continue: ") == "a":
            pass
        return True
    else:
        return False


def open_google_search():
    speak("What do you need to search on google:..")
    search = str(get_text()).lower()
    # url = f"https://www.google.com/search?q={search}"
    # webbrowser.get().open(url)
    pywhatkit.search(search)
    speak(f'This is information about {search} that you search on google')


def open_youtube_search():
    speak("What video do you want to watch on youtube:..")
    search = str(get_text()).lower()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak(f'Here is the video {search} that you search on youtube <..>')


def open_youtube_2():
    speak("What video do you want to watch on youtube:..")
    search = get_text()
    # while True:
    #     result = YoutubeSearch(search, max_results=10).to_dict()
    #     if result:
    #         break
    # url = f"https://www.youtube.com" + result[0]['url_suffix']
    # webbrowser.get().open(url)
    pywhatkit.playonyt(search)
    speak(f'Here is the video {search} that you search on youtube <..>')
    print(result)

def current_weather():
    speak("Where do you want to see the weather?")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "3f300f13c74943b39afd7940eb0aa108"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.now()
        content = f"""
        Today is {now.day} month {now.month} year {now.year}
        The sun rises in  {sunrise.hour} hours {sunrise.minute} minute
        The sun goes down {sunset.hour} hours {sunset.minute} minute
        Current temperature is {current_temperature} degrees Celsius
        The air pressure is {current_pressure} Pascal's vector
        Humidity is {current_humidity}%
        """
        speak(content)
    else:
        speak("Your address could not be found")
        current_weather()

# url = 'https://api.unsplash.com/photos/random?client_id=' + \
#       api_key
def change_wallpaper():
    api_key = "FjxCbKxmzTrradwyKJChv42K9dz1xMFoA6bzaryhoAo"
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
          api_key
    f = urllib.request.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']
    urllib.request.urlretrieve(photo, "G:\\OBS VIDEO\\a.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "G:\\OBS VIDEO\\a.png", 3)
    speak("Your desktop wallpaper has been changed. Do you go home to see if it's beautiful?")
def read_news():
    #https://newsapi.org/v2/everything?q=th%E1%BB%83%20thao&apiKey=ef0edfb96bba4717b9da796b6ca7a152
    speak("What do you want to read about?")
    queue = get_text()
    params = {'apiKey': 'ef0edfb96bba4717b9da796b6ca7a152', "q": queue, }
    api_result = requests.get('https://newsapi.org/v2/everything?', params)
    api_response = api_result.json()
    print("News")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"News {number}:\nTitle: {result['title']}\nDescription: {result['description']}\nLink: {result['url']}")
        if number <= 3:
            webbrowser.open(result['url'])
def tell_me_about():
    try:
        speak("What do you want to hear about?")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(5)
        for content in contents[1:]:
            speak("Do you want to hear more?")
            ans = get_text()
            if "yes" not in ans:
                break
            speak(content)
            time.sleep(5)

        speak('Thank you for listening!!!')
    except:
        speak("The bot doesn't define your term. Please say it again")

def main_brain():
    speak("hello what's your name??")
    name = get_text()
    if name:
        speak(f'Hello {name}.')
        hello(name)
        speak(f'Do you need help with bots? ')
        while True:
            text = get_text()
            if not text:
                break
            elif "goodbye" in text or "see you later" in text:
                stop()
                break
            elif 'what can' in text:
                help_me()
            elif 'time' in text:
                get_time(text)
            elif 'open' in text:
                open_app(text)
                #if input("Để tiếp tục mở y/n: ") == "y":
                   # pass
            elif 'open.' in text:
                open_web(text)
               # if input("Để tiếp tục mở y/n: ") == "y":
                   # pass
            elif "google" in text:
                open_google_search()
            elif 'youtube' in text:
                speak("Do you want a simple or complex search?")
                yeu_cau = get_text()
                if "simple" in yeu_cau:
                    open_youtube_search()
                   # if input("Để tiếp tục y/n: ") == "y":
                     #   pass
                elif "complex" in yeu_cau:
                    open_youtube_2()
                    #if input("Để tiếp tục y/n: ") == "y":
                       # pass
            elif "weather" in text:
                current_weather()
            elif "wallpaper" in text:
                change_wallpaper()
            elif "read" in text:
                read_news()
            elif "definition" in text:
                tell_me_about()
            else:
                speak(f'This feature is probably not available, please choose it again later <..>')
main_brain()
