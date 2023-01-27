import ctypes
import json
import os
import re
import subprocess
import time
import urllib
import webbrowser
from _ast import operator
from datetime import datetime
from time import strftime
import requests
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
from youtube_search import YoutubeSearch


# chuyển giọng nói (âm thanh) thành văn bản
def get_audio():
    robot_aer = sr.Recognizer()
    with sr.Microphone() as mic:  # dùng mic của máy để nghe người dùng nói
        print("Trợ lý ảo: đang nghe.....!")
        audio = robot_aer.listen(mic,
                                 phrase_time_limit=5)  # truyền vào âm thanh thu dc từ mic vào biến audio, để bot nghe trong 5s
        try:  # nhận dạng giọng nói
            text = robot_aer.recognize_google(audio,
                                              language="vi-VN")  # nhận dạng âm thanh ở biến audio chuyển thành văn bản
            print("Bạn: ", text)
            return text
        except:  # nếu lỗi
            print("Trợ lý ảo: bị lỗi ạ...")
            return 0


# có chức năng là máy tính sẽ cố gắng nhận dạng âm thanh của người đọc tối đa 3 lần cho đến khi máy tính hiểu
def get_text():
    for i in range(3):  # vòng lặp này sẽ chạy 3 lần
        text = get_audio()  # nghe những gì nghe dc sẽ chuyển thành văn bản
        if text:  # nếu true or !=0 thì if sẽ dc thực hiện
            return text.lower()
        elif i < 2:
            speak("mình không nghe rõ, bạn nói lại nha")
    time.sleep(3)  # chương trình sẽ tạm dừng trong 3s
    stop()
    return 0


# chuyển văn bản thành âm thanh
def speak(text):
    print("Trợ lý ảo:", text)
    robot_mouth = pyttsx3.init()
    voices = robot_mouth.getProperty('voices')
    robot_mouth.setProperty('voice', voices[1].id)
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
    speak("""bot có thể giúp bạn thực hiện các việc sau đây:
    <<........>>>
    1. chào hỏi
    2. Hiển thị giờ
    3. Mở website, ứng dụng desktop
    4. Tìm kiếm với google
    5. Tìm kiếm video với youtube
    6. Dự báo thời tiết
    7. Đọc báo
    8. Thay đổi hình nền máy tính
    9. Định nghĩa với từ điển bách khoa toàn thư ( Wikipedia )
    10. Mở nhạc với youtube
    <<.........>>>
    """)


def stop():
    speak("Tạm biệt bạn, hẹn gặp lại bạn sau nha")


def hello(name):
    day_time = int(strftime('%H'))
    if 0 <= day_time < 11:
        speak(f'chào bạn {name}. chúc bạn một buổi sáng tốt lành <..>')
    elif 11 <= day_time < 13:
        speak(f'chào bạn {name}. buổi trưa tốt lành nha <..>')
    elif 13 <= day_time < 18:
        speak(f'chào bạn {name}. buổi chiều an lành <..>')
    elif 18 <= day_time < 22:
        speak(f'chào bạn {name}. buổi tối vui vẻ, bạn đã ăn cơm chưa <..>')
    elif 22 <= day_time < 23:
        speak(f'chào bạn {name}. muộn rồi bạn nên đi ngủ, ngủ sớm để đẹp da nhé <..>')
    else:
        speak(f'chào bạn {name}. buổi tối vui vẻ <..>')


def get_time(text):
    now = datetime.now()
    if "giờ" in text:
        speak(f" Bây giờ là {now.hour} giờ {now.minute} phút {now.second} giây")
    elif "ngày" in text:
        speak(f" Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}")
    else:
        speak("tôi chưa hiểu ý của bạn <'-'>")


