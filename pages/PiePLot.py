import streamlit as st
import  matplotlib.pyplot as plt
import numpy as np

with st.sidebar:
    plt.style.use('_mpl-gallery-nogrid')


    x = []
    count = st.number_input('Enter the amount of peaces:',min_value = 1,max_value = 10)
    for i in range(count):
        c = st.number_input("Enter the value:",min_value = 1,max_value = 10,key = f'value{i}')
        x.append(c)
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

    fig, ax = plt.subplots()
    ax.pie(x, colors=colors, radius=3, center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

st.pyplot(fig)