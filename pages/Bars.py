import matplotlib.pyplot as plt
import streamlit as st
fig = plt.figure()
plt.bar(['A', 'B', 'C'], [3, 7, 5])
st.pyplot(fig)
