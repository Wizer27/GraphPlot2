import os
import json
import streamlit as st

from authorize import autor



# ===== LOGIN PAGE ===== 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.title("🔒 Вход в систему")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        if autor(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            #st.experimental_rerun()  # Обновляем страницу
        else:
            st.error("Неверный логин или пароль")
    st.stop()  # 🔒 Без входа — ничего не запускается дальше

# 🟢 Если авторизован — запускаем интерфейс приложения
st.success(f"✅ Привет, {st.session_state.username}!")     

st.title("History of plots")
if os.path.exists('/Users/ivanvinogradov/GraphPlot2/pages/data.json'):
    with open('/Users/ivanvinogradov/GraphPlot2/pages/data.json') as file:
        history = json.load(file)
    for item in reversed(history):
         st.markdown(f"""
        - 🧮 **Formula:** `{item['formula']}`  
        """)
         st.markdown("---") 
    if not history:
        st.info("History is empty")
             