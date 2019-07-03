import os
import json
import sys
import time
import serial

tme = time.time()

fr = open("config.json","r")
data = json.load(fr)
fr.close()

recport=data['recport']
traport=data['traport']
# user=data['user']

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

print("Waiting to Receive ...")
barr=[]
cpkt=[]
ppkt=[]
flag=0
fname=''
dflg=0
lnx=0
fobj=open('./Received/none','wb')
while  True :
    while queuecomp(queue, start_seq) == False :
        val = int(ser.readline().decode('ascii')[0])
        queue.pop(0)
        queue.append(val)
    while True:
        q=[]
        for i in range(10):
            queue.pop(0)
            val = (ser.readline().decode('ascii')[0])
            queue.append(int(val))
            q.append(val)
        if(queuecomp(queue, end_seq)==True):
            if(len(cpkt)==packlen):
                if(ppkt!=cpkt):
                    flag=1
                else:
                    flag=3
            else:
                flag=2
            break
        queuex=''.join(q)
        try:
            q1=x2[queuex[0:5]]
            q2=x2[queuex[5:]]
            num=q1*16+q2
            cpkt.append(num)
        except KeyError:
            flag=2
            break
    if(flag==1 or flag==3):
        ppkt=cpkt
        if(cpkt==endlst): #affected by packlen, individual and robust modification needed
            serftr.write(bytearray(true_packet))
            break
        if(flag==1):
            if(dflg==2):
                barr=barr+cpkt[:packlen-1]
            else:
                dflg+=1
                for b in cpkt:
                    if(chr(b)!='0' and b!=0 and b!=1):
                        fname=fname+chr(b)
                if(dflg==2):
                    fobj=open("./Received/"+fname,'wb')
        cpkt=[]
        serftr.write(bytearray(true_packet)) # true_seq shall act as replacement for Y
    if(flag==2):
        cpkt=[]
        serftr.write(bytearray(false_packet)) # false_seq shall act as replacement for N
fobj.write(bytearray(barr))

tme=time.time()-tme
datnew = {
    "status":"Successful Reception",
    "time":str(tme)
}
fw = open("filedata.json","w")
fw.write(json.dumps(datnew))
fw.close()