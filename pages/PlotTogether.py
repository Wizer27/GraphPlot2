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
import secrets
import string

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
option = st.radio("Choose an option:", 
                 ["Access existing conference", "Create new conference"])

if option == "Access existing conference":
    st.session_state.log_conf = True
    st.session_state.create_conf = False
    
    st.subheader("Access Conference")
    key = st.text_input("Enter the special key for conference")
    nm = st.text_input("Enter the name of conference you want to access")
    
    if st.button("Access"):
        try:
            with open("/Users/ivanvinogradov/GraphPlot2/pages/pltg.json", 'r') as file:
                pltg = json.load(file)
            
            if nm in pltg:
                if pltg[nm] == key:
                    st.success("Access granted! Conference loaded successfully.")
                    # Here you would add your logic for what happens after successful access
                    st.session_state.create_conf = True
                else:
                    st.error("Invalid key for this conference.")
            else:
                st.error("Conference with this name doesn't exist.")
        except FileNotFoundError:
            st.error("Conference database not found.")
        except json.JSONDecodeError:
            st.error("Error reading conference database.")

elif option == "Create new conference":
    st.session_state.create_conf = True
    st.session_state.log_conf = False
    
    st.subheader("Create New Conference")
    cr = st.text_input("Enter the name for new conference")
    
    if cr:
        if st.button("Create Conference"):
            if not cr.strip():
                st.warning("Conference name cannot be empty!")
            else:
                try:
                    # Generate secure key
                    key_bytes = secrets.token_bytes(32)
                    key_hex = key_bytes.hex()
                    
                    # Load existing conferences
                    try:
                        with open('/Users/ivanvinogradov/GraphPlot2/pages/pltg.json', 'r') as file:
                            pl = json.load(file)
                    except FileNotFoundError:
                        pl = {}
                    except json.JSONDecodeError:
                        pl = {}
                    
                    # Check if conference name already exists
                    if cr in pl:
                        st.error("Conference with this name already exists!")
                    else:
                        # Add new conference
                        pl[cr] = key_hex
                        
                        # Save back to file
                        with open("/Users/ivanvinogradov/GraphPlot2/pages/pltg.json", 'w') as file:
                            json.dump(pl, file, indent=2)
                        
                        st.success(f"Conference '{cr}' created successfully!")
                        st.info(f"Your access key (save this!): {key_hex}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
