import serial
ser = serial.Serial()
ser.baudrate=230400
# ser.port = '/dev/ttyUSB0'
ser.port='COM4'
ser.open()

val=ser.readline()[0]-48
prev=val
counter=1
flag=0
a=1

while True:
    val = ser.readline()[0]-48
    if flag:
        if(val==prev):
            counter+=1
        else:
            if(counter==4 or counter==5):
                if(prev==0):
                    print(0)
                else:
                    print(1)
                a=0
                # for i in range(4):
                #     print(prev)
            elif(counter==2 or counter==3):
                if a:
                    if prev:
                        print(1)
                    else:
                        print(0)
                    a=0
                else:
                    a=1
                # for i in range(2):
                #     print(prev)
            prev=val
            counter=1
    
    else:
        if val:
            flag=1
            counter=1
            prev=val

            
    
