import os
import time
import sys
import speech_recognition as sr
import psutil
import keyboard
import pygetwindow as gw
import pyautogui
import random
from urllib.parse import quote_plus
import pytesseract
import mss
import cv2
import pyttsx3
import subprocess
import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from threading import Thread
from PIL import Image, ImageTk
import json


# Указываем путь к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

# Функция для получения случайной фразы из словаря
def get_random_phrase(action):
    if action in phrases:  # Проверяем, существует ли ключ в словаре
        return random.choice(phrases[action])
    else:
        return "Фраза для этого действия не найдена."  # На случай отсутствия ключа

# Фразы для разных действий
phrases = {
"greeting": [
        "Привет! Как я могу помочь?",
    "Здравствуйте! Чем могу быть полезен?",
    "Приветствую вас! Что вас интересует?",
    "Добро пожаловать! Какой вопрос у вас есть?",
    "Привет! Чем могу вам помочь сегодня?",
    "Здравствуйте! Что вы хотели бы узнать?",
    "Привет! Я здесь, чтобы помочь вам.",
    "Добро пожаловать! Как я могу быть полезен?",
    "Привет! Какие у вас сегодня планы?",
    "Здравствуйте! Какую задачу мне решить?",
    "Приветствую! Готова помочь с вашими запросами.",
    "Добро пожаловать! В чем могу помочь?",
    "Привет! Что вас интересует?",
    "Здравствуйте! Как я могу облегчить вашу жизнь?",
    "Привет! Если у вас есть вопросы, задавайте!",
    "Здравствуйте! Как я могу помочь вам сегодня?",
    "Привет! Я здесь, чтобы сделать ваш день лучше.",
    "Здравствуйте! Каковы ваши пожелания?",
    "Привет! Рад вас видеть! Как могу помочь?",
    "Добро пожаловать! Я готова помочь с вашим запросом.",
    "Привет! Надеюсь, ваш день проходит хорошо!",
    "Здравствуйте! Я здесь, чтобы помочь вам.",
    "Приветствую! Готова ответить на ваши вопросы.",
    "Добро пожаловать! Какую информацию вы ищете?",
    "Привет! Как я могу сделать вашу жизнь проще?",
    "Здравствуйте! Чем могу вам помочь прямо сейчас?",
    "Привет! Я здесь, чтобы помочь вам с чем угодно.",
    "Здравствуйте! Как я могу сделать ваш день лучше?",
    "Привет! Готова приступить к работе.",
    "Здравствуйте! Я здесь для вас.",
    "Привет! Какие у вас вопросы или задания?",
    "Здравствуйте! Какое у вас задание для меня?",
    "Привет! Чем могу быть вам полезна?"
    ],
    "activation": [
        "Я активирована и готова к работе!",
    "Теперь я активна! Чем могу помочь?",
    "Активация завершена! Какова ваша задача?",
    "Я на связи! Что хотите сделать?",
    "Активация прошла успешно! В чем помочь?",
    "Теперь я активна! Какой вопрос у вас?",
    "Я готова к работе! Что делать?",
    "Активация завершена! Давайте начнем.",
    "Теперь я здесь! Чем могу помочь?",
    "Я активировалась! Как я могу помочь вам?",
    "Активация прошла успешно! Какую задачу решим?",
    "Теперь я на связи! Как я могу помочь?",
    "Я активирована! Какой у вас запрос?",
    "Я готова к действиям! В чем помочь?",
    "Активация завершена! Какие у вас задачи?",
    "Теперь я здесь для вас! Как могу помочь?",
    "Я активировалась! Какой вопрос у вас?",
    "Активация прошла успешно! Давайте работать.",
    "Теперь я готова к вашим командам!",
    "Я активна и жду ваших указаний.",
    "Активация завершена! Давайте начнем.",
    "Теперь я здесь для решения ваших вопросов.",
    "Я готова к вашим командам! Что делать?",
    "Теперь я активна! Какова ваша просьба?",
    "Я активирована и готова к действиям!",
    "Активация завершена! Какой вопрос у вас?",
    "Я готова к работе! В чем помочь?",
    "Активация завершена! Я здесь, чтобы помочь.",
    "Я активирована! Какой вопрос у вас?",
    "Активация успешна! Жду ваших указаний.",
    "Я готова выполнять ваши команды!",
    "Активация прошла успешно! Чем могу помочь?",
    "Я на связи и готова помочь вам!"
    ],
    "deactivation": [
        "Я деактивируюсь. Если что-то понадобится, просто позовите!",
    "Деактивация завершена. Удачи вам!",
    "Я отключаюсь. Если понадобится помощь, обращайтесь!",
    "Деактивация завершена. Буду ждать вашего вызова.",
    "Я выключаюсь. Возвращайтесь, когда будете готовы.",
    "Сейчас я деактивируюсь. Всего хорошего!",
    "Я отключаюсь. Надеюсь, скоро увидимся снова!",
    "Деактивация завершена. Удачи в делах!",
    "Я ухожу на отдых. Позовите меня, когда будете готовы.",
    "Сейчас я отключусь. Буду ждать вашего возвращения!",
    "Я деактивируюсь. Желаю вам хорошего дня!",
    "Я отключаюсь. Если что-то понадобится, просто позовите!",
    "Деактивация завершена. Всегда рада помочь!",
    "Я на время отключаюсь. Удачи вам!",
    "Я выключаюсь. До скорой встречи!",
    "Сейчас я деактивируюсь. Обращайтесь, когда нужно!",
    "Я отключаюсь. Берегите себя!",
    "Деактивация завершена. Жду вашего возвращения!",
    "Сейчас я ухожу. Если что-то нужно, дайте знать!",
    "Я отключаюсь. Буду ждать вашего вызова.",
    "Деактивация завершена. Успехов вам!",
    "Я на время отключаюсь. Если нужно, позовите!",
    "Сейчас я деактивируюсь. Всегда рада помочь!",
    "Я отключаюсь. Если что-то нужно, обращайтесь!",
    "Деактивация завершена. До скорой встречи!",
    "Я выключаюсь. Удачи вам во всем!",
    "Я на время отключаюсь. Буду ждать вашего возвращения.",
    "Деактивация завершена. Надеюсь, скоро увидимся!",
    "Я отключаюсь. Если потребуется помощь, обращайтесь!",
    "Сейчас я деактивируюсь. Всего наилучшего!",
    "Я выключаюсь. Если что-то понадобится, просто позовите!"
    ],
    "click": [
        "Нажимаю.",
        "Сейчас нажму.",
        "Кликаю.",
        "Делаю клик.",
        "Вот нажимаю.",
        "Скоро нажму.",
        "Нажимаю на элемент.",
        "Приступаю к нажатию.",
        "Кликаю прямо сейчас.",
        "Давайте нажмем.",
        "Я нажимаю.",
        "Выполняю клик.",
        "Сейчас кликну.",
        "Сейчас активирую.",
        "Вот и клик.",
        "Уже нажимаю."
    ],
    "vpn_connect": [
        "Подключаю VPN, всё будет как по маслу!",
        "VPN на старте, жди соединения!",
        "Сейчас подключу VPN, подожди минутку.",
        "Погружаемся в анонимность с VPN!",
        "Запускаю VPN, почти готово!",
        "VPN включён, могу помогать!",
        "Уже подключаю VPN, не волнуйся!",
        "Соединяюсь через VPN, подожди.",
        "VPN готов к работе, вперёд!",
        "VPN на связи, теперь ты под защитой!",
        "Скоро будет подключение, подожди немного.",
        "Настраиваю VPN, оставайся на линии.",
        "Подключение в процессе, скоро всё будет!",
        "Почти готово, подождите ещё чуть-чуть!",
        "VPN соединение — это мой конёк!",
        "Настраиваю защиту, следи за процессом."
    ],
    "vpn_disconnect": [
        "Отключаю VPN, жди...",
        "VPN больше не нужен? Сейчас отключу.",
        "Закрываю VPN, снова в обычном режиме!",
        "VPN отключён, связь нормальная.",
        "Выключаю VPN, как скажешь!",
        "VPN выключен, теперь в обычном режиме!",
        "Отсоединяюсь от VPN, готово.",
        "Отключаю VPN, давай по старинке.",
        "VPN выключен, можешь расслабиться!",
        "VPN отключён, теперь без шифрования.",
        "Даю свободу интернету, отключаю VPN.",
        "VPN отключён, всё снова открыто.",
        "Всё, связь восстановлена, VPN отключён.",
        "Виртуальная защита выключена, возвращаюсь в реальность.",
        "VPN больше не защищает, мы в свободном доступе.",
        "VPN отключен, наслаждайся свободой!"
    ],
    "open_website": [
        "Открываю сайт, держись!",
        "Сейчас загружу сайт, подожди немного!",
        "Уже открываю, секунду...",
        "Подключаюсь к нужному сайту, готово!",
        "Сайт почти готов, открываю!",
        "Сейчас всё загружу, момент...",
        "Уже в процессе открытия сайта!",
        "Начинаю загрузку сайта, секунду.",
        "Сайт на подходе, скоро будет открыт!",
        "Вот-вот откроется сайт, жди.",
        "Загружаю страницу, не переключайся!",
        "Скоро открою сайт, оставайся с нами.",
        "Подожди немного, сайт загружается.",
        "Почти готово, сайт уже на подходе.",
        "Открываю браузер, сайт сейчас откроется.",
        "Сейчас все откроется, не переживай!"
    ],
    "not_found": [
        "Что-то не могу найти это на экране...",
        "Не вижу, чтобы это тут было...",
        "Не нахожу, попробуй ещё раз!",
        "Где это? Не вижу...",
        "Хм, кажется, этого тут нет.",
        "Не нахожу это на экране, сорри!",
        "Где это? Что-то не видно.",
        "Не нашла, попробуй ещё раз.",
        "Это исчезло с экрана?",
        "Кажется, этого тут не видно.",
        "Что-то не нашлось, проверь ещё раз.",
        "Кажется, это ускользнуло от меня.",
        "Не вижу, где это находится.",
        "Не нашла нужный элемент на экране.",
        "Проблема с нахождением элемента, проверь ещё раз.",
        "Не нашлось, возможно, это скрыто."
    ],
    "general_error": [
        "Упс! Что-то пошло не так...",
        "Кажется, что-то сломалось...",
        "Что-то тут не так, проверь ещё раз.",
        "Сбой в системе, что-то не то!",
        "Ой! Произошла ошибка.",
        "Похоже, что-то пошло не по плану.",
        "Небольшая проблема, проверю.",
        "Что-то не получилось...",
        "Не выходит... Проверь ещё раз.",
        "Упс! Похоже, ошибка.",
        "Неожиданная ошибка, дайте мне минутку.",
        "Ошибка системы, проверяю проблему.",
        "Кажется, возникла проблема, нужно разобраться.",
        "Не удалось выполнить действие, проверьте настройки.",
        "Проблема с выполнением команды, попробуйте еще раз.",
        "Техническая ошибка, дайте знать, если что-то не так."
    ]
}

