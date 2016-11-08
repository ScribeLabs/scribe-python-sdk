# Scan for and communicate with bluetooth le devices

import uuid
import Queue
import struct
from collections import OrderedDict as OD

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services.servicebase import ServiceBase


SERVICE_UUID = uuid.UUID("00001723-0000-1000-8000-00805f9b34fb") # 16-bit UUID "1723"
RS_SERV_UUID = uuid.UUID("00001723-1212-EFDE-1523-785FEABCD123")
# FIRMWARE_UPDATE_SERVICE_UUID = uuid.UUID("00001530-1212-efde-1523-785feabcd123")
CHAR_UUID = uuid.UUID("00001724-1212-EFDE-1523-785FEABCD123")


# Class to represent a RunScibe device
# Many of the commands aren't completely implemented
class RunScribeDevice(ServiceBase):
    ADVERTISED = [SERVICE_UUID]
    SERVICES = [RS_SERV_UUID]
    CHARACTERISTICS = [CHAR_UUID]

    def __init__(self, device):
        self._service = device.find_service(RS_SERV_UUID)
        self._char = self._service.find_characteristic(CHAR_UUID)
        self._char.start_notify(self._data_received)
        self._responses = {chr(i): Queue.Queue() for i in range(0x41, 0x5a + 1)}
        self.files = []
        self.file_update = False
        self.file_read = False

    def _data_received(self, data):
        print "In data received : " + data[0] 
        if data[0] == "D":
            self._update_fs(data)
        elif data[0] == "R":
            self._update_read(data)
        else:
            self._responses[data[0]].put(data)

    def write(self, value):
        self._char.write_value(value)

    def write_packet(self, value):
        if len(value) <= 20:
            self.write(value + "\x00" * (20 - len(value)))
        else:
            raise Exception("Packet length > 20")

    # Commands
    def reboot(self, type=0):
        if type == 0:
            # soft/default reboot
            self.write_packet("A\x00")
        elif type == 1:
            # hard reboot
            self.write_packet("A\x01")

    def hard_reboot(self):
        self.write_packet("A\x01")

    def annotate_file(self, data1, data2, type=2, event_type=52, fit_event_type=1, event_group=1):
        # FIT event type can be 1 or 2 for to specify Marker Type
        self.write_packet("B" + chr(type) + chr(event_type) + chr(fit_event_type) + chr(event_group) +
                          struct.pack(">I", data1) + struct.pack(">H", data2))
        resp = self._responses["B"].get()
        version_major, version_minor, result = struct.unpack("BBB", resp[1:4])
        if result == 1: # Success
            return {"version major": version_major, "version minor": version_minor}
        else:
            raise Exception("File annotation failed")

    def update_crc_checksum(self, file_block_size, file_point_buf):
        self.write_packet("C" + chr(file_block_size) + struct.pack(">I", file_point_buf))
        resp = self._responses["C"].get()
        return OD(zip(["version major", "version minor", "file total size", "file point reg", "crc high", "crc low"],
                        struct.unpack(">BBIIBB", resp[1:13])))

    def load_file_list(self, all_files=True):
        # Alternative to all files is undeleted files
        self.write_packet("D" + chr(1 if all_files else 2))
        self.file_update = False
        while not self.file_update:
            pass

        return self.files

    def _update_fs(self, resp):
        result = OD(zip(["file list number", "file list index", "file size", "file date", "crc high",
                           "crc low", "crc valid", "file deleted", "MSB", "LSB", "file status"],
                          struct.unpack(">BBIIBBBBBBB", resp[1:18])))

        result["crc valid"] = result["crc valid"] == 1
        result["file deleted"] = result["file deleted"] == 2
        result["file status"] = ["normal", "truncated", "restored"][result["file status"]]

        if result["file size"] == 0xFFFFFFFF:
            result["file size"] = 0

        if not result in self.files:
            self.files.append(result)

        self.file_update = True


    def get_file_info(self, file_list_index, file_block_size=16):
        self.write("I" + struct.pack("BB", file_list_index, file_block_size))
        resp = self._responses["I"].get()
        result = OD(zip(["version major", "version minor", "file list index", "total size", "file point reg",
                         "crc high", "crc low", "crc valid", "file deleted", "MSB", "LSB", "file status"],
                        struct.unpack(">BBBIIBBBBBBB", resp[1:19])))
        result["crc valid"] = result["crc valid"] == 1
        result["file deleted"] = result["file deleted"] == 2
        result["file status"] = ["normal", "truncated", "restored"][result["file status"]]
        return result

    def get_led_color(self):
        self.write_packet("K")
        resp = self._responses["K"].get()
        r, g, b = struct.unpack(">BBB", resp[1:4])
        return (r, g, b)

    def set_led_color(self):
        self.write_packet("J" + chr(255) + chr(0) + chr(0))
        resp = self._responses["J"].get()
        r, g, b = struct.unpack(">BBB", resp[1:4])
        return (r, g, b)        

    def read_data(self, file_list_index, file_point_reg, file_block_size=16):
        self.write_packet("R" + struct.pack(">BBI", file_list_index, file_block_size, file_point_reg))

    def _update_read(self, resp):
        point = ord(resp[1]) << 16 + ord(resp[2]) << 8 + ord(resp[3])
        data = resp[4:20]
        f = open('temp.fit', 'a')
        #print "data: ", repr(data)
        f.write(repr(data))
        f.close()

    def status(self):
        self.write_packet("S")
        resp = self._responses["S"].get()
        result = OD(zip(["version major", "version minor", "battery remaing percent", "file count undeleted",
                           "flash free percent", "temperature", "last access time", "mode", "battery type",
                           "battery mode", "MSB", "LSB", "battery usage time", "file count all", "diagnostics result",
                           "battery charge time"], struct.unpack(">BBBBBbIBBBBBBBBB", resp[1:20])))
        result["mode"] = ["sleeping", "waiting", "recording", "paused", "erasing", "syncing", "manufacture", "error"]\
            [result["mode"]]
        result["battery type"] = ["Primary Lithium", "Lilon", "LiPoly"][result["battery type"]]
        result["battery mode"] = ["active", "idle", "sleep", "charge"][result["battery mode"]]
        result["battery usage time"] *= 10
        result["battery charge time"] *= 10
        # Time results are in minutes
        return result

    def stop_read_data(self):
        self.write_packet("P")
        resp = self._responses["P"].get()
        return OD(zip(["version major", "version minor", "file read crc"], struct.unpack(">BBH", resp[1:5])))

    def read_time(self):
        self.write_packet("W")
        resp = self._responses["W"].get()
        return OD(zip(["version major", "version minor", "system time", "last access time", "last boot time",
                       "time since last boot"], struct.unpack(">BBIIII", resp[1:19])))

    # TODO: Don't know what is device_time_*
    def set_time(self, device_time_0, device_time_1, device_time_2, device_time_3):
        self.write_packet("T" + struct.pack(">IIII", device_time_0, device_time_1, device_time_2, device_time_3))
        resp = self._responses["T"].get()
        return OD(zip(["version_major", "version_minor"], struct.unpack(">BB", resp[1:3])))

    def pooling_status(self):
        self.write_packet("N")
        resp = self._responses["N"].get()
        return OD(zip(["version major", "version minor"], struct.unpack(">BB", resp[1:3])))

    def erase_data(self, erase_type=4 , erase_bit_mask=1):
        self.write_packet("E" + struct.pack(">BB", erase_type, erase_bit_mask))
        resp = self._responses["E"].get()
        return OD(zip(["version major", "version minor", "erase flash result", "file total size", "file point reg",
                         "crc high", "crc low"], struct.unpack(">BBBIIBB", resp[1:14])))

    def manufacturing_mode(self, state=0): # 0 - off, 1 - on
        #if state==0 :
        #    self.write_packet("H" + struct.pack(">B", state))
        self.write_packet("H" + struct.pack(">B", state))
        #else :
        #    self.write_packet("H\x01")
        print 'written packet'
        resp = self._responses["H"].get()
        return OD(zip(["version major", "version minor"], struct.unpack(">BB", resp[1:3])))

    def DFU_mode(self):
        self.write_packet("F")

    def set_mode(self, command=0, state=1):
        self.write_packet("M" + struct.pack(">BB", command, state))
        resp = self._responses["M"].get()
        return OD(zip(["version major", "version minor"], struct.unpack(">BB", resp[1:3])))

    def real_time_polling(self, mode): # 0 => Accel, 1 => Gyro, 2 => Compass
        if mode == 0:
            print "Hello accel"
            self.write_packet("G\x80")
            print "write packet"
            resp = self._responses["G"].get()
            print "return data"
            return OD(zip(["accel 0", "accel 1", "accel 2", "accel 3", "accel 4",
                            "accel 5", "quat 0", "quat 1", "quat 2", "quat 3", "quat 4", "quat 5",
                            "quat 6", "quat 7"], struct.unpack("BBBBBBBBBBBBBB", resp[1:15])))
        elif mode == 1:
            self.write_packet("G\x81")
            resp = self._responses["G"].get()
            return OD(zip(["MPU data index", "gyro 0", "gyro 1", "gyro 2", "gyro 3", "gyro 4",
                            "gyro 5", "quat 0", "quat 1", "quat 2", "quat 3", "quat 4", "quat 5",
                            "quat 6", "quat 7"], struct.unpack("BBBBBBBBBBBBBBB", resp[1:16])))

        else:
            self.write_packet("G\x82")
            resp = self._responses["G"].get()
            return OD(zip(["MPU data index", "compass 0", "compass 1", "compass 2", "compass 3", "compass 4",
                            "compass 5", "quat 0", "quat 1", "quat 2", "quat 3", "quat 4", "quat 5",
                            "quat 6", "quat 7"], struct.unpack("BBBBBBBBBBBBBBB", resp[1:16])))

    def light_led(self):
        self.write_packet("L" + chr(13) + "\x01\x00\x00\xFF")
        resp = self._responses["L"].get()
        return OD(zip(["Mode", "cycles", "R" , "G", "B"],struct.unpack("BBBBB", resp[1:6])))

    def read_config_data(self, configblocksize=16, configpoint=0):
        self.write_packet("U" + struct.pack(">BH", configblocksize, configpoint))
        resp = self._responses["U"].get()
        if configblocksize == 16:
            if configpoint == 0xAA01 or configpoint == 0xAA03:
                return OD(zip(["config block size", "config point buf", "ble device 0", "ble device 1",
                               "ble device 2", "ble device 3", "ble device 4", "ble device 5", "ble device 6",
                               "ble device 7", "ble device 8", "ble device 9", "ble device 10", "ble device 11",
                               "ble device 12", "ble device 13", "ble device 14", "ble device 15", "ble device 16"],
                                struct.unpack("HBBBBBBBBBBBBBBBBB", resp[1:20])))
            elif configpoint == 0xAA02:
                return OD(zip(["config block size", "config point buf", "ble device led color", "heel/lace",
                               "right/left", "device time 0", "device time 1", "device time 2", "device time 3",
                               "device sample rate", "sensitivity", "timeout", "stride rate", "min conn interval",
                               "max conn interval", "ble slave latency"], 
                               struct.unpack("HBBBBBBBBBBBBBBB", resp[1:18])))
            elif configpoint == 0xAA04:
                return OD(zip(["config block size", "config point buf", "heel/lace", "right/left", "timeout", "stride rate",
                            "scale factor A", "scale factor B", "min recording voltage MSB", "min recording voltage LSB",
                            "deep sleep voltage MSB", "deep sleep voltage LSB", "R", "G", "B" ],
                            struct.unpack("HBBBBBBBBBBBBBB",resp[1:17])))
            elif configpoint == 0xAA05:
                return OD(zip(["config block size", "config point buf", "min conn interval", "max conn interval", "ble slave latency"],
                               struct.unpack("HBBBB",resp[1:7])))
            elif configpoint == 0xAA06:
                return OD(zip(["config block size", "config point buf", "raw data"], struct.unpack("HBB", resp[1:5])))
            elif configpoint == 0xAA07:
                return OD(zip(["config block size", "config point buf", "battery capacity"], struct.unpack("HBB", resp[1:5])))
            else:
                return OD(zip(["default","config point buf"], struct.unpack("HB", resp[1:4])))

    def write_config_data(self, packet):
        self.write_packet("V" + packet)
        resp = self._responses["V"].get()
        return OD(zip(["config block size", "config point buf"], struct.unpack("HB", resp[1:4])))

    def perform_diagnostics(self):
        self.write_packet("X\x00")
        resp = self._responses["X"].get()
        return OD(zip(["version major", "version minor", "diagnostics status", "diagnostics result"],struct.unpack("BBBB", resp[1:5])))

    def get_diagnostics_results(self, packetOffset=0):
        self.write_packet("Z" + chr(packetOffset))
        resp = self._responses["Z"].get()
        return OD(zip(["Total packets", "Packet Offset", "buffer chart 0", "buffer chart 1", 
                       "buffer chart 2", "buffer chart 3", "buffer chart 4", "buffer chart 5",
                       "buffer chart 6", "buffer chart 7", "buffer chart 8", "buffer chart 9", 
                       "buffer chart 10", "buffer chart 11", "buffer chart 12", "buffer chart 13",
                       "buffer chart 14"], struct.unpack("BBBBBBBBBBBBBBBBB", resp[1:18])))


