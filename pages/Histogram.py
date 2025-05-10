import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
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

data = np.random.rand(1000)
fig = plt.figure()
plt.hist(data,bins = 30)
with st.sidebar:
    title = st.text_input("Enter the title")
plt.title(title)
st.pyplot(fig)
### New page