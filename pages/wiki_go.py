import wikipedia as wk
import streamlit as st
#print(wk.summary("Java programming language"))
from authorize import autor
import json
# ====LOGIN PAGE ====
def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password
    
    
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False 
if not st.session_state.logged_in:
    # Переключатель между формами входа и регистрации
    if st.session_state.show_register:
        st.title("📝 Регистрация")
        new_username = st.text_input("Новый логин", key="reg_user")
        new_password = st.text_input("Новый пароль", type="password", key="reg_pass1")
        confirm_password = st.text_input("Повторите пароль", type="password", key="reg_pass2")
        
        if st.button("Зарегистрироваться"):
            if not new_username or not new_password:
                st.error("Заполните все поля")
            elif new_password != confirm_password:
                st.error("Пароли не совпадают!")
            elif new_username in st.session_state.get('users', {}):
                st.error("Пользователь уже существует")
            else:
                register_user(new_username, new_password)
                st.success("Регистрация успешна! Можете войти")
                st.session_state.show_register = False
                with open('/Users/ivanvinogradov/GraphPlot2/users.json','r', encoding="utf-8") as file:
                    data = json.load(file)
                    
                data[new_username] = new_password # записываем нового пользователя 
                
                
                
                # Запись в базу нового пользователя (уже обновляем базу)
                with open('/Users/ivanvinogradov/GraphPlot2/users.json','w', encoding="utf-8") as file:
                    json.dump(data,file,indent=4, ensure_ascii=False)
                       
                    
                    
                    
        if st.button("← Назад к входу"):
            st.session_state.show_register = False
            st.rerun()
    
    else:
        # Форма входа
        st.title("🔒 Вход в систему")
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        
        if st.button("Войти"):
            if autor(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Неверные данные")
        
        if st.button("Создать новый аккаунт"):
            st.session_state.show_register = True
            st.rerun()
    
    st.stop()

# Основной интерфейс после авторизации
st.success(f"✅ Добро пожаловать, {st.session_state.username}!")    
            
st.markdown("""Wikipedia Search App
This is a simple Streamlit application that allows users to search for any topic using the Wikipedia API.
The app displays a summary of the requested topic or shows an error message if the topic is not found.""")
task = st.text_input("Enter what you want to find")
if task != '':
    try:  
        res = st.text(wk.summary(task))
    except Exception as e:
        st.error("Nothing was found (try searching more correctly)")    
