import streamlit as st
import numpy as np
import plotly.figure_factory as ff

# Add histogram data
with st.sidebar:
    x12 = st.text_input("Enter the value1: ",value = 20)
    x22 = st.text_input("Enter the value2: ",value = 20)
    x32 = st.text_input("Enter the value3: ",value = 20)
    x1 =  np.random.randn(int(x12)) - 2
    x2 = np.random.randn(int(x22))
    x3 = np.random.randn(int(x32)) + 2
# Group data together
    hist_data = [x1, x2, x3]

    group_labels = [st.text_input("Name the value1: "), st.text_input("Name the value2:"), st.text_input("Name the value3:")]

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!

st.plotly_chart(fig)