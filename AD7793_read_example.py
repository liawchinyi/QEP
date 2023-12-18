import AD7793
import time
import machine
from machine import ADC, Pin, Timer, SPI, RTC, UART

hspi = SPI(1, 10000000, polarity=1, phase=1, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
ADC = AD7793.ADC7793(hspi,1)

# Set Mode register of the ADC ( See page 15 of datasheet for options)
MD =b'\x00\x41'#bytearray(0x00, 0x0A)   #   16 bit Mode register [MSB[8], LSB[8]]   Page 15 of Datasheet 
                                          
CFW1 =b'\x10\x10'#bytearray(0x00, 0x80)   #   16 bit Configuration register [MSB[8], LSB[8]] 
CFW2 =b'\x10\x11'#bytearray(0x00, 0x80)   #   16 bit Configuration register [MSB[8], LSB[8]]
CFW3 =b'\x10\x16'#Temp Sensor
CFW4 =b'\x10\x17'#AVDD Monitor
                      
# Reset the ADC                                                                            
print("RESET",hex(ADC.RST(0)[0]))
# Get the ADC ID and model number
print("ID",hex(ADC.ID(0)[0]))
# See if the ADC is ready
print("STATUS",hex(ADC.STATUS(0)[0]))

# Set the mode register
print("MODE",hex(ADC.SET_MODE(MD)[0]))

# Set the Configuration register
print("CONFIG-WRI",hex(ADC.WRITE_CONFIG(CFW1)[0]))
# Read the configuration register to verify 
print("CONFIG-R",hex(ADC.READ_CONFIG(0)[0]),hex(ADC.READ_CONFIG(0)[1]))

# Continouosly read the voltage
while True:
    
    DATA = ADC.READ_DATA(CFW1)
    V1= int((DATA[0]<<8)+(DATA[1]))
    time.sleep(0.1)
    
    DATA = ADC.READ_DATA(CFW2)
    V2= int((DATA[0]<<8)+(DATA[1]))
    
    print ("Voltage", ADC.round_up(V1,4), "V ", ADC.round_up(V2,4), "V ") # rounding up the voltage to 4 decimal points
    time.sleep(0.1)
    #break
