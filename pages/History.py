import os
import json
import streamlit as st
st.title("History of plots")
if os.path.exists('/Users/ivanvinogradov/GraphPlot2/pages/data.json'):
    with open('/Users/ivanvinogradov/GraphPlot2/pages/data.json') as file:
        history = json.load(file)
    for item in reversed(history):
         st.markdown(f"""
        - 🧮 **Formula:** `{item['formula']}`  
        """)
         st.markdown("---") 
    else:
        st.info("History is empty")
                