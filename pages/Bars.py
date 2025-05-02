import matplotlib.pyplot as plt
import streamlit as st
fig = plt.figure()
with st.sidebar:
    val1 = st.text_input("Value1: ",placeholder = 'Enter the value1',value = 20)
    val2 = st.text_input("Value2:  ",placeholder = 'Enter the value2',value = 10)
    val3 = st.text_input("Value3: ",placeholder = 'Enter thr value3',value =5)
    n1 =st.text_input("Name1:",placeholder = 'Enter the name1')
    n2 = st.text_input("Name2: ",placeholder = 'Enter the name2')
    n3 = st.text_input("Name3: ",placeholder = 'Enter the name3')
plt.bar([n1,n2,n3], [float(val1), float(val2), float(val3)])
st.pyplot(fig)
