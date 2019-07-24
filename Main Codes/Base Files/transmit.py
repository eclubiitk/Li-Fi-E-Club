import os
import json
import sys
import time
import serial

fr = open("config.json","r")
data = json.load(fr)
fr.close()

recport=data['recport']
traport=data['traport']

fr = open("filedata.json","r")
data = json.load(fr)
fr.close()

ser = serial.Serial()
ser.baudrate=230400
ser.port=recport
ser.open()

serftr = serial.Serial()
serftr.baudrate=9600
serftr.port=traport
serftr.open()

endwrd="ElEcTrOn" # size should match packlen
endlst=[]
for j in endwrd:
    endlst.append(ord(j))
packlen=8 # IMPORTANT : DETERMINES THE SIZE OF PACKETS 
true_packet=[1]*packlen
false_packet=[0]*packlen
queue = [0,0,0,0,0,0,0,0,0,0]
start_seq = [1,1,0,0,0,1,0,0,0,1]
end_seq=[0,1,1,0,1,0,0,1,1,1]
x2={
    '11110':0,
    '01001':1,
    '10100':2,
    '10101':3,
    '01010':4,
    '01011':5,
    '01110':6,
    '01111':7,
    '10010':8,
    '10011':9,
    '10110':10,
    '10111':11,
    '11010':12,
    '11011':13,
    '11100':14,
    '11101':15}

def queuecomp(queue1, queue2) :
    if(queue1!=queue2):
        return False
    return True

strn=''
time.sleep(5)

tme = time.time()

def transmit():
    fl=data['fname']
    fp=data['path']
    barr=[]
    if(fl!=''):
        if(os.path.exists(fp) and os.path.isfile(fp)):
            fname=fl
            with open(fname, "rb") as image:
                barr = bytearray(image.read())
            print("File Loaded Successfully.")
        else:
            print("File Specified doesn't exist.")
            return
        strn=fname
        if(len(strn)<=2*packlen-2):
            g=2*packlen-len(strn)-2
            for _ in range(g):
                strn=strn+"0"
        else:
            print("File name too big.")
            return
    barr=strn.encode()+barr
    lbarr=len(barr)
    ind=0
    fx=[]
    gfl=0
    op=packlen-1
    while(ind<lbarr):
        fx.append(barr[ind])
        ind+=1
        if(gfl>0):
            gfl=0
        else:
            gfl=1
        if(ind==op):
            op+=packlen-1
            fx.append(gfl)
    barr=bytearray(fx)
    lbarr=len(barr)
    if(lbarr%packlen!=0):
        buff=(lbarr//packlen+1)*packlen-lbarr
        for bfind in range(buff):
            barr=barr+bytearray([0])
            lbarr+=1
    lbarr+=8 #for end packet
    barr=barr+endwrd.encode()
    buff=[]
    response=""
    flag=0
    trans=''
    ind=0
    t1=0
    t2=0
    while (ind<lbarr):
        trans=barr[ind:ind+packlen]
        serftr.write(trans)
        t1=time.time()
        while  True :
            t2=time.time()
            if(t2-t1>1):
                serftr.write(trans)
                t1=t2
            while queuecomp(queue, start_seq) == False :
                val = int(ser.readline().decode('ascii')[0])
                queue.pop(0)
                queue.append(val)
                t2=time.time()
                if(t2-t1>0.25):
                    serftr.write(trans)
                    t1=t2
            while True:
                q=[]
                for _ in range(10):
                    queue.pop(0)
                    val = (ser.readline().decode('ascii')[0])
                    queue.append(int(val))
                    q.append(val)
                if(queuecomp(queue, end_seq)==True and len(buff)==packlen):
                    flag=1
                    if(buff==true_packet):
                        response=1
                    else:
                        response=0                            
                    bfind=0
                    buff=[]
                    break
                elif(queuecomp(queue, end_seq)==True and len(buff)!=packlen): # in case, end_seq is received but buffer in not full, trigger error response
                    buff=[]
                    bfind+=1
                    break
                queuex=''.join(q)
                try:
                    q1=x2[queuex[0:5]]
                    q2=x2[queuex[5:]]
                    num=q1*16+q2
                    buff.append(num)
                except KeyError:
                    response=0
                    flag=1
                    break
            if(flag==1):
                if(response==0):
                    break
                elif(response==1):
                    ind+=packlen
                    break
                else:
                    flag=0

transmit()
tme=time.time()-tme
datnew = {
    "status":"Successful Transmission",
    "time":tme,
    "success":True,
    "type":"T"
}
fw = open("filedata.json","w")
fw.write(json.dumps(datnew))
fw.close()