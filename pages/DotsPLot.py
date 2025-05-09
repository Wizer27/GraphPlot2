import streamlit as st
import  matplotlib.pyplot as plt

fig = plt.figure()
#x = [1, 2, 3, 4]
#y = [10, 20, 25, 30]
plt.title("Диаграмма рассеяния")
xs = []
ys = []
with st.sidebar:
    grid = st.checkbox('Grid')
    count = st.number_input('How many dots?',min_value=1,max_value = 50)
    for dot in range(count + 1):
        x = st.text_input(f'Dotx {dot}',key = f"Dotx {dot}")
        y = st.text_input(f'Doty {dot}',key = f"Doty {dot}")
        if x != '':  
            xs.append(int(x))
        if y != '':        
            ys.append(int(y))
print("xs:", xs)
print("ys: ", ys)    
if grid:
    plt.grid()    
if len(ys) == len(xs):    
    plt.scatter(xs, ys)
else:
    st.error("Not enough inputs !")    
st.pyplot(fig)



