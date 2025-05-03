import matplotlib.pyplot as plt
import streamlit as st
with st.sidebar:
    count  = st.number_input("How many bars?",min_value = 1,max_value = 20,step = 1)
    lab = []
    nums = []
    for i in range(count):
        label = st.text_input(f"Name {i+1}", key=f"Label {i}")
        value = st.number_input(f"Value {i+1}", key= f"Value {i}")
        lab.append(label)
        nums.append(value)

#Made an update
fig, ax = plt.subplots()
ax.bar(lab, nums)
st.pyplot(fig)