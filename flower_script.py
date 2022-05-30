import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import time
import struct
import datetime

write_handle = 50
read_handle = 52
write_value = bytearray([0xA0, 0x1F])
time_retry = 3600
history = dict()
def unpack(byte_array):
    record = dict()
    temp_hex = byte_array[0:4]
    sunlight_hex = byte_array[6:14]
    moisture_hex = byte_array[14:16]
    fertility_hex = byte_array[16:20]
    record["temp"] = struct.unpack('<H',bytes.fromhex(temp_hex))[0]/10
    record["sunlight"] = struct.unpack('<HH',bytes.fromhex(sunlight_hex))[0]
    record ["fertility"] = struct.unpack('<H',bytes.fromhex(fertility_hex))[0]
    record["moisture"] =  int(moisture_hex, base=16)
    
    
    print(record)
    return record

async def descover():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
address = "C4:7C:8D:6C:F2:9B"

async def connect(address):
    async with BleakClient(address) as client:
        
        print ("device is connected ")
        while True:
            writeValue= await client.write_gatt_char(write_handle, write_value, response = True)
            newVAlue = await client.read_gatt_char(read_handle)
            history[datetime.datetime.now()] = unpack(newVAlue.hex())
            time.sleep(5)
            
     
        
async def main():   
    while True:
        try:
            await connect(address)
        except Exception as err:
            print("retry to connect ", err)
            continue
            