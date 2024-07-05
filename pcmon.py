# python file

import serial
import serial.tools.list_ports
import time
import psutil


info_battery_percentage: int
info_battery_charge_state: str
f_battery = 100

ser: serial.Serial

TEXT_TO_SEND = "HELLO_ARDUINO;"
TEXT_TO_GET = "HELLO_PYTHON"
BATT_LOW = 40
BATT_HIGH = 70
WAIT_CHAR = 20
# max milisecond needed to transmit all data

# ----------------------------------------------------------------------------


# get info from pc
def get_battery_percentage() -> int:
    battery = psutil.sensors_battery()
    if battery is not None:
        return int(battery.percent)
    else:
        return 0


def get_battery_charge_state() -> bool:
    battery = psutil.sensors_battery()
    return battery.power_plugged


# send commands & values to arduino
def act_charge_pc(val: int = 1) -> None:
    # plug or unplug pc
    ser.write(f"charge_pc>{str(val)}".encode())


def wait_char():
    time.sleep(WAIT_CHAR/1000)


# port configuration
def is_correct_port(port: str) -> bool:
    ser = serial.Serial(port)
    try:
        communicate(ser)
        return True
    except serial.SerialException:
        return False


def communicate(ser: serial.Serial) -> None:
    time.sleep(6)
    ser.write(TEXT_TO_SEND.encode())
    for _ in range(100):
        # TODO timeout by predefined value
        if ser.in_waiting > 0:
            wait_char()
            a = ser.read_all().decode()
            print(f"got message from arduino: {a}")
            if a == TEXT_TO_GET:
                # time.sleep(1)
                return
            else:
                break
        else:
            time.sleep(0.1)
    raise serial.SerialException()


def find_port():
    ports = serial.tools.list_ports.comports()
    # print(f"Found {len(ports)} ports.")

    arduino_ports = list()
    for port in ports:
        if 'arduino' in port.description.lower() or\
           'serial' in port.description.lower() or \
           'ttyUSB' in port.device or\
           'ttyACM' in port.device:
            arduino_ports.append(port)

    print(f"Found {len(arduino_ports)} potential arduino port(s): "
          f"{','.join([port.device for port in arduino_ports])}.")

    for port in arduino_ports:
        print(f"Trying port: {port.device}.")
        # print(f"Port.description = {port.description}")
        try:
            if is_correct_port(port.device):
                print(f"Success at {port.device}.")
                return port.device
            else:
                print(f"Fail at: {port.device}.")
                break
        except serial.SerialException:
            continue
    print("No correct port found!")
    raise serial.SerialException()


# main function. (entry)
def main():
    global ser
    ser = serial.Serial(find_port())
    communicate(ser)

    while True:
        for i in range(10000):
            if True:
                if ser.in_waiting != 0:
                    print("==something appeared!==")
                    wait_char()
                    command, arguments = ser.read_until(b';').decode().split('>')
                    print(f"command={command}\nargs={arguments}")
                    if command == "hello" and arguments == "python":
                        ser.write(b"hello arduino")


            # BATTERY
            if not i % f_battery:  # if i%f_battery == 0:
                info_battery_percentage = get_battery_percentage()
                info_battery_charge_state = get_battery_charge_state()
                if info_battery_percentage < BATT_LOW and\
                   not info_battery_charge_state:
                    print("charge pc sent")
                    act_charge_pc(1)
                elif info_battery_percentage > BATT_HIGH and\
                     info_battery_charge_state:
                    print("unpluging battery")
                    act_charge_pc(0)
                else:
                    print("doing nothing with battery!")

            # WAIT
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


# use test() for debug only
def test():
    try:
        find_port()
        exit(0)
    except Exception:
        print("EXCEPTION !!!")
    exit(1)


# test()

if __name__ == "__main__":
    while True:
        # main()
        # exit()
        try:
            main()
        except serial.SerialException:
            time.sleep(5)
            continue
        except KeyboardInterrupt:
            break
