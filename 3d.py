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
    x_min = st.number_input("Минимум", value=-10)
    x_max = st.number_input("Максимум", value=10)
    steps = st.slider("Количество точек", 50, 500)
    grid = st.checkbox("Сетка")
    function = st.text_input("Формула", value='x') + ' '
    fun2 = st.text_input("Формула", value='')   
    file = st.file_uploader("Выбрать формулу из файла")         
    description = st.empty()
    if 'sin' in function:
        description.text("Синус - это тригонометрическая функция, которая описывает колебания.")
    elif 'cos' in function:
        description.text("Косинус - это тригонометрическая функция, которая также описывает колебания, но со сдвигом фазы.")
    elif 'tan' in function:
        description.text("Тангенс - это тригонометрическая функция, которая описывает отношение синуса к косинусу.")
    elif 'exp' in function:
        description.text("Экспонента - это функция, которая описывает экспоненциальный рост или затухание.")
    elif 'log' in function:
        description.text("Логарифм - это функция, обратная экспоненте, которая описывает рост или затухание в логарифмической шкале.")
    elif 'sqrt' in function:
        description.text("Квадратный корень - это функция, которая возвращает квадратный корень из числа.")
    elif 'sin' not in function and 'cos' not in function and 'tan' not in function and 'exp' not in function and 'log' not in function and 'sqrt' not in function:
        description.text("Линейная функция - вида kx + b, некоторые переменные могут отсутствовать.")   
    else:
        description.text("")  
x = linspace(x_min, x_max, steps)        
def d3_grafic():
    x4 = np.linspace(x_min,x_max,steps)
    y4 = safe_evaluate(replace_abs_notation(function), {'x': x})
    x4, y4 = np.meshgrid(x, y4)
    z = np.sin(np.sqrt((x4 ** 2) + (y4 ** 2)))
    fiig = plt.figure()
    ax = fiig.add_subplot(111, projection='3d')
    ax.plot_surface(x4, y4, z, cmap='viridis')
    st.pyplot(fiig)            
d2 = st.button('3d') # Поменял специально метстами немного запутанно (Знаю, так надо)     
d3 = st.button('2d',on_click = d3_grafic()) 

print(replace_abs_notation(function))
print(function)
######Нейросеть######
# Вычисления (с заменой ne.evaluate на safe_evaluate)
try:
    y = safe_evaluate(replace_abs_notation(function), {'x': x})
except Exception as e:
    st.error(f"Ошибка в формуле: {e}")
    y = np.zeros_like(x) 

if fun2 != '':
    fun2 = fun2 + ' '
    try:
        y2 = safe_evaluate(replace_abs_notation(fun2), {'x': x})
    except Exception as e:
        st.error(f"Ошибка в формуле: {e}")
        y2 = np.zeros_like(x)        

# Построение графика (без изменений)
figure = plt.figure()
plt.plot(x, y)
if fun2 != '':
    plt.plot(x, y2)    

y0 = np.asarray([0] * len(x))
plt.plot(x, y0, color='black')
plt.plot(y0, x, color='black')

if grid:
    plt.grid()

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
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            print(text)
            if 'sin' in text:
                print("Sin in text")
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
def test():
    pass
        
st.pyplot(figure)    
