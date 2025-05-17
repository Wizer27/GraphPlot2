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
#for i in range(len(formulas)):
    #try:    
        #data[str(f'formula{i}')] = formulas[i]
   # except:
        #st.error('Something went wrong')
print(data)

user_ex = False

for user in data:
    if user['username'] == us:
        user['formulas'] += formulas
        user_ex = True
    break


if not user_ex:
    data.append({
        "username":us,
        "formulas":formulas
    })    



with open('dt2.json','w') as file:
    try:  
        json.dump(data,file,indent=4,ensure_ascii=False)
    except:
        st.error('Wrong went')    
        
print(data)

print(formulas)        


    