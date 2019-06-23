import serial
import time
import os
import sys
import json

recport=0
traport=0
user=0

flagsexec={}
if('-f' in sys.argv):
    flagsexec['reset']=True
else:
    flagsexec['reset']=False

if('-t' in sys.argv):
    flagsexec['trans']=True
else:
    flagsexec['trans']=False

if('-r' in sys.argv):
    flagsexec['rec']=True
else:
    flagsexec['rec']=False

confile="pylifi.json"
if(os.path.exists(confile) and os.path.isfile(confile) and not flagsexec['reset']):
    ch=input("Configuration File Detected : Use that ? (Y/N) ")
    if(ch[0]=='y' or ch[0]=='Y'):
        fobj=open(confile,'r')
        jd=json.load(fobj)
        recport=jd['recport']
        traport=jd['traport']
        user=jd['user']
        fobj.close()
    else:
        recport=input('{:<25}'.format("Input Receiver Port : "))
        traport=input('{:<25}'.format("Input Transmitter Port : "))
        user=input('{:<25}'.format("Input Username : "))
        fobj=open(confile,'w')
        jd={}
        jd['recport']=recport
        jd['traport']=traport
        jd['user']=user
        json.dump(jd, fobj)
        fobj.close()
else:
    recport=input('{:<25}'.format("Input Receiver Port : "))
    traport=input('{:<25}'.format("Input Transmitter Port : "))
    user=input('{:<25}'.format("Input Username : "))
    fobj=open(confile,'w')
    jd={}
    jd['recport']=recport
    jd['traport']=traport
    jd['user']=user
    json.dump(jd, fobj)
    fobj.close()

ser = serial.Serial()
ser.baudrate=230400
ser.port=recport #Receiver-(Slave/Master)
ser.open()

serftr = serial.Serial()
serftr.baudrate=9600
serftr.port=traport #Transmitter-(Master-Slave)
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
x2={'11110':0,
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

ch=0
if(flagsexec['trans'] and not flagsexec['rec']):
    ch='T'
elif(flagsexec['rec'] and not flagsexec['trans']):
    ch='R'
else:
    ch=input("(T)ransmitter or (R)eceiver : ")

def receive():
    print("Waiting to Receive ...")
    barr=[]
    cpkt=[]
    ppkt=[]
    flag=0
    fname=''
    dflg=0
    lnx=0
    fobj=open('none','wb')
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
            q1=x2[queuex[0:5]]
            q2=x2[queuex[5:]]
            num=q1*16+q2
            cpkt.append(num)
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
                        fobj=open(fname,'wb')
            cpkt=[]
            serftr.write(bytearray(true_packet)) # true_seq shall act as replacement for Y
        if(flag==2):
            cpkt=[]
            serftr.write(bytearray(false_packet)) # false_seq shall act as replacement for N
    fobj.write(bytearray(barr))
    print("Reception Complete!")

def transmit():
    strn=''
    print("Initialising Transmitter. Please Wait ...")
    time.sleep(5)
    fl=input("File Path : ")
    barr=[]
    if(fl!=''):
        if(os.path.exists(fl) and os.path.isfile(fl)):
            if(os.name=='nt'):
                fname=fl.split('\\')
            else:
                fname=fl.split('/')
            fname=fname[-1]
            with open(fname, "rb") as image:
                barr = bytearray(image.read())
            print("File Loaded Successfully.")
        else:
            print("File Specified doesn't exist.")
            return
        strn=fname
        if(len(strn)<=2*packlen-2):
            g=2*packlen-len(strn)-2
            for i in range(g):
                strn=strn+"0"
        else:
            print("File name too big.")
            return
    print("Sending ...")
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
                for i in range(10):
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
                q1=x2[queuex[0:5]]
                q2=x2[queuex[5:]]
                num=q1*16+q2
                buff.append(num)
            if(flag==1):
                if(response==0):
                    break
                elif(response==1):
                    ind+=packlen
                    break
                else:
                    flag=0
    print("Sending Successful.")

if(ch[0]=='T' or ch[0]=='t'):
    transmit()
elif(ch[0]=='R' or ch[0]=='r'):
    receive()
else:
    print("Wrong Choice. Start pyLi-Fi again.")
