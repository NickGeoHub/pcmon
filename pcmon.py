# python file

import serial
import serial.tools.list_ports
import time
import psutil


info_battery_percentage: int
info_battery_is_charging: bool
f_battery = 200

END = ';'
SEP = '>'
TEXT_TO_SEND = "HELLO_"+SEP+"ARDUINO"+END
TEXT_TO_GET = "HELLO_"+SEP+"PYTHON"+END

BATT_LOW = 50
BATT_HIGH = 70

# ----------------------------------------------------------------------------


# get info from pc
def get_batt_percentage() -> int:
    battery = psutil.sensors_battery()
    if battery is not None:
        return int(battery.percent)
    else:
        return 0


def get_batt_is_charging() -> bool:
    battery = psutil.sensors_battery()
    return bool(battery.power_plugged)


def send_log(message):
    print(f"PC: log: {message}")


# send commands & values to arduino
def act_charge_pc(val: int = 1) -> None:
    # plug or unplug pc
    ser.write(f"charge_pc{SEP}{str(val)}{END}".encode())


# port configuration
def is_correct_port(port: str) -> bool:
    ser = serial.Serial(port)
    try:
        communicate(ser)
        return True
    except serial.SerialException:
        return False


def communicate(ser: serial.Serial) -> None:
    time.sleep(5)
    ser.write(TEXT_TO_SEND.encode())
    for _ in range(100):
        # TODO timeout by predefined value
        if ser.in_waiting > 0:
            a = ser.read_until(END.encode()).decode()
            # print(f"got message from arduino: {a}")
            if a == TEXT_TO_GET:
                # time.sleep(1)
                return
            else:
                break
        else:
            time.sleep(0.1)
    raise serial.SerialException()


def command_send(cmd: str, arg: str, ser: serial.Serial):
    ser.write(f"{cmd}{SEP}{arg}{END}".encode())


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
                print(f"Success in {port.device}.")
                return port.device
            else:
                print(f"Fail in: {port.device}.")
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
            # get data from arduino
            if not i % 3:
                if ser.in_waiting != 0:
                    a = ser.read_until(END.encode()).decode()
                    # print(f"here==={a}")
                    command, arguments = a.strip(END).split(SEP)
                    # print("message from arduino".center(50, "="))
                    # print(f"command={command}\nargs={arguments}")  # #
                    if command == "log":
                        print(f"Arduino: log: {arguments}")

                    elif command + SEP + arguments + END == TEXT_TO_GET:  # +END ratoa arvici
                        ser.write(TEXT_TO_SEND.encode())
                    elif command == "get":
                        if arguments == "all":
                            # print("get all detected!!!!")
                            command_send("batt_p", str(get_batt_percentage()))
                            command_send("batt_c", str(get_batt_is_charging()))

                        # TODO for now commenteds
                        # elif arguments == "batt_p":
                        #     command_send("batt_p", str(get_batt_percentage()))

                        # elif arguments == "batt_c":
                        #     command_send("batt_c", str(get_batt_is_charging()))

                    else:
                        send_log(f"Unknown command,argument: {command},{arguments}.")

            # give data to arduino if it is time!
            # BATTERY
            if not i % f_battery:  # if i%f_battery == 0:
                info_battery_percentage = get_batt_percentage()
                info_battery_is_charging = get_batt_is_charging()
                if info_battery_percentage < BATT_LOW and\
                   not info_battery_is_charging:
                    send_log("plug pc sent")
                    act_charge_pc(1)
                elif info_battery_percentage > BATT_HIGH and\
                     info_battery_is_charging:
                    send_log("unplug pc sent")
                    act_charge_pc(0)
                else:
                    # print("doing nothing with battery!")
                    pass

            # WAIT
            time.sleep(0.1)


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
            print("E: Arduino disconnected!")
            continue
        # except Exception as e:  # jobia
        #     print(f"E: {e}; skipped")
        #     time.sleep(5)
        #     continue
        except KeyboardInterrupt:
            print("W: Process is stopped (User request).")
            break
