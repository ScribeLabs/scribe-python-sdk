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

    def _data_received(self, data):
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
    def soft_reboot(self):
        self.write_packet("A\x00")

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

    def get_file_info(self, file_list_index, file_block_size):
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
        r, g, b = struct.unpack("BBB", resp[1:4])
        return (r, g, b)

    def read_data(self, file_list_index, file_point_reg, file_block_size=16):
        self.write_packet("R" + struct.pack(">BBI", file_list_index, file_block_size, file_point_reg))

    def _update_read(self, resp):
        point = ord(resp[1]) << 16 + ord(resp[2]) << 8 + ord(resp[3])
        data = resp[4:20]
        print "data: ", repr(data)

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