# Активирующие слова для Мику
activation_words = ["мику", "мико", "микуша", "микочка", "микуся", "мик", "микочка"]

deactivation_words = ["спасибо", "хватит", "стоп"]

# Инициализация голосового движка pyttsx3
engine = pyttsx3.init()

# Настройки голоса (добавляем более высокий тон, чтобы приблизиться к характерному звучанию Мику)
engine.setProperty('rate', 160)  # Скорость речи
voices = engine.getProperty('voices')
# Используем женский голос, который максимально напоминает голос Мику
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Функция для озвучивания текста через женский голос
def speak(text):
    engine.say(text)
    engine.runAndWait()


def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, корректно работает в PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Словарь для хранения ресурсов
resources = {
    "miku": resource_path("resources/miku.png"),
    "icn": resource_path("resources/Miku.ico"),
    "1monitor": resource_path("resources/1monitor.png"),
    "2monitor": resource_path("resources/2monitor.png"),
    "connect_button": resource_path("resources/connect_button.png"),
    "disconnect_button": resource_path("resources/disconnect_button.png"),
    "info_button": resource_path("resources/info_button.png"),
    "search_youtube": resource_path("resources/search_youtube.png"),
    "search_youtube_2": resource_path("resources/search_youtube_2.png"),
    "settings_button": resource_path("resources/settings_button.png"),
    "white_search": resource_path("resources/white_search.png"),
}

