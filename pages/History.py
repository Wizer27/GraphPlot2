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
        - 📈 x: [{item['x_min']} .. {item['x_max']}]  
        """)
         st.markdown("---") 
    else:
        st.info("History is empty")
                