import streamlit as st
import json 


us = st.text_input('Enter the username:')


count = st.number_input('Enter the amount: ',min_value = 1,max_value = 10)


formulas = []
for i in range(count):
    forl = st.text_input(f"Enter the formula{i}:",key = f"Formula{i}")
    formulas.append(forl)
with open('dt2.json','r') as file:
    try:   
        data = json.load(file)
    except:
        st.error('Went wrong')
for i in range(len(formulas)):
    try:    
        data[str(f'formula{i}')] = formulas[i]
    except:
        st.error('Something went wrong')
print(data)
with open('dt2.json','r') as file:
    try:  
        json.dump(data,file,indent=4)
    except:
        st.error('Wrong went')    
        
        


    