import streamlit as st
import pandas as pd
import numpy as np
data = pd.DataFrame(np.random.randn(20,3),columns =["Russia","Germany","USA"])
st.area_chart(data)