import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# GPT-2 для генерации текста
chatbot = pipeline("text-generation", model="gpt2")

user_input = "What is AI?"
response = chatbot(user_input, max_length=50)[0]['generated_text']
print(response)

# Или DialoGPT (специально для диалогов)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

inputs = tokenizer(user_input, return_tensors="pt")
outputs = model.generate(**inputs, max_length=1000)
print(tokenizer.decode(outputs[0]))
def main(expr):
    main_ask = st.text_input('Enter he massage for ai')
    resp = 'this is a test'
    return resp