def open_app(text):
    if "google" in text:
        speak("mở google chrome")
        # subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        # mở ứng dụng dẽ ko tắt chương tr, tắt ứng dụng thì mới tát ct
    elif "Telegram" in text:
        speak(" mở ứng dụng Telegram ")
        # subprocess.Popen("C:\\Users\\Brak Lihou\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
        os.startfile("C:\\Users\\Brak Lihou\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
    elif "zalo" in text:
        speak(" mở ứng dụng zalo")
        # subprocess.Popen("C:\\Users\\Brak Lihou\\AppData\\Local\\Programs\\Zalo\\Zalo.exe")
        os.startfile("C:\\Users\\Brak Lihou\\AppData\\Local\\Programs\\Zalo\\Zalo.exe")
    else:
        speak("ứng dụng chưa được cài đặt ạ :)")


def open_web(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở ạ. ")
        if input("hãy nhập a để tiếp tục: ") == "a":  # sau khi mở web thì chương trình sẽ dừng lại đến khi bạn nhập "a"
            pass
        return True
    else:
        return False


def open_google_search():
    speak("Bạn cần tìm kiếm gì trên google vậy:..")
    search = str(get_text()).lower()
    # url = f"https://www.google.com/search?q={search}"
    # webbrowser.get().open(url)
    pywhatkit.search(search)
    speak(f'Đây là thông tin về {search} mà bạn tìm kiếm trên google')


def open_youtube_search():
    speak("Bạn muốn xem vi deo nào trên youtube vậy:..")
    search = str(get_text()).lower()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak(f'Đây là vi deo {search} mà bạn tìm kiếm trên youtube <..>')


def open_youtube_2():
    speak("Bạn muốn xem vi deo nào trên youtube vậy:..")
    search = get_text()
    # while True:
    #     result = YoutubeSearch(search, max_results=10).to_dict()
    #     if result:
    #         break
    # url = f"https://www.youtube.com" + result[0]['url_suffix']
    # webbrowser.get().open(url)
    pywhatkit.playonyt(search)
    speak(f'Đây là vi deo {search} mà bạn tìm kiếm trên youtube <..>')


def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"  # Đường dẫn trang web để lấy dữ liệu về thời tiết
    city = get_text()  # lưu tên thành phố vào biến city
    if not city:  # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
        pass
    api_key = "3f300f13c74943b39afd7940eb0aa108"  # api_key lấy trên open weather map
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"  # tìm kiếm thông tin thời thời tiết của thành phố
    # truy cập đường dẫn lấy dữ liệu thời tiết
    response = requests.get(call_url)  # gửi yêu cầu lấy dữ liệu
    data = response.json()  # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
    if data["cod"] != "404":  # kiểm tra nếu ko gặp lỗi 404 thì xem xét và lấy dữ liệu
        # lấy dữ liệu của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # 	lúc mặt trời mọc, mặt trời mọc
        sunrise = datetime.fromtimestamp(suntime["sunrise"])
        # lúc mặt trời lặn
        sunset = datetime.fromtimestamp(suntime["sunset"])
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
        Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
        nhiệt độ hiện tại là {current_temperature} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        """
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        speak("Không tìm thấy địa chỉ của bạn")
        current_weather()


# url = 'https://api.unsplash.com/photos/random?client_id=' + \
#       api_key
def change_wallpaper():
    api_key = "FjxCbKxmzTrradwyKJChv42K9dz1xMFoA6bzaryhoAo"
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
          api_key  # pic from unspalsh.com
    f = urllib.request.urlopen(url)  # lấy kết qur trả về của trang web
    json_string = f.read()  # đọc dự liệu ở trang web
    f.close()  # đóng lại trình duyệt ẩn
    parsed_json = json.loads(json_string)  # sử lý dữ liệu từ JSON to Python (dict)
    photo = parsed_json['urls']['full']  # lấy ảnh ở link urls với chất lượng full
    urllib.request.urlretrieve(photo, "G:\\OBS VIDEO\\a.png")  # tải về máy
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "G:\\OBS VIDEO\\a.png", 3)
    speak("Hình nền máy tính bạn đã được thay đổi. Bạn ra home xem có đẹp không nha ?")
    picture = get_text()
    if 'không đẹp' in picture:
        speak('Bạn muốn thay đổi lại phải không?')
        again = get_text()
        speak('Bạn cứ nói đi để tôi thay cho nhe')
        if 'có' not in again:
            change_wallpaper()
    else:
        pass

def read_news():
    # https://newsapi.org/v2/everything?q=th%E1%BB%83%20thao&apiKey=ef0edfb96bba4717b9da796b6ca7a152
    speak("Bạn muốn đọc báo về gì")
    queue = get_text()
    params = {'apiKey': 'ef0edfb96bba4717b9da796b6ca7a152', "q": queue, }
    api_result = requests.get('https://newsapi.org/v2/everything?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}")
        if number <= 3:
            webbrowser.open(result['url'])


def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        wikipedia.set_lang('vi')
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(5)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            ans = get_text()
            if "có" not in ans:
                break
            speak(content)
            time.sleep(5)

        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")


def main_brain():
    speak("xin chào bạn tên là gì vậy ạ??")
    name = get_text()
    if name:
        speak(f'xin chào bạn {name}.')
        hello(name)
        speak(f'Bạn cần bot giúp gì không ạ: ')
        while True:
            text = get_text()
            if not text:
                break
            elif "tạm biệt" in text or "hẹn gặp lai" in text:
                stop()
                break
            elif 'thực hiện' in text:
                help_me()
            elif 'hiện tại' in text:
                get_time(text)
            elif "mở" in text:
                if "ứng dụng" in text:
                    open_app(text)
                    if input("Để tiếp tục y/n: ") == "y":
                        pass
                elif "." in text:
                    open_web(text)
            elif "google" in text:
                open_google_search()
            elif 'youtube' in text:
                speak("Bạn muốn tìm kiếm đơn giản hay phức tạp")
                yeu_cau = get_text()
                if "đơn giản" in yeu_cau:
                    open_youtube_search()
                    if input("Để tiếp tục y/n: ") == "y":
                        pass
                elif "phức tạp" in yeu_cau:
                    open_youtube_2()
                    if input("Để tiếp tục y/n: ") == "y":
                        pass
            elif "thời tiết" in text:
                current_weather()
            elif "hình nền" in text:
                change_wallpaper()
                if input("Để tiếp tục y/n: ") == "y":
                    pass
            elif "đọc báo" in text:
                read_news()
                if input("Để tiếp tục y/n: ") == "y":
                    pass
            elif "định nghĩa" in text:
                tell_me_about()
            else:
                speak(f'chắc năng này chưa có bạn vui lòng chọn lại sau nha <..>')
main_brain()
