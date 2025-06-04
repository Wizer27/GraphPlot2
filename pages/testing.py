import streamlit as st
import matplotlib.pyplot as plt
import re
import numpy as np
import numexpr  as ne









def safe_evaluate(expr, variables=None):
    """Безопасная замена ne.evaluate() с ограниченным набором функций"""
    allowed_functions = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': abs

    }
    local_dict = {**(variables or {}), **allowed_functions}
    return ne.evaluate(expr, local_dict=local_dict, global_dict={})
def replace(expression):
    expression = re.sub(r'\|(.+?)\|', r'abs(\1)', expression)
    # Добавление * между числом и x (например, 2x → 2*x)
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)
    # Замена ^ на **
    expression = expression.replace('^', '**')
    return expression



with st.sidebar:
    forl = st.text_input("Enter the formula")
fig = plt.figure()
plt.axhline(0, color='black', linewidth=1)  # Ось X (y = 0)
plt.axvline(0, color='black', linewidth=1)   
x = np.linspace(-20,20,450)
if forl != "":
    y = safe_evaluate(replace(forl),{'x':x}) 
def ploting_with_dots(x,y):  
    plt.plot(x,y)  
    mxy = max(y)
    mny = min(y)
    print(f"Minimum of y is {mny}")
    print(f"Maximum if y is {mxy}")
    for i in range(len(x)):
        x[i] = int(x[i])
    x = set(x)
    y2 = []
    for i in range(len(y)):
        y2.append(int(y[i]))
    y2 = set(y2)
    for i in y2:
        for j in x:
            if (i % 2 == 0 and j % 2 == 0):   
                plt.scatter(i,j)     
       
      
    st.pyplot(fig)  
    
if forl != "":    
    try:
            
        ploting_with_dots(x,y)        
    except Exception as e:
        print(f"Error {e}")          