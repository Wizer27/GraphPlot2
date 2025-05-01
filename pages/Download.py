import streamlit as st
import numpy
text_contents = '''
Foo, Bar
123, 456
789, 000
'''
a = st.download_button('Download CSV', text_contents, 'text/csv')