# Словарь для хранения загруженных изображений
loaded_images = {}

def load_images():
    try:
        # Загружаем изображения и сохраняем их в loaded_images
        for key, path in resources.items():
            loaded_images[key] = Image.open(path)
            print(f"Загружено изображение: {key} из {path}")  # Отладочная информация
        print("Все изображения загружены успешно")
    except FileNotFoundError as e:
        print(f"Ошибка загрузки изображения: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


# Вызов функции для загрузки изображений
load_images()

# Функция для получения голосовой команды через PyAudio
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Ошибка сервиса распознавания речи.")
            return ""
        except sr.WaitTimeoutError:
            return ""


# Глобальная переменная для хранения пути к браузеру
browser_path = ""
config_file = "resources/config.json"

def load_settings():
    global browser_path
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            settings = json.load(file)
            browser_path = settings.get("browser_path", "")
            print(f"Загружен путь к браузеру: {browser_path}")

# Функция для выбора браузера
def choose_browser():
    global browser_path
    # Открываем диалог выбора файла
    browser_path = filedialog.askopenfilename(title="Выберите браузер", filetypes=[("Executable Files", "*.exe")])
    if browser_path:
        print(f"Выбранный браузер: {browser_path}")

# Функция для запуска выбранного браузера
def start_browser():
    if browser_path:
        subprocess.Popen([browser_path])
        time.sleep(10)  # Ждем, пока браузер запустится
    else:
        print("Браузер не выбран.")

# Функция для поиска текста на экране и нажатия на него
screenshot_folder = "screenshots"
os.makedirs(screenshot_folder, exist_ok=True)


# Функция для поиска текста на экране и нажатия на него
def click_on_text(target_text, monitor_index):
    try:
        with mss.mss() as sct:
            # Захватываем указанный монитор
            monitor = sct.monitors[monitor_index]
            screenshot = sct.grab(monitor)
            screenshot_path = os.path.join(screenshot_folder, f"monitor_{monitor_index}.png")
            # Сохраняем скриншот в файл
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)

            # Загружаем изображение и обрабатываем его
            img = cv2.imread(screenshot_path)

            # Используем Tesseract для распознавания текста и его координат
            data = pytesseract.image_to_data(img, lang='rus', output_type=pytesseract.Output.DICT)
            for i in range(len(data['text'])):
                if target_text.lower() in data['text'][i].lower():
                    if len(data['left']) > i and len(data['top']) > i and len(data['width']) > i and len(data['height']) > i:
                        x, y, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        pyautogui.click(x + width / 2, y + height / 2)
                        speak(get_random_phrase("click"))
                        # Удаляем скриншот после нажатия
                        os.remove(screenshot_path)
                        return
            speak(get_random_phrase("not_found"))
            # Удаляем скриншот после неудачного поиска
            os.remove(screenshot_path)
    except Exception as e:
        speak(get_random_phrase("general_error"))
        print("Ошибка при нажатии на текст:", e)

