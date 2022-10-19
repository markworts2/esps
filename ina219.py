from machine import Pin, I2C
import ustruct

class INA219(object):
    def __init__(self, i2c=None, scl=None, sda=None,Rsh=0.1,BRNG=1,PG=3,BADC=3,SADC=3,MODE=7, addr=64):
        if not scl:
            scl = Pin(5)
        if not sda:
            sda = Pin(4)
        # construct an I2C bus
        if not i2c:
            i2c = I2C(scl=scl, sda=sda, freq=100000)
        self.i2c = i2c
        
        self.Rsh = Rsh
        self.addr = addr
        
        #write cal
        calstr = bytearray(3)
        calstr[1] = ((BRNG&0x01)<<5)+((PG&0x03)<<3)+((BADC>>1)&0x07)
        calstr[2] = ((BADC&0x01)<<7)+((SADC&0x0F)<<3)+(MODE&0x07)
        self.i2c.writeto(self.addr, calstr)
        
    def readI(self):
        self.i2c.writeto(self.addr, '\1') #select Reg1 Shunt Voltage
        data = self.i2c.readfrom(self.addr, 2)
        data = ustruct.unpack('!h', data)[0]
        return data*self.Rsh #100uV/0.1Ω=1mA
    
    def readV(self):
        self.i2c.writeto(self.addr, '\2') #select Reg2 Bus Voltage
        data = self.i2c.readfrom(self.addr, 2)
        data = ustruct.unpack('!h', data)[0]
        return (data>>3)*4.0 #mV
    
    def readW(self):
        self.i2c.writeto(self.addr, '\3') #select Reg3 Bus Voltage
        data = self.i2c.readfrom(self.addr, 2)
        data = ustruct.unpack('!h', data)[0]
        return data

    def read_current():
        MAX_CURRENT = 3.2 # Amps
        CURRENT_LSB = MAX_CURRENT/(2**15)
        R_SHUNT = 0.1 # Ohms
        CALIBRATION = int(0.04096 / (CURRENT_LSB * R_SHUNT))

        CONF_R = 0x00
        SHUNT_V_R = 0x01
        BUS_V_R = 0x02
        POWER_R = 0x03
        CURRENT_R = 0x04
        CALIBRATION_R = 0x05

        ADDRESS = 0x40

        SDA = Pin(4)
        SCL = Pin(5)
        FREQ = 400000

        i2c = I2C(sda=SDA,scl=SCL,freq=FREQ)
        i2c.writeto_mem(ADDRESS, CALIBRATION_R ,(CALIBRATION).to_bytes(2, 'big'))
        raw_current = int.from_bytes(i2c.readfrom_mem(ADDRESS, SHUNT_V_R, 2), 'big')
        if raw_current >> 15:
            raw_current -= 2**16
        return raw_current * CURRENT_LSB

    
    def read(self):
      return self.readI(), self.readV(), self.readW()
