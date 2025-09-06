from time import sleep
import tkinter as tk
from webbrowser import open_new_tab
import logging

logging.basicConfig(level="INFO", format="[%(name)s] %(levelname)s -> %(message)s")
logger = logging.getLogger("commands")


def text_to_number(text):
    numbers = {
        "ноль": 0,
        "один": 1,
        "два": 2,
        "три": 3,
        "четыре": 4,
        "пять": 5,
        "шесть": 6,
        "семь": 7,
        "восемь": 8,
        "девять": 9,
        "десять": 10,
        "одиннадцать": 11,
        "двенадцать": 12,
        "тринадцать": 13,
        "четырнадцать": 14,
        "пятнадцать": 15,
        "шестнадцать": 16,
        "семнадцать": 17,
        "восемнадцать": 18,
        "девятнадцать": 19,
        "двадцать": 20,
        "тридцать": 30,
        "сорок": 40,
        "пятьдесят": 50,
        "шестьдесят": 60,
        "семьдесят": 70,
        "восемьдесят": 80,
        "девяносто": 90,
        "сто": 100
    }

    words = text.lower().split()
    total = 0

    for word in words:
        if word in numbers:
            total += numbers[word]

    return total if total <= 100 else None


def computer(command):
    return "комп" in command or "ноут" in command


def show_volume_change(current, new):
    root = tk.Tk()
    root.title("")
    root.attributes('-topmost', True)
    label = tk.Label(root, text=f"было: {int(current * 100)}, стало: {int(new * 100)}", font=("Arial", 16))
    label.pack(pady=20)
    root.after(3000, root.destroy)
    root.mainloop()


def command_recognition(command: str, volume):
    if "громче" in command:
        current = volume.GetMasterVolumeLevelScalar()
        add = 0.05
        new = min(current + add, 1.0)
        volume.SetMasterVolumeLevelScalar(new, None)
        print(f"было: {current}, стало {new}")
        show_volume_change(current, new)
    elif "тише" in command:
        current = volume.GetMasterVolumeLevelScalar()
        remove = 0.05
        new = max(current - remove, 0.0)
        volume.SetMasterVolumeLevelScalar(new, None)
        print(f"было: {current}, стало {new}")
        show_volume_change(current, new)
    elif "громкость на" in command:
        current = volume.GetMasterVolumeLevelScalar()
        word = command[23:]
        digit = text_to_number(word)
        if digit is not None:
            volume.SetMasterVolumeLevelScalar(digit / 100, None)
            print(f"было: {current}, стало {digit / 100}")
            show_volume_change(current, digit / 100)
        else:
            print("error: not a digit")
    elif "звук на" in command:
        current = volume.GetMasterVolumeLevelScalar()
        word = command[18:]
        digit = text_to_number(word)
        if digit is not None:
            volume.SetMasterVolumeLevelScalar(digit / 100, None)
            print(f"было: {current}, стало {digit / 100}")
            show_volume_change(current, digit / 100)
        else:
            print("error: not a digit")
    elif "найди" in command:
        q = command[16:]
        open_new_tab(f"https://www.google.com/search?q={q}")


def command_recognition_arduino(command, ser):
    if "вкл" in command:
        if "свет" in command:
            print("вкл св")
            ArduinoCommands.on_light(ser)
        elif "звук" in command:
            print("вкл зв")
            ArduinoCommands.on_sound(ser)
    elif "выкл" in command:
        if "свет" in command:
            print("выкл св")
            ArduinoCommands.off_light(ser)
        elif "звук" in command:
            print("выкл зв")
            ArduinoCommands.off_sound(ser)


class ArduinoCommands:
    @staticmethod
    def on_light(ser):
        sleep(3)
        ser.write(b'Hello world')
        ser.write(b'1')

    @staticmethod
    def off_light(ser):
        sleep(3)
        ser.write(b'Hello world')
        ser.write(b'0')

    @staticmethod
    def on_sound(ser):
        sleep(3)
        ser.write(b'Hello world')
        ser.write(b'2')

    @staticmethod
    def off_sound(ser):
        sleep(3)
        ser.write(b'Hello world')
        ser.write(b'3')
