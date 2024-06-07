# python file


import serial
import serial.tools.list_ports
import time
import psutil
import os


WAIT_CHAR = 0.003  # max second needed to transmit all data

# ----------------------------------------------------------------------------


def get_battery_percentage() -> str:
    battery = psutil.sensors_battery()
    if battery is not None:
        return str(int(battery.percent))
    return "NoBatteryInfo"


def get_battery_charge_state() -> str:
    battery = psutil.sensors_battery()
    if battery.power_plugged:
        return "Charging"
    else:
        return "Discharging"


def test():
    print(get_battery_percentage())
    print(get_battery_charge_state())


def find_port():
    ports = serial.tools.list_ports.comports()
    print(f"Found {len(ports)} ports.")

    if len(ports) > 1:
        # print(f"found ports: {','.join([port.device for port in ports])}.")
        time.sleep(2)

    for port in ports:
        # print(f"Trying port: {port.device}")
        try:
            ser = serial.Serial(port.device)
            time.sleep(6)
            ser.write("HELLO_ARDUINO;".encode())
            while True:
                if ser.in_waiting > 0:
                    time.sleep(WAIT_CHAR)
                    a = ser.read_all().decode()
                    ser.close()  # we don't need port anymore
                    if a == "HELLO_PYTHON;":
                        print(f"Success at {port.device}.")
                        return port.device
                    else:
                        print(f"Got message: {a}")

                        break
                else:
                    time.sleep(0.1)  # simple time for break

        except serial.SerialException:
            # ser.close()
            continue
    print("No ports found")
    return None


if __name__ == "__main__":
    print(find_port())
