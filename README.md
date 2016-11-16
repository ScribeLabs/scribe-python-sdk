# README #

This is a Python SDK for runscribe devices. This SDK provides interface for connecting and communicating with the Runscribe devices through BTLE protocol 

# Version #
1.0

## How do I get set up? ##

Python SDK requires additional support library (called Adafruit Python BluefruitLE : https://github.com/adafruit/Adafruit_Python_BluefruitLE ). Pull git repo using the above link and follow their instructions to install the library into your machine. This library will work only for linux and mac os.

## Example Script ##
Full script containing the examples of each operation : 
``` python console.py ```
Required python version : 2.7 + 


## Usage ##

### To Scan BTLE enabled devices ###
* ** scan(self, on_update) ** : This will scan for nearby BTLE devices and provides a list of all such devices.

```
from btle import BTLE
devices = []
def update_list(current_devices):
        for device in current_devices:
            if not device in devices:
                devices.append(device)
bt = BTLE() 
bt.scan(update_list)
```


### Connect to scribe device ###
* ** connect_to(device) ** : This command will connect to the BTLE device and return connected scribe device. Using this returned scribe we can call more functions, for and can configure the device or get information about connected scribe.
For example to reboot device 
```
from btle import BTLE
bt = BTLE() 
device = devices[1] 
scribe = bt.connect_to(device)
scribe.reboot(r_type) 
```

### Commands related to scribe operations : ###
** reboot ** : reboot the device

```scribe.reboot(r_type)```

##### r_type : 0 - Soft reboot, 1 - Hard reboot #####



** update crc ** : update crc checksum

```scribe.update_crc_checksum(file_block_size = 16, file_point_buffer = 0)```
##### Input : file block size, file point buffer #####
##### Output : version major, version minor, file total size, file point reg, crc high, crc low #####

** load file list **: load file list stored in scribe

```scribe.load_file_list (file_type = 0)```

##### Input : file_type : 0,1 - all files, 2 - undeleted file #####
##### Output : File list number, File list index, File size, File date, crc high, crc low, crc valid, File deleted, MSB, LSB, File status #####


** erase data **: Erase data from scribe

```scribe.erase_data(erase_type = 4, erase_bit_mask = 1)```
##### Input : erase_type : 1 - partial , 0,2 - chip, 3 - deleted, 4 - EEPROM/Default, erase_bit_mask : 1 - file #####
##### Output : version major, version minor, erase flash result, file total size, file point reg, crc high, crc low #####
 
** DFU mode ** : set device into DFU mode

```scribe.DFU_mode()```


** real time polling ** :

```scribe.real_time_polling(mode = 0)```

##### Input : mode : 0 - Accel, 1 - Gyro, 2 - Compass #####
##### Output : If mode == 0 then Accel 0...5, Quat 0...7 #####

##### If mode == 1,2 then MPU data index, Gyro 0...5/ Compass 0...5, Quat 0...7 #####


** manufacturing mode **: 

```scribe.manufacturing_mode(state = 1)```

##### Input : state : 0 - off, 1 - on #####
##### Output : version major, version minor #####


** file information **: File information of file stored in scribe

```scribe.get_file_info(file_index = 0, file_block_size = 16)```

##### Input : file_index, file_block_size (default - 16) #####
##### Output : version major, version minor, file list index, total size, file point reg, crc high, crc low, crc valid, file deleted, MSB, LSB, file status #####

** set led color **: Set led color of device

```scribe.set_led_color(255, 0, 255)```

##### Input : r, g, b - colour can be one of the four colours - green, yellow, blue,  purple #####
##### Output : r, g, b #####

** get led color **:

```scribe.get_led_color()```

##### Output : r, g, b #####

** light **:

```scribe.light_led(mode = 14, cycles = 1, r = 255, g = 0,b = 0)```

##### Input : mode : 13 - connected, 14 - recording, 15 - syncing, 16 - sync_complete, 17 -low_bettery, cycles - default 1, Red, Green, Blue #####
##### Output : mode, cycles, r, g, b #####

** set mode **:

```scribe.set_mode(command = 0, state = 1)```
##### Input : command : 0 - N/A, 1 - record, 2 - pause, 3 - sync, state : 0 - off, 1 - on #####
##### Output : version major, version minor #####
 
** polling status **:

```scribe.polling_status()```

##### Output : version major, version minor #####
 
** stop read data **: 

```scribe.stop_read_data()```
##### Output : version major, version minor, file read crc #####

** read data **: 

```scribe.read_data(file_index = 0, block_data_point = 0)```
##### Input : file_index, block_data_point #####
##### Output : Data written to ****.fit (**** is device serial number) file that can be parse by fit parser. See below for details how to install fit parser and how to use it.

** status **:

```scribe.status()```
##### Output : version major, version minor, battery remaining percent, file count undeleted, flash free percent, temperature, last access time, mode, battery type, battery mode, MSB, LSB, battery usage time, file count all, diagnostics result, battery charge time #####

** set time **:

```scribe.set_time(deviceTime[0] = 45, deviceTime[1] = 50, deviceTime[2] = 57, deviceTIme[3] = 39 )```

##### Input : deviceTime[0], deviceTime[1], deviceTime[2], deviceTime[3] #####
##### Output : version major, version minor #####


** read time ** :

```scribe.read_time()```
##### Output : version major, version minor, system time, last access time, last boot time, time since last boot #####


** Read configuration data **:

```scribe.read_config_data(config_block_size = 16, config_point = 0xAA02)```
##### Input : config_point - 0xAA01...07, config_block_size - default 16 #####

##### Output : 
##### if config_point == 0xAA01 or 0xAA03 then config block size, config point buf, ble device 0..16 #####
##### if config_point == 0xAA02 then config block size, config point buf, ble device led color, heel/lace, right/left, device time 0..3, device sample rate, sensitivity, timeout, stride rate, min conn interval, max conn interval, ble slave latency #####
##### if config_point == 0xAA04 then config block size, config point buf, heel/lace, right/left, timeout, stride rate, scale factor A, scale factor B, min recording voltage MSB, min recording voltage LSB, deep sleep voltage MSB, deep sleep voltage LSB, R, G, B #####
##### if config_point == 0xAA05 then config block size, config point buf, min conn interval, max conn interval, ble slave latency #####
##### if config_point == 0xAA06 then config block size, config point buf, raw data #####
##### if config_point == 0xAA07 then config block size, config point buf, battery capacity #####


** Write configuration data **:

```
packet = struct.pack(">BHBBB", configblocksize = 16, configpoint = 0xAA05, min_conn_interval = 25, max_conn_interval = 35, ble_slave_latency = 0)
scribe.write_config_data(packet)
```
##### Input : config_point - 0xAA01...07, config_block_size - default - 16, 
##### if config_point == 0xAA01 or 0xAA03 then Ble device 0…15
##### if config_point == 0xAA02 then Block size, led color, heel/lace, right/left, deviceTime[0..3], deviceSampleRate, sensitivity, Timeout, strideRate, minConnInterval, maxConnInterval, bleSlaveLatency #####
##### if config_point == 0xAA04 then Block size,  heel/lace, right/left, Timeout, strideRate, scale_factor_A, scale_factor_B, min_recording_voltage_MSB, max_recording_voltage_LSB, deep_sleep_voltage_LSB, deep_sleep_voltage_MSB, deep_sleep_voltage_LSB, R, G, B #####
##### if config_point == 0xAA05 then Block size, minConnInterval, maxConnInterval, bleSlaveLatency #####
##### if config_point == 0xAA06 then Block size, raw data #####
##### if config_point == 0xAA07 then Block size, better capacity #####

##### Output : config block size, config point but #####

** Perform Diagnostics **: 

```scribe.perform_diagnostics(update_calibration = 0)```
##### Input : update_calibration - default 0 #####
##### Output : version major, version minor, diagnostics status, diagnostics result #####


** Get diagnostics results **:
```scribe.get_diagnostics_result(packetOffset = 0)```
##### Input : Packet offset - default 0 #####
##### Output : total packets, packet offset, buffer char 0...14 #####


** device Information services ** :

```
from Adafruit_BluefruitLE.services import DeviceInformation
dis = DeviceInformation(device)
print('Manufacturer: {0}'.format(dis.manufacturer))
print('Model: {0}'.format(dis.model))
print('Serial: {0}'.format(dis.serial))
print('Hardware Revision: {0}'.format(dis.hw_revision))
print('Software Revision: {0}'.format(dis.sw_revision))
print('Firmware Revision: {0}'.format(dis.fw_revision))
print('System ID: {0}'.format(dis.system_id))
print('Regulatory Cert: {0}'.format(dis.regulatory_cert))
print('PnP ID: {0}'.format(dis.pnp_id))

```

##### Input : device 
##### Output : Manufacturer, Model, Serial, Hw_revision, Sw_revision, Fw_revision, System_id, Regulatory_cert, Pnp_id