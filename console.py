# Console UI to communicate with runscribe device over bluetooth
# This is less of a mess but still pretty bare

from btle import BTLE
import threading

def print_dict(dict):
    for key in dict:
        print "{}: {}".format(key, dict[key])

def main(bt):
    devices = []

    def update_list(current_devices):
        for device in current_devices:
            if not device in devices:
                devices.append(device)
                print "#{}: {}".format(devices.index(device), device.name)
    print "Type number of device + enter to connect"
    bt.scan(update_list)

    name = int(raw_input())
    device = devices[name]
    scribe = bt.connect_to(device)
    print ("Connected")

    while True:
        cmd = raw_input("> ")
        if cmd == "q":
            break
        elif cmd == "read time":
            print_dict(scribe.read_time())
        elif cmd == "get led color":
            print scribe.get_led_color()
        elif cmd == "load file list":
            scribe.load_file_list()
        elif cmd == "status":
            print_dict(scribe.status())
        elif cmd == "read":
            scribe.read_data(0, 0)
        elif cmd == "reboot":
            scribe.soft_reboot()
        elif cmd == "light":
            scribe.write_packet("L" + chr(13) + "\x01\x00\xff\x00")
    bt.end()

bt = BTLE()
threading.Thread(target=main, args=(bt,)).start()
bt.launch()