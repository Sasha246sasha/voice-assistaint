import json
import pyaudio
from vosk import Model, KaldiRecognizer
from commands import command_recognition

# Инициализация модели
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

# Инициализация PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Начинаю распознавание речи...")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            res_text = json.loads(result)["text"]
            command_recognition(res_text)
        else:
            partial_result = recognizer.PartialResult()
            print(json.loads(partial_result)["partial"], end='\r')
except KeyboardInterrupt:
    print("Завершение распознавания речи...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
