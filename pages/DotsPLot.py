import streamlit as st
import  matplotlib.pyplot as plt
from authorize import autor




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


fig = plt.figure()
#x = [1, 2, 3, 4]
#y = [10, 20, 25, 30]
plt.title("Диаграмма рассеяния")
xs = []
ys = []
with st.sidebar:
    grid = st.checkbox('Grid')
    count = st.number_input('How many dots?',min_value=1,max_value = 50)
    for dot in range(count + 1):
        x = st.text_input(f'Dotx {dot}',key = f"Dotx {dot}")
        y = st.text_input(f'Doty {dot}',key = f"Doty {dot}")
        if x != '':  
            xs.append(int(x))
        if y != '':        
            ys.append(int(y))
print("xs:", xs)
print("ys: ", ys)    
if grid:
    plt.grid()    
if len(ys) == len(xs):    
    plt.scatter(xs, ys)
else:
    st.error("Not enough inputs !")    
st.pyplot(fig)



