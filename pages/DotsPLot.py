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



