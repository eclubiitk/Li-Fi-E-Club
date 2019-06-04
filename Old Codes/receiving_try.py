import serial
ser = serial.Serial()
ser.baudrate=230400
# ser.port = '/dev/ttyUSB0'
ser.port='COM4'
ser.open()

val=99
prev=100
counter=1
flag=0
a=1
data=[]

while True:
    val = int((ser.readline()[0]-48))
    if (flag==1):
        if(val==prev):
            counter+=1
        else:
            if(counter==4 or counter==5):
                print(prev)
                data.append(prev)
                a=0
            elif(counter==2 or counter==3):
                if a:
                    print(prev)
                    data.append(prev)
                    a=0
                else:
                    a=1
            if(len(data)==7 and data[0]==1 and data[1]==0):
                sum=0
                for i in range(7):
                    sum += data[7-i]*(2**i)
                print(chr(sum))
                data=[]
                flag=2
            prev=val
            counter=1
    elif (flag==0):
        if val==1:
            flag=2
            counter=1
            prev=val
    else:
        if val==0:
            flag=1
            prev=val
            counter=1