# Console UI to communicate with runscribe device over bluetooth
# This is less of a mess but still pretty bare

from btle import BTLE
import threading
from Adafruit_BluefruitLE.services import DeviceInformation
import struct

def print_dict(dict):
    for key in dict:
        print "{}: {}".format(key, dict[key])

def main(bt):
    devices = []

    def update_list(current_devices):
        for device in current_devices:
            if not device in devices:
                devices.append(device)
                print "#{}: {} {} {} {}".format(devices.index(device), device.name, device.id, device.is_connected, device.advertised)
    print "Type number of device + enter to connect"
    bt.scan(update_list)

    name = int(raw_input())
    device = devices[name]
    scribe = bt.connect_to(device)
    print ("Connected")
    print "#{}: {} {} {} {}".format(devices.index(device), device.name, device.id, device.is_connected, device.advertised)

    while True:
        cmd = raw_input("> ")
        if cmd == "q":
            break
        elif cmd == "reboot":
            print "Reboot type : 0 - soft, 1 - hard"
            r_type = int(raw_input())
            scribe.reboot(r_type)
        #elif cmd == "annotate file":
        #    print_dict(scribe.annotate_file(0, 1))
        elif cmd == "update crc":
            print "file block size : (16-default)"
            file_block_size = int(raw_input())
            print "file point buffer : (0 - default)"
            file_point_buffer = int(raw_input())
            print_dict(scribe.update_crc_checksum(file_block_size, file_point_buffer))
        elif cmd == "load file list":
            files = scribe.load_file_list()
            for f in files:
                print_dict(f)
        elif cmd == "erase data":
            print "erase type (1-partial 0,2-chip, 3-deleted, 4-EEPROM/default ): "
            e_type = int(raw_input())
            print "erase bit mask (1-file): "
            e_bit_mask = int(raw_input())
            print_dict(scribe.erase_data(e_type, e_bit_mask))
        elif cmd == "DFU mode":
            scribe.DFU_mode()
            print "Scribe in DFU mode"
        #elif cmd == "real time polling":
        #    print "Enter mode (0 => Accel, 1 => Gyro, 2 => Compass):"
        #    mode = int(raw_input())
        #    print_dict(scribe.real_time_polling(mode))
        #elif cmd == "manufacturing mode": # deep motion sleep
        #    print "state : (0 - off, 1 - on)"
        #    state = int(raw_input())
        #    print_dict(scribe.manufacturing_mode(state))
        elif cmd == "file information":
            print "Type file index : "
            file_idx = int(raw_input())
            print_dict(scribe.get_file_info(file_idx))
        #elif cmd == "set led color":
        #    r, g, b = scribe.set_led_color()
        #    string = 'Red : ' + str(r) + ', Green: ' + str(g) + ', Blue: ' + str(b)
        #    print string
        #elif cmd == "get led color":
        #    r, g, b = scribe.get_led_color()
        #    string = 'Red : ' + str(r) + 'Green: ' + str(g) + 'Blue: ' + str(b)
        #    print string
        elif cmd == "light":
            print_dict(scribe.light_led())
        elif cmd == "set mode":
            print "Command (0 - N/A, 1 - record, 2 - pause, 3 - sync) : "
            command = int(raw_input())
            print "state : (0 - off, 1 - on)"
            state = int(raw_input())
            print_dict(scribe.set_mode(command, state))
        elif cmd == "pooling status":
            print_dict(scribe.pooling_status())
        elif cmd == "stop read data":
            print_dict(scribe.stop_read_data())
        elif cmd == "read data":
            print "Type file index : "
            file_idx = int(raw_input())
            print "Type file block data point : "
            data_pt = int(raw_input())
            scribe.read_data(file_idx, data_pt)
        elif cmd == "status":
            print_dict(scribe.status())
        elif cmd == "set time":
            print_dict(scribe.set_time(805306370, 1, 1, 2))
        elif cmd == "read time":
            print_dict(scribe.read_time())
        elif cmd == "read configuration data":
            print "Enter config point (0xAA01..7): "
            configpoint = int(raw_input(),16)
            print_dict(scribe.read_config_data(configblocksize = 16, configpoint = configpoint))
        elif cmd == "write configuration data":
            print "Enter config point (0xAA01..7))"
            configpoint = int(raw_input(),16)
            if configpoint == 0xAA01 or configpoint == 0xAA03:
                print "config block size : "
                configblocksize = int(raw_input())
                for i in range(0,17) :
                    print "ble device " + str(i) + " : "
                    bledevice[i] = int(raw_input())
                packet = struct.pack(">HBBBBBBBBBBBBBBBBB", configblocksize, 1, bledevice[0], bledevice[1], bledevice[2],
                        bledevice[3], bledevice[4], bledevice[5], bledevice[6], bledevice[7], bledevice[8], bledevice[9], bledevice[10],
                        bledevice[11], bledevice[12], bledevice[13], bledevice[14], bledevice[15], bledevice[16])
            elif configpoint == 0xAA02:
                print "config block size : "
                configblocksize = int(raw_input())
                print "led color : "
                bledevice_ledcolor = int(raw_input())
                print "heel/lace : "
                heel_lace = int(raw_input())
                print "right/left : "
                right_left = int(raw_input())
                for i in range(0,4):
                    print "device time " + str(i) + " : "
                    device_time[i] = int(raw_input())
                print "device sample rate : "
                device_sample_rate = int(raw_input())
                print "sensitivity : "
                sensitivity = int(raw_input())
                print "Timeout : "
                timeout = int(raw_input())
                print "stride rate : "
                stride_rate = int(raw_input())
                print "min conn interval : "
                min_conn_interval = int(raw_input())
                print "max conn interval : "
                max_conn_interval = int(raw_input())
                print "ble slave latency : "
                ble_slave_latency = int(raw_input())
                packet = struct.pack(">HBBBBBBBBBBBBBBB", configblocksize, 2, bledevice_ledcolor, heel_lace,
                               right_left, device_time[0], device_time[1], device_time[2], device_time[3], device_sample_rate, 
                               sensitivity, timeout, stride_rate, min_conn_interval, max_conn_interval, ble_slave_latency)
            elif configpoint == 0xAA04:
                print "config block size : "
                configblocksize = int(raw_input())
                print "heel/lace : "
                heel_lace = int(raw_input())
                print "right/left : "
                right_left = int(raw_input())
                print "Timeout : "
                timeout = int(raw_input())
                print "stride rate : "
                stride_rate = int(raw_input())
                print "scale factor A : "
                scale_factor_A = int(raw_input())
                print "scale factor B : "
                stride_rate = int(raw_input())
                print "min recording voltage MSB : "
                min_recording_voltage_MSB = int(raw_input())
                print "min recording voltage LSB : "
                min_recording_voltage_LSB = int(raw_input())
                print "deep sleep voltage MSB : "
                deep_sleep_voltage_MSB = int(raw_input())
                print "deep sleep voltage LSB : "
                deep_sleep_voltage_LSB = int(raw_input())
                print "R : "
                R = int(raw_input())
                print "G : "
                G = int(raw_input())
                print "B : "
                B = int(raw_input())
                packet = struct.pack(">HBBBBBBBBBBBBBB", configblocksize, 4, heel_lace, right_left, timeout,
                    stride_rate, scale_factor_A, scale_factor_B, min_recording_voltage_MSB, min_recording_voltage_LSB,
                    deep_sleep_voltage_MSB, deep_sleep_voltage_LSB, R, G, B )
            elif configpoint == 0xAA05:
                print "config block size : "
                configblocksize = int(raw_input())
                print "min conn interval : "
                min_conn_interval = int(raw_input())
                print "max conn interval : "
                max_conn_interval = int(raw_input())
                print "ble slave latency : "
                ble_slave_latency = int(raw_input())
                packet = struct.pack(">HBBBB", configblocksize, 5, min_conn_interval, max_conn_interval, ble_slave_latency)
            elif configpoint == 0xAA06:
                print "config block size : "
                configblocksize = int(raw_input())
                print "raw data : "
                raw_data = int(raw_input())
                packet = struct.pack(">HBB", configblocksize, 6, raw_data)
            elif configpoint == 0xAA07:
                print "config block size : "
                configblocksize = int(raw_input())
                print "bettery capacity : "
                bettery_capacity = int(raw_input())
                packet = struct.pack(">BHB", configblocksize, 7, bettery_capacity)
            print_dict(scribe.write_config_data(packet))
        elif cmd == "perform diagnostics":
            print_dict(scribe.perform_diagnostics())
        elif cmd == "get diagnostics results":
            print_dict(scribe.get_diagnostics_results())
        elif cmd == "device information service":
            dis = DeviceInformation(device)
            # Print out the DIS characteristics.
            print('Manufacturer: {0}'.format(dis.manufacturer))
            print('Model: {0}'.format(dis.model))
            print('Serial: {0}'.format(dis.serial))
            print('Hardware Revision: {0}'.format(dis.hw_revision))
            print('Software Revision: {0}'.format(dis.sw_revision))
            print('Firmware Revision: {0}'.format(dis.fw_revision))
            print('System ID: {0}'.format(dis.system_id))
            print('Regulatory Cert: {0}'.format(dis.regulatory_cert))
            print('PnP ID: {0}'.format(dis.pnp_id))
    bt.end()

bt = BTLE()
threading.Thread(target=main, args=(bt,)).start()
bt.launch()