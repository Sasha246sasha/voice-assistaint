import time


def command_recognition(command, ser):
    if "вкл" in command:
        print("вкл")
        Commands.on(ser)
    elif "выкл" in command:
        print("выкл")
        Commands.off(ser)


class Commands:
    @staticmethod
    def on(ser):
        time.sleep(3)
        ser.write(b'Hello world')
        ser.write(b'1')

    @staticmethod
    def off(ser):
        time.sleep(3)
        ser.write(b'Hello world')
        ser.write(b'0')
