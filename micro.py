import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os

# Проверяем доступные устройства
print("Доступные устройства:")
print(sd.query_devices())

# Настройки записи
duration = 60  # Длительность записи в секундах
fs = 44100  # Частота дискретизации
channels = 1  # Количество каналов (1 для моно)

try:
    # Запись звука
    print(f"Записываем {duration} секунд аудио...")
    recording = sd.rec(int(duration * fs), 
                      samplerate=fs, 
                      channels=channels,
                      device='MacBook Air Microphone')  # Явно указываем устройство
    
    sd.wait()  # Ждем окончания записи
    
    # Сохраняем в WAV файл
    output_path = os.path.expanduser("~/Desktop/mic_recording.wav")
    write(output_path, fs, recording)
    print(f"Запись сохранена: {output_path}")

except Exception as e:
    print(f"Ошибка: {e}")