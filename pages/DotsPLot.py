import streamlit as st
import  matplotlib.pyplot as plt
from authorize import autor
from authorize import hash_password
import json



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
def exi():
    st.session_state.logged_in = False
ex = st.button("Выйти из аккаунта",on_click=exi)
if not st.session_state.premium: 
        st.title('DotsPlot')
        st.error('This is a Premium function')
        st.stop()
        
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
        x = st.text_input(f'Dot {dot+ 1}',key = f"Dotx {dot}",placeholder= '1,2')
        if x  != '':
            try:
                x = x.split(',')
                xs.append(int(x[0]))
                ys.append(int(x[1]))
            except:
                st.error('Something went wrong.Try again.')    
        #y = st.text_input(f'Doty {dot}',key = f"Doty {dot}")
        #if x != '':  
         #   xs.append(int(x))
        #if y != '':        
         #   ys.append(int(y))
print("xs:", xs)
print("ys: ", ys)    
if grid:
    plt.grid()    
if len(ys) == len(xs):    
    plt.scatter(xs, ys)
else:
    st.error("Not enough inputs !")    
st.pyplot(fig)

    