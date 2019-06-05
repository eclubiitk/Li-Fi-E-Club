import serial
inp=input("Enter the port : ")
ser=serial.Serial(inp,baudrate=230400,timeout=None)
data_old=0 # always the first-fixed bit
skipped=0
cntr=0
fl=1
su=0
cx=0
while True:
    if (skipped!=0):
        data_old=ser.readline().decode('ascii')[0]
        data_old=int(data_old)
        skipped-=1
        continue
    data_new=ser.readline().decode('ascii')[0]
    data_new=int(data_new)
    if (data_old!=data_new):
        skipped=3
        # print(data_old)
        if(fl==1):
            if(data_old==0):
                cntr+=1
            if(data_old==1):
                cntr=0
            if(cntr==27):
                # print("Connection Established")
                cntr=0
                fl=0
                continue
        if(fl==0):
            cx+=1
            su=int(data_old)+su*2
            if(cx==8):
                print(chr(su), end='')
                cx=0
                su=0