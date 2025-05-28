import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import numexpr as ne
#from easyocr import Reader
from pypdf import PdfReader
import re
from mpl_toolkits.mplot3d import Axes3D
import json
import os
import random 
from authorize import autor
from authorize import hash_password
from datetime import datetime
import time
import cv2, sounddevice as sd, socket, os, subprocess
# файлик с авторизацией
# ===== LOGIN PAGE =====




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
with open('coins.json','r') as t:
    ust = json.load(t)
        
if st.session_state.username not in ust:
    ust[st.session_state.username] = 0
    with open('coins.json','w') as g:
        json.dump(ust,g,indent=2)
            
def safe_evaluate(expr, variables=None):
    """Безопасная замена ne.evaluate() с ограниченным набором функций"""
    allowed_functions = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': abs

    }
    local_dict = {**(variables or {}), **allowed_functions}
    return ne.evaluate(expr, local_dict=local_dict, global_dict={})
def replace_abs_notation(expression):
    """Заменяет |x| на abs(x) в выражении (оригинальная функция без изменений)"""
    stack = []
    result = []
    i = 0
    n = len(expression)

    while i < n:
        if expression[i] == '|':
            if stack:
                stack.pop()
                result.append(')')
            else:
                stack.append('|')
                result.append('abs(')
            i += 1
        else:
            result.append(expression[i])
            i += 1
    result = ''.join(result).replace('^', '**')
    for i in range(len(result)):
        if result[i] == 'x' and (result[i - 1].isdigit() or result[i-1] == ')'):
            result = result[:i] + '*' + result[i:]
            result = ''.join(result)
        if result[i] == 'x' and (result[i + 1] == '(' or result[i + 1].isdigit()):
            print('2')
            result = result[:i+1] + '*' + result[i:]
            result = ''.join(result)
    return result

def replace(expression):
    expression = re.sub(r'\|(.+?)\|', r'abs(\1)', expression)
    # Добавление * между числом и x (например, 2x → 2*x)
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)
    # Замена ^ на **
    expression = expression.replace('^', '**')
    return expression
# Streamlit интерфейс (без изменений)   

with st.sidebar:
    x_min = st.number_input("Minimum", value=-20)
    x_max = st.number_input("Maximum", value=20)
    steps = st.slider("Amount of dots", 50, 500)
    d_gr = st.text_input("Enter the fucntion for 3d plot:",value = 'x')
    grid = st.checkbox("Grid")
    x = linspace(x_min, x_max, steps) 
    ys = [] #список всех формул
    dur = 5
    fs = 44100
    #recording = sd.rec(int(dur * fs), samplerate=fs, channels=2)
    #sd.wait()
    #sd.write("C:\\Temp\\mic.wav", recording, fs)
    count = st.number_input("How many Formulas: ",min_value = 1,max_value = 20)
    logs = []
    coins = 0
    cnis = []
    # ========= БАЗА ДАННЫХ ГРАФИКОВ ========= 
    formulas = []
    for i in range(count):
        forl = st.text_input(f'Enter the formula {i + 1}',key = f"Formula{i}")
        formulas.append(forl)
        try:
            if  forl != '' and f"Formula{i}" not in st.session_state.processed:
                st.session_state.processed.add(f"Formula{i}")
                #ys.append(safe_evaluate(replace(forl),{'x':x}))
                coins += 1 
                #cnis.append(coins)
                with open('coins.json', 'r+') as file:
                    cn = json.load(file)
                    cn[st.session_state.username] += 1
                    file.seek(0)
                    json.dump(cn, file, indent=2)
                    file.truncate() 
        except:
            st.error('Something went wrong')  
        if forl != '':
            try:
                ys.append(safe_evaluate(replace(forl),{'x':x}))
            except:
                st.error('Plot is not working')          
    with open('dt2.json','r') as file:
        try:
            data = json.load(file)
        except:
            print('Loading is not working')
    user_ex = False
    for user in data:
        if user["username"] == st.session_state.username:
            user['formulas']+=formulas
            user_ex = True
    if not user_ex:
        if st.session_state.username != '' and formulas != []:
            data.append({
                "username":st.session_state.username,
                "formulas":formulas
            })
    with open('dt2.json','w') as file:
        json.dump(data,file,indent=2,ensure_ascii=False)                
                           
    file = st.file_uploader("Chose a formula from file")         
    #Описание графиков 1 для обычного 2d графика
    description = st.empty()   
    if  'sin' in forl:
        print('Синус')
        description.text("Синус - это тригонометрическая функция, которая описывает колебания.")
    elif 'cos' in forl:
        description.text("Косинус - это тригонометрическая функция, которая также описывает колебания, но со сдвигом фазы.")
    elif 'tan' in forl:
        description.text("Тангенс - это тригонометрическая функция, которая описывает отношение синуса к косинусу.")
    elif 'exp' in forl:
        description.text("Экспонента - это функция, которая описывает экспоненциальный рост или затухание.")
    elif 'log' in forl:
        description.text("Логарифм - это функция, обратная экспоненте, которая описывает рост или затухание в логарифмической шкале.")
    elif 'sqrt' in forl:
        description.text("Квадратный корень - это функция, которая возвращает квадратный корень из числа.")
    elif 'sin' not in forl and 'cos' not in forl  and 'tan' not in forl and 'exp' not in forl and 'log' not in forl and 'sqrt' not in forl:
        description.text("Линейная функция - вида kx + b, некоторые переменные могут отсутствовать.")   
    else:
        description.text("")   
          
