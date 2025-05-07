import wikipedia as wk
import streamlit as st
#print(wk.summary("Java programming language"))
st.markdown("""Wikipedia Search App
This is a simple Streamlit application that allows users to search for any topic using the Wikipedia API.
The app displays a summary of the requested topic or shows an error message if the topic is not found.""")
task = st.text_input("Enter what you want to find")
if task != '':
    try:  
        res = st.text( wk.summary(task))
    except Exception as e:
        st.error("Nothing was found (try searching more correctly)")    
