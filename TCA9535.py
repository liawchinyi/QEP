import machine
from machine import Pin, PWM
                
class TCA9535:
    #Define register
    TCA9535_IN_REG  = const(0x00) #Input register
    TCA9535_OUT_REG = const(0x02) #Output register
    TCA9535_POL_REG = const(0x04) #Polarity inversion register (1=data inverted)
    TCA9535_DIR_REG = const(0x06) #Configuration register (0=output, 1=input)
    TCA9535_I2CADDR = const(0x22)
    
    def __init__(self, i2c, address=TCA9535_I2CADDR):
        self.i2c = i2c
        self.address = address
        self.port = bytearray(1)
        if i2c.scan().count(address) == 0:
            raise OSError('TCA9535 not found at I2C address {:#x}'.format(address))
        else:
            print('TCA9535 device initialised')
        #"""set bit as output"""
    def setoutput(self,OUT):
        print('setting output to')
        currentvalue = self.i2c.readfrom_mem(TCA9535_I2CADDR , TCA9535_DIR_REG, 1)
        self.i2c.writeto_mem(TCA9535_I2CADDR, TCA9535_DIR_REG , OUT)

        #"""set bit as input"""
    def setinput(self):
        print('setting input to')
        currentvalue = self.i2c.readfrom_mem(TCA9535_I2CADDR , TCA9535_DIR_REG, 1)
        print(currentvalue[0] | (0x01<<self._port))
        self.i2c.writeto_mem(TCA9535_I2CADDR, TCA9535_DIR_REG ,currentvalue[0] | (0x01<<self.port))

    def writebyte(self,value):
        #"""write output byte value"""
		self.i2c.writeto_mem(TCA9535_I2CADDR, TCA9535_OUT_REG, value)
		return
        
    def readbyte(self):
        #"""read input byte value"""
        return self.i2c.readfrom_mem(TCA9535_I2CADDR, TCA9535_IN_REG,1)
        
    def set(self):
        #"""set output bit at 1"""
        currentvalue = self.i2c.readfrom_mem(TCA9535_I2CADDR, TCA9535_OUT_REG,1)
        self.i2c.writeto_mem(TCA9535_I2CADDR, TCA9535_OUT_REG, currentvalue[0] | 1<<self.port)

    def reset(self):
        #"""reset output bit at 0"""
		currentvalue = self.i2c.readfrom_mem(TCA9535_I2CADDR, TCA9535_OUT_REG,1)
		self.i2c.writeto_mem(TCA9535_I2CADDR, TCA9535_OUT_REG, currentvalue[0] & (255-(1<<self.port)))
		return
        
    def get(self):
        #"""read input bit value"""
		linevalue = self.i2c.readfrom_mem(TCA9535_I2CADDR, TCA9535_IN_REG,1)
		ret = ((linevalue >> self.port) & 1 )
		return ret
		    






