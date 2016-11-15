# README #

This is a Python SDK for runscribe devices. 
### What is this repository for? ###

* Quick summary
This SDK provides interface for connecting and communicating with the Runscribe devices through BTLE protocol 
* Version 1.0
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

Python SDK requires additional support library (called Adafruit Python BluefruitLE : https://github.com/adafruit/Adafruit_Python_BluefruitLE ). Pull git repo using the above link and follow their instructions to install the library into your machine. This library will work only for linux and mac os.

### Example Script ###
Full script containing the examples of each operation : python console.py
Required python version : 2.7 + 


### Usage ###

* To Scan BTLE enabled devices :
* * scan(self, on_update)
    This will scan for nearby BTLE devices and provides a list of all such devices.


*from btle import BTLE
devices = []
def update_list(current_devices):
        for device in current_devices:
            if not device in devices:
                devices.append(device)
bt = BTLE() 
bt.scan(update_list)
*


* Connect to scribe device : 
* * connect_to(device)
 This command will connect to the BTLE device and return connected scribe device. Using this returned scribe we can call more functions, for and can configure the device or get information about connected scribe.

For example to reboot device  :

*from btle import BTLE
bt = BTLE() 
device = devices[1] 
scribe = bt.connect_to(device)
scribe.reboot(r_type) 

*


#### Commands related to scribe operations : ####
* reboot : 
* * Inputs : 
* * * r_type : 0 - soft, 1 - Hard reboot
* * Output : nil
Example: 
scribe.reboot(r_type)


 update crc :
Input : file block size, file point buffer
Output : version major, version minor, file total size, file point reg, crc high, crc low
Example:
scribe.update_crc_checksum(file_block_size = 16, file_point_buffer = 0)
version major: 20
version minor: 16
file total size: 1000
file point reg: 0
crc high: 255
crc low: 255


load file list : 
Input : file_type // 0,1 - all files, 2 - undeleted file
Output : file information like :
File list number
File list index
File size
File date
Crc high
Crc low
Crc valid
File deleted
MSB
LSB
File status
Example :
scribe.load_file_list (file_type = 0)
file list number: 1
file list index: 0
file size: 218
file date: 847781232
crc high: 163
crc low: 169
crc valid: True
file deleted: False
MSB: 0
LSB: 0
file status: normal


erase data :
Input : 
erase_type  // 1 - partial , 0,2 - chip, 3 - deleted, 4 - EEPROM/Default
erase_bit_mask // 1 - file 
Output : version major, version minor, erase flash result, file total size, file point reg, crc high, crc low
Example :
scribe.erase_data(erase_type = 4, erase_bit_mask = 1)
version major: 20
version minor: 16
erase flash result: 2
file total size: 0
file point reg: 0
crc high: 255
crc low: 255
 
DFU mode :
Input : nil
Output : nil
Example :
scribe.DFU_mode()


real time polling :
Input : mode // 0 - Accel, 1 - Gyro, 2 - Compass
Output : 
If mode == 1,2 then MPU data index
Accel 0...5 / Gyro 0...5/ Compass 0...5
Quat 0...7
Example :
scribe.real_time_polling(mode = 0)
accel 0: 128
accel 1: 201
accel 2: 255
accel 3: 3
accel 4: 1
accel 5: 59
quat 0: 8
quat 1: 20
quat 2: 210
quat 3: 57
quat 4: 44
quat 5: 151
quat 6: 5
quat 7: 92


manufacturing mode : 
Input : state // 0 - off, 1 - on
Output : version major, version minor
Example :
scribe.manufacturing_mode(state = 1)
version major: 20
version minor: 16


file information : 
Input : file_index, file_block_size (default - 16)
Output : version major, version minor, file list index, total size, file point reg, crc high, crc low, crc valid, file deleted, MSB, LSB, file status
Example :
scribe.get_file_info(file_index = 0, file_block_size = 16)
version major: 20
version minor: 16
file list index: 0
total size: 4294967295
file point reg: 0
crc high: 0
crc low: 0
crc valid: False
file deleted: False
MSB: 0
LSB: 0
file status: normal


set led color : 
Input : color // 0 - green 1 - yellow 2 - blue 3 - purple
Output : r, g, b
Example : 
scribe.set_led_color(255, 0, 255)
Red : 255, Green: 0, Blue: 255


get led color :
Input : nil
Output : r, g, b
Example :
scribe.get_led_color()
Red : 255, Green: 0, Blue: 255


light :
Input :
mode // 13 - connected, 14 - recording, 15 - syncing, 16 - sync_complete, 17 - low_bettery
cycles // default 1
Red
Green
Blue
Output : mode, cycles, r, g, b
Example :
scribe.light_led(mode = 14, cycles = 1, r = 255, g = 0,b = 0)
Mode: 14
cycles: 1
R: 255
G: 0
B: 0




set mode :
Input : 
command // 0 - N/A, 1 - record, 2 - pause, 3 - sync
state // 0 - off, 1 - on
Output : version major, version minor
Example :
scribe.set_mode(command = 0, state = 1)
version major: 20
version minor: 16
 
polling status :
Input : nil
Output : version major, version minor
Example :
scribe.polling_status()
version major: 20
version minor: 16
 
stop read data: 
Input : nil
Output : version major, version minor, file read crc
Example :
scribe.stop_read_data()
version major: 20
version minor: 16
file read crc: 0




read data : 
Input : file_index, block_data_point
Output : Data written to temp.fit file that can be parse by fit parser. See below for details. 
Example :
scribe.read_data(file_index = 0, block_data_point = 0)


status :
Input : nil 
Output : version major, version minor, battery remaining percent, file count undeleted, flash free percent, temperature, last access time, mode, battery type, battery mode, MSB, LSB, battery usage time, file count all, diagnostics result, battery charge time
Example :
scribe.status()
version major: 20
version minor: 16
battery remaining percent: 77
file count undeleted: 1
flash free percent: 100
temperature: 21
last access time: 0
mode: manufacture
battery type: LiPoly
battery mode: active
MSB: 15
LSB: 79
battery usage time: 20
file count all: 1
diagnostics result: 64
battery charge time: 70


set time :
Input : deviceTime[0], deviceTime[1], deviceTime[2], deviceTime[3]
Output : version major, version minor
Example :
scribe.set_time(deviceTime[0] = 45, deviceTime[1] = 50, deviceTime[2] = 57, deviceTIme[3] = 39 )
version_major: 20
version_minor: 16


read time :
Input : nil
Output : version major, version minor, system time, last access time, last boot time, time since last boot
Example :
scribe.read_time()
version major: 20
version minor: 16
system time: 1320
last access time: 0
last boot time: 0
time since last boot: 1320


Read configuration data :
Input :
config_point // 0xAA01...07
config_block_size // default - 16
Output : 
config_point == 0xAA01 or 0xAA03
config block size, config point buf, ble device 0..16 
config_point == 0xAA02
config block size, config point buf, ble device led color, heel/lace, right/left, device time 0..3, device sample rate, sensitivity, timeout, stride rate, min conn interval, max conn interval, ble slave latency
config_point == 0xAA04
config block size, config point buf, heel/lace, right/left, timeout, stride rate, scale factor A, scale factor B, min recording voltage MSB, min recording voltage LSB, deep sleep voltage MSB, deep sleep voltage LSB, R, G, B
config_point == 0xAA05
config block size, config point buf, min conn interval, max conn interval, ble slave latency
config_point == 0xAA06
config block size, config point buf, raw data
config_point == 0xAA07
config block size, config point buf, battery capacity
Example :
scribe.read_config_data(config_block_size = 16, config_point = 0xAA02)
config block size: 43536
config point buf: 2
ble device led color: 0
heel/lace: 0
right/left: 0
device time 0: 45
device time 1: 50
device time 2: 57
device time 3: 39
device sample rate: 0
sensitivity: 5
timeout: 30
stride rate: 80
min conn interval: 20
max conn interval: 40
ble slave latency: 0




Write configuration data :
Input :
config_point // 0xAA01...07
config_block_size // default - 16
config_point == 0xAA01 or 0xAA03
Ble device 0…15  
config_point == 0xAA02
Block size, led color, heel/lace, right/left, deviceTime[0..3], deviceSampleRate, sensitivity, Timeout, strideRate, minConnInterval, maxConnInterval, bleSlaveLatency
config_point == 0xAA04 
Block size,  heel/lace, right/left, Timeout, strideRate, scale_factor_A, scale_factor_B, min_recording_voltage_MSB,max_recording_voltage_LSB, deep_sleep_voltage_LSB, deep_sleep_voltage_MSB, deep_sleep_voltage_LSB, R, G, B
config_point == 0xAA05
Block size, minConnInterval, maxConnInterval, bleSlaveLatency
config_point == 0xAA06
Block size, raw data
config_point == 0xAA07
Block size, bettery capacity 
 Output : config block size, config point buf
Example :
packet = struct.pack(">BHBBB", configblocksize = 16, configpoint = 0xAA05, min_conn_interval = 25, max_conn_interval = 35, ble_slave_latency = 0)
scribe.write_config_data(packet)  // packet is struct.pack of above parameters
config block size: 43536
config point buf: 5


Perform Diagnostics : 
Input :
update_calibration // default 0
 Output : version major, version minor, diagnostics status, diagnostics result
Example :
scribe.perform_diagnostics(update_calibration = 0)
version major: 20
version minor: 16
diagnostics status: 2
diagnostics result: 103


Get diagnostics results :
Input : Packet offset  // default 0 
Output : total packets, packet offset, buffer char 0...14
Example :
scribe.get_diagnostics_result(packetOffset = 0)
Total packets: 24
Packet Offset: 0
buffer chart 0: 82
buffer chart 1: 117
buffer chart 2: 110
buffer chart 3: 83
buffer chart 4: 99
buffer chart 5: 114
buffer chart 6: 105
buffer chart 7: 98
buffer chart 8: 101
buffer chart 9: 32
buffer chart 10: 68
buffer chart 11: 105
buffer chart 12: 97
buffer chart 13: 103
buffer chart 14: 110


device Information services :
Input : device 
Output : 
Manufacturer
Model
Serial
Hw_revision
Sw_revision
Fw_revision
System_id
Regulatory_cert
Pnp_id
Example :
from Adafruit_BluefruitLE.services import DeviceInformation
dis = DeviceInformation(device)
dis.manufacturer - Manufacturer: ScribeLabs
dis.model - Model: None
dis.serial - Serial: b8ef4c5773b593a1
dis.hw_revision - Hardware Revision: 2.0
dis.sw_revision - Software Revision: 2.3-7.2
dis.fw_revision - Firmware Revision: 20.16
dis.system_id - System ID: None
dis.regulatory_cert - Regulatory Cert: None
dis.pnp_id - PnP ID: None



