import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
data = np.random.rand(1000)
fig = plt.figure()
plt.hist(data,bins = 30)
plt.title("Histogramm")
st.pyplot(fig)