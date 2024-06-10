# python file


import serial
import serial.tools.list_ports
import time
import psutil
import os

info_battery_percentage: int
info_battery_charge_state: str
f_battery = 100

ser: serial.Serial

TEXT_TO_SEND = "HELLO_ARDUINO;"
TEXT_TO_GET = "HELLO_PYTHON;"
BATT_LOW = 20
BATT_HIGH = 80
WAIT_CHAR = 0.003  # max second needed to transmit all data

# ----------------------------------------------------------------------------


class PortNotFoundError(Exception):
    pass


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

    if len(ports) > 0:
        print(f"found ports: {','.join([port.device for port in ports])}.")

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
    raise PortNotFoundError()

def main():
    # my_arduino = myArduino(port=find_port())
    global ser
    ser = serial.Serial(find_port())
    communicate(ser)
    while True:
        for i in range(10000):
            # BATTERY
            if not i % f_battery:  # if i%f_battery == 0:
                info_battery_percentage = get_battery_percentage()
                info_battery_charge_state = get_battery_charge_state()
                if info_battery_percentage < BATT_LOW and\
                not info_battery_charge_state:
                    print("charge pc sent")
                    act_charge_pc()
            
            time.sleep(0.1)
            # TODO axla aq gvinda sixshireebi
            # tu sixshire aris 10 mashin kvela me-10 loop-ze daUpdatdes
            # tu sixshire aris 1 mashin kvela loopze update
            # i%{sixshire}
            # kvela sidides ro tavisi sixshire qondes xom ar shevqmna klasi?
            # class batteryPercentage():
            #     self.sicshire
            #     self.value
            #     def update(self):
            #         update()


if __name__ == "__main__":
    while True:
        try:
            main()
        except PortNotFoundError:
            time.sleep(5)
            continue
        except KeyboardInterrupt:
            break