def open_website(site_name):
    try:
        # Проверяем, запущен ли браузер
        browser_window = None
        for window in gw.getWindowsWithTitle(os.path.basename(browser_path).replace(".exe", "")):
            if os.path.basename(browser_path).replace(".exe", "").lower() in window.title.lower():
                browser_window = window
                break

        if not browser_window:
            # Если браузер не запущен, то запускаем его
            start_browser()
            browser_window = gw.getWindowsWithTitle(os.path.basename(browser_path).replace(".exe", ""))[0]

        # Разворачиваем окно и активируем его
        if browser_window:
            if not browser_window.isMaximized:
                browser_window.maximize()  # Разворачиваем окно, если оно свернуто
            browser_window.activate()  # Активируем окно
            time.sleep(1)  # Ждем, чтобы окно стало активным
            savescum = browser_window.title.lower()
            # Используем горячие клавиши для перехода по вкладкам и поиска нужного сайта
            while True:
                if site_name.lower() in browser_window.title.lower():
                    speak(get_random_phrase("open_website"))
                    return
                keyboard.press_and_release('ctrl+PageDown')
                time.sleep(0.5)
                if savescum in browser_window.title.lower():
                    break

            # Если сайт не найден, открываем новую вкладку
            keyboard.press_and_release('ctrl+t')  # Открываем новую вкладку
            time.sleep(1)
            keyboard.write(f'https://www.google.com/search?q={quote_plus(site_name)}', delay=0.05)
            keyboard.press_and_release('enter')
            time.sleep(2)  # Ждем загрузки результатов поиска
            keyboard.press_and_release('tab')
            time.sleep(1)
            keyboard.press_and_release('enter')
            keyboard.press_and_release('enter')
            speak(get_random_phrase("open_website"))
        else:
            speak(get_random_phrase("not_found"))
    except Exception as e:
        speak(get_random_phrase("general_error"))
        print(e)

def back():
    # Имитация кнопки "Назад"
    pyautogui.press('browserback')

def forward():
    # Имитация кнопки "Вперед"
    pyautogui.press('browserforward')

def change_window():
    #одноразовый альтаб
    keyboard.press_and_release('alt+tab')

def double_click():
    # Имитация двойного щелчка левой кнопкой мыши
    pyautogui.doubleClick()

def smiv():
    #сворачивает окна часто багичи случаются
    keyboard.press('win')
    keyboard.press_and_release('m')
    time.sleep(0.3)
    keyboard.release('win')

