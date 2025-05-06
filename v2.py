import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import numexpr as ne
#from easyocr import Reader
from pypdf import PdfReader
import re
from mpl_toolkits.mplot3d import Axes3D

def safe_evaluate(expr, variables=None):
    """Безопасная замена ne.evaluate() с ограниченным набором функций"""
    allowed_functions = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': abs

    }
    local_dict = {**(variables or {}), **allowed_functions}
    return ne.evaluate(expr, local_dict=local_dict, global_dict={})

def replace_abs_notation(expression):
    """Заменяет |x| на abs(x) в выражении (оригинальная функция без изменений)"""
    stack = []
    result = []
    i = 0
    n = len(expression)

    while i < n:
        if expression[i] == '|':
            if stack:
                stack.pop()
                result.append(')')
            else:
                stack.append('|')
                result.append('abs(')
            i += 1
        else:
            result.append(expression[i])
            i += 1
    result = ''.join(result).replace('^', '**')
    for i in range(len(result)):
        if result[i] == 'x' and (result[i - 1].isdigit() or result[i-1] == ')'):
            result = result[:i] + '*' + result[i:]
            result = ''.join(result)
        if result[i] == 'x' and (result[i + 1] == '(' or result[i + 1].isdigit()):
            print('2')
            result = result[:i+1] + '*' + result[i:]
            result = ''.join(result)
    return result

def replace(expression):
    expression = re.sub(r'\|(.+?)\|', r'abs(\1)', expression)
    # Добавление * между числом и x (например, 2x → 2*x)
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)
    # Замена ^ на **
    expression = expression.replace('^', '**')
    return expression
# Streamlit интерфейс (без изменений)   

with st.sidebar:
    x_min = st.number_input("Минимум", value=-20)
    x_max = st.number_input("Максимум", value=20)
    steps = st.slider("Количество точек", 50, 500)
    d_gr = st.text_input("Enter the fucntion for 3d plot:",value = 'x')
    grid = st.checkbox("Сетка")
    x = linspace(x_min, x_max, steps) 
    ys = [] #список всех формул
    count = st.number_input("How many Formulas: ",min_value = 1,max_value = 20)
    for i in range(count):
        forl = st.text_input(f"Formula {i + 1}",key = f"Formula {i}")
        if forl != '':  
            try:
                ys.append(safe_evaluate(replace(forl),{'x':x}))
            except Exception as e:
                st.error(f"No function for {e}")
                       
    file = st.file_uploader("Выбрать формулу из файла")         
    #Описание графиков 1 для обычного 2d графика
    description = st.empty()   
    if  ys and 'sin' in ys[0]:
        description.text("Синус - это тригонометрическая функция, которая описывает колебания.")
    elif ys and 'cos' in ys[0]:
        description.text("Косинус - это тригонометрическая функция, которая также описывает колебания, но со сдвигом фазы.")
    elif ys and 'tan' in ys[0]:
        description.text("Тангенс - это тригонометрическая функция, которая описывает отношение синуса к косинусу.")
    elif ys and 'exp' in ys[0]:
        description.text("Экспонента - это функция, которая описывает экспоненциальный рост или затухание.")
    elif ys and'log' in ys[0]:
        description.text("Логарифм - это функция, обратная экспоненте, которая описывает рост или затухание в логарифмической шкале.")
    elif ys and 'sqrt' in ys[0]:
        description.text("Квадратный корень - это функция, которая возвращает квадратный корень из числа.")
    elif ys and ('sin' not in ys[0] and 'cos' not in ys[0] and 'tan' not in ys[0] and 'exp' not in ys[0] and 'log' not in ys[0] and 'sqrt' not in ys[0]):
        description.text("Линейная функция - вида kx + b, некоторые переменные могут отсутствовать.")   
    else:
        description.text("")   
      
# ======== 3D ГРАФИК ========
x4 = np.linspace(x_min,x_max,steps)
try:
    y4 = safe_evaluate(replace(d_gr.lower()), {'x': x})
except Exception as e:
    st.error(f"No function for {e}")
    y4 = np.zeros_like(x)     
x4, y4 = np.meshgrid(x, y4)
z = np.sin(np.sqrt(x4**2 + y4 **2))
fiig = plt.figure()
ax = fiig.add_subplot(111, projection='3d')
ax.plot_surface(x4, y4, z, cmap='viridis')
st.pyplot(fiig)             





######Нейросеть######
# Вычисления (с заменой ne.evaluate на safe_evaluate)
#try:
 #   y = safe_evaluate(replace_abs_notation(function.lower()), {'x': x})
#except Exception as e:
  #  st.error(f"Ошибка в формуле: {e}")
   # y = np.zeros_like(x) 

#if fun2 != '':
    #fun2 = fun2 + ' '
    #try:
     #   y2 = safe_evaluate(replace_abs_notation(fun2.lower()), {'x': x})
    #except Exception as e:
     #   st.error(f"Ошибка в формуле: {e}")
      #  y2 = np.zeros_like(x)        

# Построение графика (без изменений)
 


#========= ПОСТРОЕНИЕ ГРАФИКА ИЗ ФАЙЛА ========= 
if grid:
    plt.grid()
# ===== Фигура(канвас) для  2d графика ===== 
figure = plt.figure()
if file != None:
        print(file)
        name = file.name.split('.')
        #print(name)
        #if 'jpg' in name:
            #reader = Reader(["en"])
            #im = file
            #t = reader.readtext(im,detail = 0)
           # for row in t:
               # print('-'+row)
                #if 'sin' in row:
                    #x2 = linspace(x_min,x_max,steps)
                    #try:
                        #y3 = safe_evaluate(replace(row),{'x': x})
                    #except Exception as e:
                        #st.error(f"Ошибка в формуле {e}")
                        #y3 = np.zeros_like(x)
                    #fig2 = plt.figure()
                   # plt.plot(x,y3)
        if 'pdf' in name:
            print('PDF')
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            print("PLotig from file.......")
            #x2 = linspace(x_min,x_max,steps)
            try:
                print('Working')
                y3 = safe_evaluate(replace(text),{'x':x})
            except Exception as e:
                st.error(f"Ошибка в формуле {e}")
                y3 = np.zeros_like(x)
            #fig2 = plt.figure()
            plt.plot(x,y3)    
            #st.pyplot(figure)
        if 'txt' in name:
            with open(file.name,'r') as file:
                c = file.read()
            print(c)    
            #if 'sin' in c:
            try:
                print('txt is here')
                y3 = safe_evaluate(replace(c),{'x':x})
            except Exception as e:
                st.error(f"Ошибка в формуле {e}")
                y3 = np.zeros_like(x)
            plt.plot(x,y3)  
        if 'txt' not in  name and 'pdf' not in name:
            st.error("This file type is not supported yet")           
                        
def test():
    pass

# ======== 2D ГРАФИК ========
plt.axhline(0, color='black', linewidth=1)  # Ось X (y = 0)
plt.axvline(0, color='black', linewidth=1)
for i in ys:
    plt.plot(x,i)
        
st.pyplot(figure)    
 