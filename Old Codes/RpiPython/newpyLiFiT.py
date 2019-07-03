import RPi.GPIO as gpio
import time
import threading
import os

endwrd="ElEcTrOn" # size should match packlen
endlst=[]
for j in endwrd:
    endlst.append(ord(j))
packlen=8 # IMPORTANT : DETERMINES THE SIZE OF PACKETS 
true_packet=[1]*packlen
false_packet=[0]*packlen
queue = []
start_seq = [1,1,0,0,0,1,0,0,0,1]
end_seq=[0,1,1,0,1,0,0,1,1,1]
sendarr=[0 for i in range(8)]
end_trans=0
time_delay=50*(10**(-6))
timer1=0
skip=0
ack_pack=[0 for i in range(10)]
rec_flag=1

x1={'[0,0,0,0]':[1,1,1,1,0],
'[0,0,0,1]':[0,1,0,0,1],
'[0,0,1,0]':[1,0,1,0,0],
'[0,0,1,1]':[1,0,1,0,1],
'[0,1,0,0]':[0,1,0,1,0],
'[0,1,0,1]':[0,1,0,1,1],
'[0,1,1,0]':[0,1,1,1,0],
'[0,1,1,1]':[0,1,1,1,1],
'[1,0,0,0]':[1,0,0,1,0],
'[1,0,0,1]':[1,0,0,1,1],
'[1,0,1,0]':[1,0,1,1,0],
'[1,0,1,1]':[1,0,1,1,1],
'[1,1,0,0]':[1,1,0,1,0],
'[1,1,0,1]':[1,1,0,1,1],
'[1,1,1,0]':[1,1,1,0,0],
'[1,1,1,1]':[1,1,1,0,1]}

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

def transmit():
    data_queue=[0 for i in range(10)]
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
        queue=[]
        rec_flag=1
        trans=barr[ind:ind+packlen]
        sendarr=trans
        rec_flag=0
        t1=time.time()
        while  True :
            t2=time.time()
            if(t2-t1>1):
                sendarr=trans
                t1=t2
            while queuecomp(data_queue, start_seq) == False :
                val = int(queue.pop(0))
                data_queue.pop(0)
                data_queue.append(val)
                t2=time.time()
                if(t2-t1>0.25):
                    sendarr=trans
                    t1=t2
            while True:
                q=[]
                for i in range(10):
                    data_queue.pop(0)
                    val = queue.pop(0)
                    data_queue.append(int(val))
                    q.append(val)
                if(queuecomp(data_queue, end_seq)==True and len(buff)==packlen):
                    flag=1
                    if(buff==true_packet):
                        response=1
                    else:
                        response=0                            
                    bfind=0
                    buff=[]
                    break
                elif(queuecomp(data_queue, end_seq)==True and len(buff)!=packlen): # in case, end_seq is received but buffer in not full, trigger error response
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
    endtrans=1

###########################################GPIO Sending#######################################################################################

def sendData(x):
    global sendarr, end_trans
    while True:
        if(end_trans):
            break
        if (not len(sendarr)):
            continue
        else:
            new_arr=x1[str(sendarr[0:3])]+x1[str(sendarr[4:7])]
            enc_send(start_seq)
            enc_send(new_arr)
            enc_send(end_seq)
            sendarr=[]
            gpio.output(channel1,gpio.HIGH)

def enc_send(x):
    for i in x:
        if(int(i)):
            gpio.output(channel1, gpio.LOW)
            time.sleep(time_delay)
            gpio.output(channel1, gpio.HIGH)
            time.sleep(time_delay)
            gpio.output(channel1, gpio.LOW)
            time.sleep(time_delay)
            gpio.output(channel1, gpio.HIGH)
            time.sleep(time_delay)
        else:
            gpio.output(channel1, gpio.LOW)
            time.sleep(time_delay*2)
            gpio.output(channel1, gpio.HIGH)
            time.sleep(time_delay*2)

##############################################################################################################################################

###########################################GPIO Reading#######################################################################################

if __name__=="__main__":
    channel=""
    gpio.setup(channel, gpio.IN)
    gpio.add_event_detect(channel, gpio.FALLING)
    gpio.add_event_callback(channel, cleanData)
    channel1=""
    gpio.setup(channel1, gpio.OUT, initial=gpio.HIGH)
    t1 = threading.Thread(target=transmit, name='t1') 
    t2 = threading.Thread(target=sendData, name='t2')
    t1.join()
    t2.join() 

def cleanData():
    global timer1, skip
    timer2=time.time()
    if(timer2-timer1<=50):
        if (not skip):
            queue.append('1')
            skip=1
            if(rec_flag):
                queue.pop(0)
        else:
            skip=0
    else:
        queue.append('0')
        if(rec_flag):
            queue.pop(0)
        skip=0
    timer1=timer2

##############################################################################################################################################