def ravorot():
    #разворачивает все окна обратно но бывают баги
    keyboard.press_and_release('win+shift+m')

def monitor1():
    # это для тех у кого два моника чтобы дублировать их часто багуется кста из-за кнопки win
    keyboard.press('win')
    keyboard.press_and_release('p')
    keyboard.release('win')
    time.sleep(1)
    mon_button_location = pyautogui.locateOnScreen(loaded_images["1monitor"])
    if mon_button_location:
        pyautogui.click(pyautogui.center(mon_button_location))
    time.sleep(1)
    keyboard.press_and_release('enter')
    keyboard.press_and_release('esc')

def monitor2():
    # это для тех у кого два моника чтобы снова их расширить часто багуется кста из-за кнопки win
    keyboard.press('win')
    keyboard.press_and_release('p')
    keyboard.release(('win'))
    time.sleep(1)
    mon_button_location = pyautogui.locateOnScreen(loaded_images["2monitor"])
    if mon_button_location:
        pyautogui.click(pyautogui.center(mon_button_location))
    time.sleep(1)
    keyboard.press_and_release('enter')
    keyboard.press_and_release('esc')

def close():
    #закрываем активное окно
    keyboard.press_and_release('alt+f4')

def pause():
    #паузим видосик
    keyboard.press_and_release('space')

def full_window():
    #разворачиваем видосик на фулл экран
    keyboard.press_and_release('f')

def write(text):
    #вбиваем текст с клавы
    keyboard.write(text)

def close_tab():
    #закрываем вкладку браузера
    keyboard.press_and_release('ctrl+w')

def search():
    # функция для поиска на ютубе
    try:
        # Проверяем каждую кнопку отдельно
        search_button_location = None
        try:
            search_button_location = pyautogui.locateOnScreen(loaded_images["search_youtube"])
        except Exception as e:
            print("Ошибка при поиске 'search_youtube.png':", e)

        search_button_light = None
        try:
            search_button_light = pyautogui.locateOnScreen(loaded_images["white_search"])
        except Exception as e:
            print("Ошибка при поиске 'white_search.png':", e)

        search_button_2 = None
        try:
            search_button_2 = pyautogui.locateOnScreen(loaded_images["search_youtube_2"])
        except Exception as e:
            print("Ошибка при поиске 'search_youtube_2.png':", e)

        # Проверка и клик
        if search_button_location is not None:
            pyautogui.click(pyautogui.center(search_button_location))
            keyboard.press_and_release('ctrl+a')
            keyboard.press_and_release('backspace')
        elif search_button_light is not None:
            pyautogui.click(pyautogui.center(search_button_light))
            keyboard.press_and_release('ctrl+a')
            keyboard.press_and_release('backspace')
        elif search_button_2 is not None:
            pyautogui.click(pyautogui.center(search_button_2))
            keyboard.press_and_release('ctrl+a')
            keyboard.press_and_release('backspace')
        else:
            print("Не удалось найти ни одну кнопку.")
            return  # Выход из функции, ничего не делаем
    except Exception as e:
        speak(get_random_phrase("general_error"))
        print("Ошибка:", e)  # Дополнительно выводим ошибку для отладки



def acces():
    # Чисто ентер нажать
    keyboard.press_and_release('enter')


# Основная функция для обработки команд и диалогов
def handle_command(command):
    if "введи" in command:
        text = command.replace("введи","").strip()
        write(text)
    elif "поиск" in command:
        search()
    elif "открой" in command:
        site_name = command.replace("открой", "").strip()
        open_website(site_name)
    elif "нажми" in command:
        target_text = command.replace("нажми", "").strip()
        click_on_text(target_text, 1)
    elif "вперёд" in command:
        forward()
    elif "назад" in command:
        back()
    elif "смени окно" in command:
        change_window()
    elif "дважды" in command:
        double_click()
    elif "сверни окна" in command:
        smiv()
    elif "разверни окна" in command:
        ravorot()
    elif "монитор 1" in command:
        monitor1()
    elif "монитор 2" in command:
        monitor2()
    elif "закрой окно" in command:
        close()
    elif "пауза" in command:
        pause()
    elif "полный экран" in command:
        full_window()
    elif "подтвердить" in command:
        acces()
    elif "закрой вкладку" in command:
        close_tab()
    elif "убей" in command:
        close()



active_mode = False


def start_listening():
    global active_mode
    active_mode = True
    speak(get_random_phrase("activation"))

    while active_mode:  # Главный цикл прослушивания
        command = listen()
        if any(word in command for word in deactivation_words):
            stop_listening()
        elif active_mode:
            handle_command(command)


