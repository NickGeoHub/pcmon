# python file


import serial
import serial.tools.list_ports
import time
import psutil
import os

info_battery_percentage: int
info_battery_charge_state: str

ser: serial.Serial

TEXT_TO_SEND = "HELLO_ARDUINO;"
TEXT_TO_GET = "HELLO_PYTHON;"
BATT_LOW = 20
BATT_HIGH = 80
WAIT_CHAR = 0.003  # max second needed to transmit all data

# ----------------------------------------------------------------------------

"""
class myArduino():
    def __init__(self,
                 port: str,
                 baudrate: int = 9600):
        self.ser = serial.Serial(port, baudrate)
        communicate(self.ser)
"""

def get_battery_percentage() -> int:
    battery = psutil.sensors_battery()
    if battery is not None:
        return int(battery.percent)
    return "NoBatteryInfo"


def get_battery_charge_state() -> str:
    battery = psutil.sensors_battery()
    return battery.power_plugged
    """
    if battery.power_plugged:
        return "Charging"
    else:
        return "Discharging"
    """


def act_charge_pc() -> None:
    time.sleep(5)
    ser.write(b"charge_pc;")


def test():
    print(get_battery_percentage())
    print(get_battery_charge_state())


def is_correct_port(port: str):
    ser = serial.Serial(port)
    try:
        communicate(ser)
        return True
    except serial.SerialException:
        return False


def communicate(ser: serial.Serial):
    time.sleep(4)
    ser.write(TEXT_TO_SEND.encode())
    while True:
        if ser.in_waiting > 0:
            time.sleep(WAIT_CHAR)
            a = ser.read_all().decode()
            if a == TEXT_TO_GET:
                return
        else:
            time.sleep(0.1)
    raise serial.SerialException()


def find_port():
    ports = serial.tools.list_ports.comports()
    print(f"Found {len(ports)} ports.")

    if len(ports) > 1:
        # print(f"found ports: {','.join([port.device for port in ports])}.")
        time.sleep(2)

    for port in ports:
        # print(f"Trying port: {port.device}")
        try:
            if is_correct_port(port.device):
                print(f"Success at {port.device}.")
                return port.device
            else:
                print(f"Got message: {a}")
                break
        except serial.SerialException:
            continue
    print("No correct port found")
    return None


def main():
    # my_arduino = myArduino(port=find_port())
    global ser
    ser = serial.Serial(find_port())
    communicate(ser)
    while True:
        info_battery_percentage = get_battery_percentage()
        info_battery_charge_state = get_battery_charge_state()
        if info_battery_percentage < BATT_LOW and not info_battery_charge_state or True:
            print("charge pc sent")
            act_charge_pc()


if __name__ == "__main__":
    main()
