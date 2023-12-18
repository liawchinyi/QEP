from time import sleep
import math
import machine
from machine import ADC, Pin, Timer, SPI, RTC, UART

STATUS_REG = b'\x40'#bytearray(0x40)
CONFIG_WRITE_REG = b'\x10'#bytearray([0x10])
CONFIG_READ_REG = b'\x50'#bytearray(0x50)
ID_REG = b'\x60'#bytearray(0x60)
MODE_WRITE_REG = b'\x08'#bytearray(0x08)
ADC_READ_REG = b'\x58'#bytearray(0x58)#58
IO_READ_REG = b'\x68'#bytearray(0x68)
IO_WRITE_REG = b'\x28'#bytearray(0x28)
RESET = b'\xFF\xFF\xFF\xFF'#bytearray([0xFF, 0XFF, 0XFF])#0xFF, 0XFF, 0XFF, 0XFF

hspi_cs = Pin(17, mode=Pin.OUT, value=1) 

class ADC7793():

    def __init__(self,spi,spi_channel):
        self.spi = spi
        hspi_cs.value(0)
        spi.write(b'\x5C')
        hspi_cs.value(1)

    def RST(self,RS):
        hspi_cs.value(0)
        self.spi.write(RESET)
        RS = self.spi.read(1)
        hspi_cs.value(1)
        return RS
      
    def ID(self,ID2):
        hspi_cs.value(0)
        self.spi.write(ID_REG) 
        ID2 = self.spi.read(1)
        hspi_cs.value(1)
        return ID2

    def STATUS(self,ST):
        hspi_cs.value(0)
        self.spi.write(STATUS_REG)
        ST = self.spi.read(2)
        hspi_cs.value(1)
        return ST

    def SET_MODE(self,MD):
        hspi_cs.value(0)
        self.spi.write(MODE_WRITE_REG)
        self.spi.write(MD)
        MD = self.spi.read(2)
        hspi_cs.value(1)
        return MD
        
    def READ_CONFIG(self,CFR):
        hspi_cs.value(0)
        self.spi.write(CONFIG_READ_REG)
        CFR = self.spi.read(2)
        hspi_cs.value(1)
        return CFR

    def WRITE_CONFIG(self,CFW):
        hspi_cs.value(0)
        self.spi.write(CONFIG_WRITE_REG)
        self.spi.write(CFW)
        CFW = self.spi.read(2)
        hspi_cs.value(1)
        return CFW
        
    def READ_IO(self,CFR):
        hspi_cs.value(0)
        self.spi.write(IO_READ_REG)
        CFR = self.spi.read(1)
        hspi_cs.value(1)
        return CFR

    def WRITE_IO(self,IO):
        hspi_cs.value(0)
        self.spi.write(IO_WRITE_REG)
        value = self.spi.read(1)#1
        hspi_cs.value(1)
        return value
        
    def READ_DATA(self,CHAN):
        hspi_cs.value(0)
        self.spi.write(CONFIG_WRITE_REG)
        self.spi.write(CHAN)

        self.spi.write(ADC_READ_REG)
        value = self.spi.read(2)
        hspi_cs.value(1)
        return value

    def round_up(self, n, decimals=0):
        return math.ceil(n * 5.0) / 65535

