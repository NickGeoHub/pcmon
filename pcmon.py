# python file



import serial
import serial.tools.list_ports
import time
import psutil
import os


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
        print(f"found ports: {','.join([port.device for port in ports])}.")
        time.sleep(2)

    for port in ports:
        print(f"Trying port: {port.device}")
        try:
            ser = serial.Serial(port.device)
            time.sleep(6)
            ser.write("HELLO_,".encode())
            while True:
                print(f"loop")
                if ser.in_waiting > 0:
                    time.sleep(1)
                    a = ser.read_all().decode()
                    print(a)
                    if a == "HELLO_PYTHON,":
                        # an erti an me2 ikos
                        print(f"Success at {port.device}.")
                        serial_port = port.device
                        return port.device
                    else:
                        print("got another message!")
                else:
                    time.sleep(1)

        except serial.SerialException:
            print(f"Port {port.device} error.")
            continue
    return None

if __name__ == "__main__":
    print(find_port())


