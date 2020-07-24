import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import time
import os
import sys
import subprocess
import datetime


opts = {
    "alias" :('nox', 'нокс', 'бокс','max','макс','мопс','люкс','linux','Люнукс','курс','нукс'),
    "tbr"   :('скажи','произнеси','озвучь','сколько','расскажи','у нас'),

    "cmds"  :{
        "ctime" :('время','текущее время','которы час','сейчас времени'),
        "radio" :('включи радио','запусти радио','включи музыку','воспроизвести музыку'),
        "stipid":('расскажи анегдот','ты знаешь анегдот','рассмеши','анекдот расскажи'),
        "good"  :('кто хороший', 'хороший бот','кто хороший бот','хороший год')
        }

    }


# Распознавание НЕЧЕТКОЕ команды при помощи fuzzywuzzy
def recognizer_cmd(cmd):
    # НЕЧЕТКОЕ сравнение полученой команды из ячейки настроек cmds
    RC = {'cmd':'','percent':0}

    # Получаем Ключи и Значения ячейкир настроек cmds, (нас интересуют только значения, ключ будет нуден когда мы узнаем ЗНАЧЕНИЕ)
    for c,v in opts['cmds'].items():

        # Проверяем НЕЧЕТКОЕ совпадения команды и Значения
        for x in v:
            vrt = fuzz.ratio(cmd,x)

            # И оставляем самую похожую на то что произнес пользователь команду
            if vrt > RC['percent']:
                # Выбираем КЛЮЧ-команду которму соответсвует комманда-значение
                RC['cmd'] = c

                RC['percent'] = vrt     # [log] Распознано мопс время {'cmd': 'ctime', 'percent': 67}
                #print(RC)
    return RC

# Исполнение команды
def execute_cmd(cmd):


    # Сказать текущее время (узнать время кодом, передать на озвучку помошнику полученую строку)
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Сейчас ' + str(now.hour)+' : ' + str(now.minute))


    # Воспроизвести Радио
    elif cmd == 'radio':
        os.system('E:/Python/Projects/NOX/09f85c8c0e74.mp3')


    # Расказать анегдот
    elif cmd == 'stupid':
        speak('Ни один анегдот пока не загружен')


    # Расказать анегдот
    elif cmd == 'good':
        speak('Я хороший бот')



    else:
        print('Команда не распознана, пожалуйста повторите')
        speak('Команда не распознана, пожалуйста повторите')




# Говорить (функция произнесения помошником полученых из кода текстовых (str) данных)
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


# РАСПОЗНАВАНИЕ ГОЛОСОВОЙ КОМАНДЫ\ её обработка\ вывод результатов  через GOOGLE распознаватель голоса. А если Гугл Сервер будет сбоить то перезапуск подключения к API Googla
def process():
    try:
        while True:
            with m as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                result = r.recognize_google(audio, language='ru-RU').lower()
                result = result.lower()
                print(f'{result}')

                if result.startswith(opts["alias"]):

                    # Обращение к помошнику полной фразой
                    cmd = result
                    # Очистка команды для Обращение к NOX(cmd) ЧИСТОЙ КОМАНДОЙ без лишнего шума( имен , слов паразитов и т.д.)
                    for x in opts['alias']:
                        cmd.replace(x, '').strip()
                    for x in opts['tbr']:
                        cmd.replace(x, '').strip()

                    # Распознавание оставшейся ЧИСТОЙ КОМАНДЫ (cmd)
                    cmd = recognizer_cmd(cmd)
                    # ИСПОЛНЕНИЕ оставшейся ЧИСТОЙ КОМАНДЫ (cmd)
                    execute_cmd(cmd['cmd'])

    except Exception as e:
        print(e)
        print('Сбой Сервера Гугл, перезапуск программы')


# Начало
# Запуск Распознавания голоса
r = sr.Recognizer()
# Выбор устройства для передачи голоса (микрофон)
m = sr.Microphone(device_index = 1)


#Обработка команды
# Используем  выбраный микрофон для распознавания голоса
with m as source:
    r.adjust_for_ambient_noise(source)




#-------------------------------------------------------------------------------------------------------
# Голос Помошника
speak_engine = pyttsx3.init()

# Дефалтный помошник, ВАЖНО перевести на РУССКИЙ язык текста иначе будет распознавать только английский!( в реестре можно глянуть остальыне языки)
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
speak_engine.setProperty('voice', ru_voice_id)


#------------------------------------------------------------------------------------------------------


speak('Добрый День, Нокс активен')


# Запуск процесса, и если процесс зазбоит то перезапуск его.
while True:
    process()
