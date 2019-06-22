import wiringpi
import time
import serial

ser=serial.Serial()

def setup(port):
    ser.baudrate(230400)
    ser.port=port
    ser.open()
    wiringpi.wiringPiSetupGpio()  
    wiringpi.pinMode(25,0)
    ReadData()

def ReadData():
    flag=0
    time1=0
    skip=0

    while True:
        if(wiringpi.digitalRead(25)==1):
            if(not flag):
                time1=time.time()
                flag=1
            else:
                pass
        else:
            if(not flag):
                pass
            else:
                time_temp=time.time()-time1
                flag=0
                time1=0
                if(time_temp<=50):
                    if(not skip):
                        ser.write(1)
                        skip=1
                    else:
                        skip=0
                else:
                    ser.write(0)
                    skip=0

