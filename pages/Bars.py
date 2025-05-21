import matplotlib.pyplot as plt
import streamlit as st
import json
from authorize import autor
from authorize import hash_password



def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password
    
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False     
# ===== LOGIN PAGE ===== ;
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
                    
                data[new_username] = hash_password(new_password) # записываем нового пользователя 
                
                
                
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
    
with st.sidebar:
    count  = st.number_input("How many bars?",min_value = 1,max_value = 20,step = 1)
    lab = []
    nums = []
    for i in range(count):
        label = st.text_input(f"Name {i+1}", key=f"Label {i}")
        value = st.number_input(f"Value {i+1}", key= f"Value {i}")
        lab.append(label)
        nums.append(value)

#Made an update
fig, ax = plt.subplots()
ax.bar(lab, nums)
st.pyplot(fig)