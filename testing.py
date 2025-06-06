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
    try:
        y = safe_evaluate(replace(forl),{'x':x}) 
    except:
        st.error("Something went wrong")    
if forl != "":
    try:
        
        dty = [forl]
        for i in range(1,10):
            dty.append(forl + '-' + str(i))
        for f in dty:
            plt.plot(safe_evaluate(replace(f.lower()),{'x':x}),x)
    except:
        st.error("Something went wrong")    
st.pyplot(fig)    
         