# ======== 3D ГРАФИК ========



with open('coins.json','r') as f:
    fil = json.load(f)
    
if st.session_state.username in fil:
    
    st.write(f"Your amount of coins is 🪙💰 {fil[st.session_state.username]}")    

            
x4 = np.linspace(x_min,x_max,steps)
try:
    y4 = safe_evaluate(replace(d_gr.lower()), {'x': x})
except Exception as e:
    st.error(f"No function for {e}")
    y4 = np.zeros_like(x4)     
x4, y4 = np.meshgrid(x4, y4)
z = np.sin(np.sqrt(x4**2 + y4**2))
fiig = plt.figure()
ax = fiig.add_subplot(projection='3d')
ax.plot_surface(x4, y4, z, cmap='viridis')
st.pyplot(fiig)             






#========= ПОСТРОЕНИЕ ГРАФИКА ИЗ ФАЙЛА ========= 
# ===== Фигура(канвас) для  2d графика ===== 
figure = plt.figure()
if grid:
    plt.grid()
if file != None:
        print(file)
        name = file.name.split('.')
        #print(name)
        #if 'jpg' in name:
            #reader = Reader(["en"])
            #im = file
            #t = reader.readtext(im,detail = 0)
           # for row in t:
               # print('-'+row)
                #if 'sin' in row:
                    #x2 = linspace(x_min,x_max,steps)
                    #try:
                        #y3 = safe_evaluate(replace(row),{'x': x})
                    #except Exception as e:
                        #st.error(f"Ошибка в формуле {e}")
                        #y3 = np.zeros_like(x)
                    #fig2 = plt.figure()
                   # plt.plot(x,y3)
        if 'pdf' in name:
            print('PDF')
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            print("PLoting from file.......")
            #x2 = linspace(x_min,x_max,steps)
            try:
                print('Working')
                y3 = safe_evaluate(replace(text),{'x':x})
            except Exception as e:
                st.error(f"Error  in the formula {e}")
                y3 = np.zeros_like(x)
            #fig2 = plt.figure()
            plt.plot(x,y3)    
            #st.pyplot(figure)
        if 'txt' in name:
            with open(file.name,'r') as file:
                c = file.read()
            print(c)    
            #if 'sin' in c:
            try:
                print('txt is here')
                y3 = safe_evaluate(replace(c),{'x':x})
            except Exception as e:
                st.error(f"Error in the formula {e}")
                y3 = np.zeros_like(x)
            plt.plot(x,y3)  
        if 'txt' not in  name and 'pdf' not in name:
            st.error("This file type is not supported yet")           
                        
def test():
    assert replace('|x-10| + 3x')

# ======== 2D ГРАФИК ========
plt.axhline(0, color='black', linewidth=1)  # Ось X (y = 0)
plt.axvline(0, color='black', linewidth=1)
for i in ys:
    plt.plot(x,i)

st.pyplot(figure) 
# биотовая функция просто для кодировки  
def bits_machine(s) -> str:
    res = ''
    for i in s:
        if i.isdigit():
            res += '1'
        if i.isalpha():
            res += '0'
        else:
            res += str(random.randint(2,100))
    return res   

def bits2(expr):
    try:
        return bin(expr)        
    except:
        return "Something went wrong"     
# декоратор для функции replace() который считает ее врямя выполнения            
def decor(func):
    def main():
        c = datetime.now()
        f = func('sin(x) - 1')
        time.sleep(1)
        v = datetime.now()
        return v - c
    return main()
print(decor(replace))        


def tests():
    pass           
            
    