# Thread-Safe interface to bluetooth module
class BTLE:
    def __init__(self):
        self.cmd_queue = Queue.Queue()
        self.scanning = False
        self.on_update = None
        self.connected = False
        self.current_device = None
        self.devices = set()

    def launch(self):
        self.ble = Adafruit_BluefruitLE.get_provider()
        self.ble.initialize()
        self.ble.run_mainloop_with(self.mainloop)

    def scan(self, on_update):
        if not self.scanning:
            self.cmd_queue.put(("scan", on_update))

    def stop_scan(self):
        if self.scanning:
            self.cmd_queue.put(("stop scan",))

    def connect_to(self, device):
        if self.connected:
            self.cmd_queue.put(("disconnect",))
        self.cmd_queue.put(("connect", device))
        while not self.current_device is device: pass
        return RunScribeDevice(self.current_device)

    def disconnect(self):
        if self.connected:
            self.cmd_queue.put(("disconnect",))

    def end(self):
        self.stop_scan()
        self.disconnect()
        self.cmd_queue.put(("end",))

    def mainloop(self):
        self.ble.clear_cached_data()
        adapter = self.ble.get_default_adapter()
        adapter.power_on()
        RunScribeDevice.disconnect_devices()

        while True:
            try:
                cmd = self.cmd_queue.get(timeout=1)
                if cmd[0] == "scan":
                    adapter.start_scan()
                    self.on_update = cmd[1]
                    self.scanning = True
                elif cmd[0] == "stop scan":
                    adapter.stop_scan()
                    self.on_update = None
                    self.scanning = False
                elif cmd[0] == "disconnect":
                    self.current_device.disconnect()
                    self.current_device = None
                    self.connected = False
                elif cmd[0] == "connect":
                    cmd[1].connect()
                    RunScribeDevice.discover(cmd[1])
                    self.connected = True
                    self.current_device = cmd[1]
                elif cmd[0] == "end":
                    break
            except Queue.Empty: pass

            if self.scanning:
                devices = set(RunScribeDevice.find_devices())
                if devices != self.devices:
                    if self.on_update:
                        self.on_update(devices)
                    self.devices = devices