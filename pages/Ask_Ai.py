from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Загрузка русскоязычной модели
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Создание пайплайна
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Пример запроса
user_input = "Привет! Как дела?"
response = chatbot(user_input, max_length=50)[0]['generated_text']
print(response)