import streamlit as st
import stripe
from urllib.parse import parse_qs, urlparse
import json
from authorize import autor
from authorize import hash_password
from datetime import datetime



def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password
    
    
    
if 'admin' not in st.session_state:
    st.session_state.admin = False
    
        
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
st.title('Buy premium subscription') 



with open('coins.json','r') as file:
    cn = json.load(file)

st.write(f"Your amount of coins is 🪙💰 {cn[st.session_state.username]}")    
def unsub_bec_time():
    st.session_state.premium = False
    
    
    
    with open('premium.json','r') as file:
        pr = json.load(file)
    
    
    
    
    pr[st.session_state.username] = "Standart"
    
    
    with open('premium.json',"w") as file:
        print('DEBUG BASE')
        json.dump(pr,file,indent=2)    
    st.error(f'Your sub is not valid')
    
            
def buy_premium():
    st.session_state.premium = True
    datetim = datetime.now()
    dt = str(datetim).split()
    dateoftime = dt[0].split('-')
    final = dateoftime[0]+'-'+'0'+str(int(dateoftime[1])+1)+'-'+dateoftime[2]
    print("DEBUG:FINAL",final)
    print("DEBUG DATE:",str(datetime.now()).split()[0])
    #print(int(dateoftime[1]) + 1)
    with open('premium.json','r') as file:
        data = json.load(file)
    
    
    if st.session_state.premium:
          data[st.session_state.username] = 'Premium'
    else:
        data[st.session_state.username] = 'Standart'
    with open('premium.json','w') as file:
        json.dump(data,file,indent = 2)                 
    print(data)
    st.success('Your 1 mouth free trial started !')
    st.success(f"Your free trial is valid until {final}")
    if final == str(datetime.now()).split()[0]:
        print('Sub should be gone')
        unsub_bec_time()    
def buy_premium_with_coins():
    st.session_state.premium = True
    datetim = datetime.now()
    dt = str(datetim).split()
    dateoftime = dt[0].split('-')
    final = dateoftime[0]+'-'+'0'+str(int(dateoftime[1])+1)+'-'+dateoftime[2]
    with open('coins.json','r') as file:
        nv = json.load(file)
    if nv[st.session_state.username] < 100:
        st.error("You dont have enought coins")
    else:
        st.success("Thanks for buying premium for 30 days") 
        nv[st.session_state.username] = nv[st.session_state.username] - 100
        with open('coins.json','w') as file:
            json.dump(nv,file,indent=2)
            print("Done") 
        with open('premium.json','r') as file:
            data = json.load(file)
        if st.session_state.premium:
            data[st.session_state.username] = 'Premium'
        else:
            data[st.session_state.username] = 'Standart'
        with open('premium.json','w') as file:
            json.dump(data,file,indent = 2)          
        if final == str(datetime.now()).split()[0]:
            print('Sub should be gone')
            unsub_bec_time()     
def unsubscribe():
    st.session_state.premium = False
    st.success('You unsubscribed')  
    with open('premium.json','r') as file:
        users = json.load(file)
    users[st.session_state.username] = 'Standart'
    
    
    with open('premium.json','w') as file:
        json.dump(users,file,indent=2) 
if not st.session_state.premium:
    st.button('Confirm',on_click=buy_premium)
    st.button("Buy premuim with coins",on_click=buy_premium_with_coins)


          
if st.session_state.premium:  
    uns = st.button('Unsubscribe',on_click=unsubscribe)
     

             
#st.title("Buy a preimium subcription and user some more functions")
#Public_key = 'public_key'
stripe.api_key = 'i hate sasha mishin'
def create_session(amount,currency='usd'):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=stripe.api_key,  # Тестовый токен (можно заменить на реальный)
            description="Платеж через Python"
        )
        return charge
    except stripe.error.StripeError as e:
        st.error(f"Error {e}")


def test():
    s = {}
    return hash(s)

if st.session_state.username == 'Ivan':
    with open('users.json','r') as file:
        al = json.load(file)
    st.write('All users')    
    st.write(al)    
### Make a pay page 


### DEBUGING AND TESTING FUNCTIONS