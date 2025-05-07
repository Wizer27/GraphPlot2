import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
data = np.random.rand(1000)
fig = plt.figure()
plt.hist(data,bins = 30)
with st.sidebar:
    title = st.text_input("Enter the title")
plt.title(title)
st.pyplot(fig)
### New page