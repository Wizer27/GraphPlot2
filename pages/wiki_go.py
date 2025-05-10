import wikipedia as wk
import streamlit as st
#print(wk.summary("Java programming language"))
from authorize import autor
# ====LOGIN PAGE ====
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


st.markdown("""Wikipedia Search App
This is a simple Streamlit application that allows users to search for any topic using the Wikipedia API.
The app displays a summary of the requested topic or shows an error message if the topic is not found.""")
task = st.text_input("Enter what you want to find")
if task != '':
    try:  
        res = st.text( wk.summary(task))
    except Exception as e:
        st.error("Nothing was found (try searching more correctly)")    
