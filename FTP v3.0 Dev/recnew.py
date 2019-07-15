import os
import json
import sys
import time
import threading
import serial

tme = time.time()

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
winlock=threading.lock()
# changeable constants
packlen=8 
WINDOWSIZE=256 # bytes
NTHREADS=4
THREADPACK=WINDOWSIZE//NTHREADS # bytes of each thread
PACKPERWINDOW = WINDOWSIZE//packlen
PACKPERTHREAD = PACKPERWINDOW//NTHREADS
assert(PACKPERWINDOW>=256),"PACKPERWINDOW should be less then the size of a byte."
assert(WINDOWSIZE%NTHREADS==0),"Wrong WINDOWSIZE and NTHREADS : Restore to system defaults."
assert(len(endwrd)==packlen),"Development Error : Handshake won't complete"
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
current_window=-1
npackrec=0

def pseudoconst():
    global INDEX, sent_packets, true_packet, false_packet, THLST
    for _ in range(NTHREADS):
        INDEX.append(0)
        sent_packets.append(0)
        THLST.append(0)
    for _ in range(packlen):
        true_packet.append(1)
        false_packet.append(0)

def getnewwindow():
    global current_window, FILESIEVE, winlock
    window=[]
    for _ in range(NTHREADS):
        window.append([])
    for threads in window:
        for _ in range(PACKPERWINDOW):
            threads.append(0)
    current_window+=1
    FILESIEVE.append(window)

def cleanup():
    fn=FILESIEVE[0][0][0]+FILESIEVE[0][0][1]
    fname=''
    for f in fn:
        if(chr(f)!='0'):
            fname=fname+chr(f)
    FILESIEVE[0][0][0]=0
    FILESIEVE[0][0][1]=0
    filewrite=open('./Received/'+fname, 'w')
    bx=bytearray([])
    for window in FILESIEVE:
        for thread in window:
            for packet in thread:
                if(packet!=0):
                    bx=bx+packet
    filewrite.write(bx)


def place_packet(pack):
    global FILESIEVE,winlock,npackrec,true_packet
    if(pack==endlst):
        return False # always returns False
    rp=pack[packlen-1]
    true_packet[packlen-1]=rp
    i=rp//PACKPERTHREAD
    offset=rp-i*PACKPERTHREAD
    if(FILESIEVE[current_window][i][offset] == 0):
        FILESIEVE[current_window][i][offset]=bytearray(pack[:packlen-1])
        npackrec+=1
    serftr.write(bytearray(true_packet))
    if(npackrec==PACKPERWINDOW):
        getnewwindow()
    return True

def receiver_interface():
    global queue
    buff=[]
    dst = True
    while dst:
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
                dst = place_packet(buff)
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
        cleanup()

getnewwindow()
receiver_interface()

tme=time.time()-tme
datnew = {
    "status":"Successful Reception",
    "time":tme,
    "fname":fname,
    "path":"./Received/"+fname,
    "success":True,
    "type":"R"
}
fw = open("filedata.json","w")
fw.write(json.dumps(datnew))
fw.close()