import streamlit as st
import numpy as np
import plotly.figure_factory as ff
from authorize import autor
import json
# ===== LOGIN PAGE ===== 
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
    
# Add histogram data
with st.sidebar:
    st.markdown("""
### 📊 Data Distribution Visualizer

This app allows you to generate and compare random data distributions.  
You can adjust the number of values for each group, name them, and instantly see how their distributions differ.  
Perfect for statistics learning, simulation, or visualizing randomized data.
""")
    x12 = st.text_input("Enter the value1: ",value = 20)
    x22 = st.text_input("Enter the value2: ",value = 20)
    x32 = st.text_input("Enter the value3: ",value = 20)
    x1 =  np.random.randn(int(x12)) - 2
    x2 = np.random.randn(int(x22))
    x3 = np.random.randn(int(x32)) + 2
    
# Group data together
    hist_data = [x1,x2,x3]

    group_labels = [st.text_input("Name the value1: "), st.text_input("Name the value2:"), st.text_input("Name the value3:")]

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!

st.plotly_chart(fig)