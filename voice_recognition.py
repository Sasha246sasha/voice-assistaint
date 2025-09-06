import json
import logging
import pyaudio
from vosk import Model, KaldiRecognizer
from commands import command_recognition_arduino, command_recognition, computer
from serial import Serial
from serial.tools.list_ports import comports
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from keyboard import add_hotkey
import gettext


def get_com():
    ports = list(comports())
    return ports[0].device


# logger
logging.basicConfig(level="INFO", format="[%(name)s] %(levelname)s -> %(message)s")
logger = logging.getLogger("voice_recognition")

# locate
t = gettext.translation(domain='messages', localedir='locale', languages=["ru", "en"])
_ = t.gettext

logger.info(_("Starting..."))

# model
model = Model("model_small_USE_THIS")
recognizer = KaldiRecognizer(model, 16000)

# PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# serial

while True:
    q = input("Arduino? да/нет ")
    if q == "да":
        ser = Serial(get_com(), 9600)
        arduino = True
        break
    elif q == "нет":
        arduino = False
        break

# pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# kb
rec = True


def l():
    global rec
    rec = not rec
    logger.info(_("Stopped/started rec"))


add_hotkey("win+z", l)

logger.info(_("Started!"))

try:
    while True:
        if not rec:
            continue
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            res_text = json.loads(result)["text"]
            if res_text:
                logger.info(_(f"Recognized text: {res_text}"))
                if computer(res_text):
                    if arduino:
                        command_recognition_arduino(res_text, ser)
                    command_recognition(res_text, volume)
        else:
            partial_result = recognizer.PartialResult()
except KeyboardInterrupt:
    logger.info(_("Finishing..."))
finally:
    if arduino:
        ser.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    logger.info("Finished!")
