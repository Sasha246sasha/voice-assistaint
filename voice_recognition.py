import json
import pyaudio
from vosk import Model, KaldiRecognizer
from commands import command_recognition
from serial import Serial
from serial.tools.list_ports import comports


def get_com():
    ports = list(comports())
    return ports[0].device


# model
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

# PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# serial
ser = Serial(get_com(), 9600)

print("Начинаю распознавание речи...")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            res_text = json.loads(result)["text"]
            command_recognition(res_text, ser)
        else:
            partial_result = recognizer.PartialResult()
            print(json.loads(partial_result)["partial"], end='\r')
except KeyboardInterrupt:
    print("Завершение распознавания речи...")
finally:
    ser.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
