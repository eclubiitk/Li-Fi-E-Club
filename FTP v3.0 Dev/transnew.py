import os
import json
import sys
import time
import threading
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
queue = [0,0,0,0,0,0,0,0,0,0]
start_seq = [1,1,0,0,0,1,0,0,0,1]
end_seq=[0,1,1,0,1,0,0,1,1,1]
x2={'11110':0,'01001':1,'10100':2,'10101':3,'01010':4,'01011':5,'01110':6,'01111':7,
    '10010':8,'10011':9,'10110':10,'10111':11,'11010':12,'11011':13,'11100':14,'11101':15}
# changeable constants
packlen=8 
WINDOWSIZE=256 # bytes
NTHREADS=4
THREADPACK=WINDOWSIZE//NTHREADS # bytes of each thread
PACKPERWINDOW = THREADPACK//packlen
PACKPERTHREAD = PACKPERWINDOW//NTHREADS
assert((WINDOWSIZE//packlen)>=256),"Ratio of WINDOWSIZE and packlen should be less then the size of a byte."
assert(WINDOWSIZE%NTHREADS==0),"Wrong WINDOWSIZE and NTHREADS : Restore to system defaults."
assert(len(endwrd)==packlen),"Development Error : Handshake won't complete."
# pseudo constants
true_packet=[]
false_packet=[]
INDEX=[]
THLST=[]
sent_packets=[]
# file dependent variables
FILE=[]
FILESIEVE=[] # [current_window][thread_number][packet_index]
FSIZE=0
NPACK=0
# global variables
# INDEX also belongs here 'technically'
current_window=0

# time.sleep(5)
tme = time.time()

def chunker(lst, sz):
    chunks=[]
    sx=len(lst)//sz
    if(len(lst)%sz!=0):
        sx+=1
    for i in range(sx):
        low=i*sz
        upp=(i+1)*sz
        if(upp>len(lst)):
            upp=len(lst)
        chunks.append(lst[low:upp])
    return chunks

def pseudoconst():
    global INDEX, sent_packets, true_packet, false_packet, THLST
    for _ in range(NTHREADS):
        INDEX.append(0)
        sent_packets.append(0)
        THLST.append(0)
    for _ in range(packlen):
        true_packet.append(1)
        false_packet.append(0)

def loader():
    fl=data['fname']
    # fl=sys.argv[1]
    barr=[]
    if(fl!=''):
        if(os.path.exists(fl) and os.path.isfile(fl)):
            fname=fl
            with open(fname, "rb") as fle:
                barr = bytearray(fle.read())
            print("File Loaded Successfully.")
        else:
            print("File specified doesn't exist.",file=sys.stderr)
            sys.exit(1)
        strn=fname
        if(len(strn)<=2*packlen-2):
            g=2*packlen-len(strn)-2
            for i in range(g):
                strn=strn+"0"
        else:
            print("File name too big. Max 14 characters.",file=sys.stderr)
            sys.exit(1)
    barr=strn.encode()+barr
    lbarr=len(barr)
    ind=0
    fx=[]
    gfl=-1
    op=packlen-1
    while(ind<lbarr):
        fx.append(barr[ind])
        ind+=1
        if(ind==op):
            gfl = (gfl+1)%(PACKPERWINDOW)
            op+=packlen-1
            fx.append(gfl)
    barr=bytearray(fx)
    lbarr=len(barr)
    if(lbarr%packlen!=0):
        buff=(lbarr//packlen+1)*packlen-lbarr
        for _ in range(buff):
            barr=barr+bytearray([0])
            lbarr+=1
    lbarr+=packlen #for end packet
    barr=barr+endwrd.encode()
    global FSIZE, NPACK
    FSIZE = lbarr
    NPACK = lbarr//packlen
    return barr

def packeter():
    global FILESIEVE, FILE
    FILE = loader()
    windows=chunker(FILE,WINDOWSIZE)
    threadpack=[]
    for window in windows:
        threadpack.append(chunker(window,THREADPACK))
    windows=threadpack
    for window in windows:
        th=[]
        for thread in window:
            th.append(chunker(thread,packlen))
        FILESIEVE.append(th)

packeter()
def get_packet(i):
    global INDEX
    if(INDEX[i]==len(FILESIEVE[current_window][i])):
        return None
    INDEX[i]+=1
    return FILESIEVE[current_window][i][INDEX[i]-1]

def put_packet(pack):
    global sent_packets
    rp=pack[packlen-1]
    i=rp//PACKPERTHREAD
    sp=sent_packets[i]
    if(sp==0):
        return
    if(sp[packlen-1]==rp):
        sent_packets[i]=0

def transmit(i,lockx):
    global INDEX
    t1=0
    t2=0
    while True:
        if(sent_packets[i]==0):
            t=get_packet(i)
            if(t==None and sent_packets[i]==0):
                break
            elif(t!=0):
                # 4 thread synchronization
                lockx.acquire()
                serftr.write(t)
                lockx.release()
                sent_packets[i]=t
                t1=time.time()
        while sent_packets[i]!=0:
            t2=time.time()
            if(t2-t1>1):
                lockx.acquire()
                serftr.write(sent_packets[i])
                lockx.release()
                t1=t2

def receiver_interface():
    global queue
    buff=[]
    while True:
        while queue!=start_seq:
            val = int(ser.readline().decode('ascii')[0])
            queue.pop(0)
            queue.append(val)
        while True:
            q=[]
            for _ in range(10):
                queue.pop(0)
                val = int(ser.readline().decode('ascii')[0])
                queue.append(int(val))
                q.append(val)
            if(queue==end_seq and len(buff)==packlen):
                if(buff[:packlen-1]==true_packet[:packlen-1]):
                    put_packet(buff)                          
                buff=[]
                break
            elif(queue==end_seq and len(buff)!=packlen): # in case, end_seq is received but buffer in not full, trigger error response
                buff=[]
                break
            queuex=''.join(q)
            try:
                q1=x2[queuex[0:5]]
                q2=x2[queuex[5:]]
                num=q1*16+q2
                buff.append(num)
            except KeyError:
                break

REC=threading.Thread(target=receiver_interface)
REC.start()
while current_window!=len(FILESIEVE):
    lock=threading.lock()
    for i in range(NTHREADS):
        THLST[i]=threading.Thread(target=transmit, args=(i, lock, ))
    for i in range(NTHREADS):
        THLST[i].start()
    for i in range(NTHREADS):
        THLST[i].join()
    current_window+=1

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