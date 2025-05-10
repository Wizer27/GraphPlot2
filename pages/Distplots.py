import streamlit as st
import numpy as np
import plotly.figure_factory as ff
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