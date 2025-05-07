import wikipedia as wk
import streamlit as st
#print(wk.summary("Java programming language"))
task = st.text_input("Enter what you want to find")
if task != '':
    try:  
        res = st.text( wk.summary(task))
    except Exception as e:
        st.error("Nothing was found (try searching more correctly)")    