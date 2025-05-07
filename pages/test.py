import wikipedia as wk
import streamlit as st
#print(wk.summary("Java programming language"))
task = st.text_input("Enter what you want ti find")
if task != '':
    res = st.text( wk.summary(task))