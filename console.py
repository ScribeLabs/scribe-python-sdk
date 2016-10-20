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
                print "#{}: {}".format(devices.index(device), device._peripheral.name())
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
        elif cmd == "load file list":
            files = scribe.load_file_list()
            for f in files:
                print_dict(f)
        elif cmd == "status":
            print_dict(scribe.status())
        elif cmd == "read data":
            print "Type file index : "
            file_idx = int(raw_input())
            print "Type file block data point : "
            data_pt = int(raw_input())
            scribe.read_data(file_idx, data_pt)
        elif cmd == "stop read data":
            print_dict(scribe.stop_read_data())
        elif cmd == "reboot":
            print "Reboot type : 0 - soft, 1 - hard"
            r_type = int(raw_input())
            scribe.reboot(r_type)
        elif cmd == "pooling status":
            print_dict(scribe.pooling_status())
        elif cmd == "file information":
            print "Type file index : "
            file_idx = int(raw_input())
            print_dict(scribe.get_file_info(file_idx))
        elif cmd == "erase data":
            print "erase type (1-partial 0,2-chip, 3-deleted, 4-EEPROM/default ): "
            e_type = int(raw_input())
            print "erase bit mask (1-file): "
            e_bit_mask = int(raw_input())
            print_dict(scribe.erase_data(e_type, e_bit_mask))
        elif cmd == "update crc":
            print "file block size : (16-default)"
            file_block_size = int(raw_input())
            print "file point buffer : (0 - default)"
            file_point_buffer = int(raw_input())
            print_dict(scribe.update_crc_checksum(file_block_size, file_point_buffer))
        elif cmd == "get led color":
            scribe.get_led_color()
        elif cmd == "light":
            scribe.write_packet("L" + chr(13) + "\x01\x00\xff\x00")
    bt.end()

bt = BTLE()
threading.Thread(target=main, args=(bt,)).start()
bt.launch()