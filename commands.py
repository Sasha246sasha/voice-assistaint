from serial import Serial
from serial.tools.list_ports import comports


def get_com():
    ports = list(comports())
    return ports[0].device


def command_recognition(command):
    if "вкл" in command:
        print("вкл")
        Commands.on()
    elif "выкл" in command:
        print("выкл")
        Commands.off()


class Commands:
    @staticmethod
    def on():
        ser = Serial(get_com(), 9600)
        ser.write(b'1')
        ser.close()

    @staticmethod
    def off():
        ser = Serial(get_com(), 9600)
        ser.write(b'0')
        ser.close()
