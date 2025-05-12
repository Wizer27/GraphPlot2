import streamlit as st
import json







username = st.text_input('Username:',placeholder='Enter the username')
pasword = st.text_input('Password',placeholder='Enter the password',type = 'password')
pasword2 = st.text_input('Reenter',placeholder='Reenter the password',type = 'password')
if pasword != pasword2:
    st.error('Passwords doesnt math')
else:
    st.success('You created an account')    