def stop_listening():
    global active_mode
    active_mode = False
    speak(get_random_phrase("deactivation"))

def save_settings(self):
    with open(config_file, 'w') as file:
        json.dump({"browser_path": browser_path}, file)
        print("Настройки сохранены.")

class MikuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Miku Assistant")
        self.root.geometry("400x600")
        self.root.resizable(False, False)  # Запретить изменение размера окна
        self.root.iconbitmap(resources["icn"])  # Используйте путь к файлу иконки
        load_settings()

        # Загрузка и настройка изображения
        image_miku = loaded_images["miku"]  # Укажите путь к изображению
        image_miku = image_miku.resize((200, 300), Image.LANCZOS)  # Измените размер по желанию
        self.photo_miku = ImageTk.PhotoImage(image_miku)  # Сохраняем ссылку на изображение в атрибуте экземпляра

        miku_label = tkinter.Label(root, image=self.photo_miku)  # Используем self.photo_miku
        miku_label.pack(pady=20)

        self.is_running = False  # Изначально помощник выключен

        # Создаем рамку для кнопки с другим фоном
        self.button_frame = tkinter.Frame(root, bg="#ffffff")  # Цвет фона для рамки
        self.button_frame.pack(side='bottom', fill='x', pady=10)  # Устанавливаем рамку внизу

        # Создаем кнопку, которая будет изменяться
        self.toggle_button = tkinter.Button(self.button_frame, text="Включить", command=self.toggle, width=20, height=50, font=("Helvetica", 16), bg="#0000CC", fg="white")
        self.toggle_button.pack(side='bottom', pady=100)

        info_image = loaded_images["info_button"]  # Укажите путь к изображению кнопки
        info_image = info_image.resize((50, 50), Image.LANCZOS)  # Измените размер по желанию
        self.photo_info = ImageTk.PhotoImage(info_image)

        # Кнопка настроек с изображением
        settings_image = loaded_images["settings_button"]  # Укажите путь к изображению кнопки
        settings_image = settings_image.resize((50, 50), Image.LANCZOS)  # Измените размер по желанию
        self.photo_settings = ImageTk.PhotoImage(settings_image)

        self.settings_button = tkinter.Button(root, image=self.photo_settings, command=self.open_settings,
                                              borderwidth=0)
        self.settings_button.place(relx=0.05, rely=0.05, anchor='nw')  # Левый верхний угол

        self.browser_path = ""  # Путь к браузеру

        self.info_button = tkinter.Button(root, image=self.photo_info, command=self.show_info, borderwidth=0)
        self.info_button.place(relx=0.95, rely=0.05, anchor='ne')  # Правый верхний угол

    def toggle(self):
        self.is_running = not self.is_running  # Переключаем состояние
        if self.is_running:
            self.start()
        else:
            self.stop()

    def start(self):
        self.toggle_button.config(text="Выключить")  # Меняем текст кнопки
        # Запускаем поток для прослушивания
        Thread(target=self.run_start, daemon=True).start()

    def stop(self):
        self.toggle_button.config(text="Включить")  # Меняем текст кнопки
        self.run_stop()  # Останавливаем прослушивание

    def run_start(self):
        start_listening()
        print("Помощник включен и начинает прослушивание...")

    def run_stop(self):
        stop_listening()
        print("Помощник выключен и останавливает прослушивание...")


    def show_info(self):
        messagebox.showinfo("Информация", "Тоса создатель.")

    def open_settings(self):
        settings_window = tkinter.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)


        # Кнопка выбора пути к браузеру
        browser_button = tkinter.Button(settings_window, text="Выбрать Браузер", command=self.select_browser)
        browser_button.pack(pady=10)

        # Кнопка для сохранения настроек
        save_button = tkinter.Button(settings_window, text="Сохранить", command=self.save_settings)
        save_button.pack(pady=10)


    def select_browser(self):
        global browser_path
        browser_path = filedialog.askopenfilename(title="Выберите Браузер",
                                                       filetypes=[("Executable files", "*.exe"), ("All files", "*.*")])
        if browser_path:
            self.save_settings()

    def save_settings(self):
        # Сохраняем настройки в файл конфигурации
        with open(config_file, 'w') as file:
            json.dump({"browser_path": browser_path}, file)
            print("Настройки сохранены.")

if __name__ == "__main__":
    root = tkinter.Tk()
    app = MikuApp(root)
    root.mainloop()