import TCA9535
import machine
from  machine  import  Pin , I2C 
import time

i2c=machine.I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)   

devices = i2c.scan()
if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))
for device in devices:
    print("At address: ",hex(device))

TCA_Port  =  TCA9535.TCA9535 (i2c, 0x22)

TCA_Port.setoutput(b'\x00\x00')

while True:
    TCA_Port.writebyte(b'\xFF\x00')
    print(b'\xFF\x00')

    time.sleep (0.5)
    
    TCA_Port.writebyte(b'\x00\xFF')
    print(b'\x00\xFF')

    time.sleep (0.5)
