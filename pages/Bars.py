import matplotlib.pyplot as plt
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