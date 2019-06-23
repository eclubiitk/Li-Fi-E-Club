import RPi.GPIO as gpio
import time
import threading

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

timer1=0
skip=0
endwrd="ElEcTrOn" # size should match packlen
endlst=[]
for j in endwrd:
    endlst.append(ord(j))
packlen=8 # IMPORTANT : DETERMINES THE SIZE OF PACKETS 
true_packet=[1,1,1,0,1,1,1,1,0,1]
false_packet=[1,1,1,1,0,1,1,1,1,0]
queue = [0,0,0,0,0,0,0,0,0,0]
start_seq = [1,1,0,0,0,1,0,0,0,1]
end_seq=[0,1,1,0,1,0,0,1,1,1]
sendarr=[]
end_trans=0
time_delay=50*(10**(-6))
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

########################################GPIO Reading###########################################################
if __name__=="__main__":
    channel=""
    gpio.setup(channel, gpio.IN)
    gpio.add_event_detect(channel, gpio.FALLING)
    gpio.add_event_callback(channel, cleanData)
    channel1=""
    gpio.setup(channel1, gpio.OUT, initial=gpio.HIGH)
    t1 = threading.Thread(target=receive, name='t1') 
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
            else:
                skip=0
        else:
            queue.append('0')
            skip=0
        timer1=timer2
    
    
##########################################################################################################

##########################################GPIO Sending###########################################################
def sendData():
    global sendarr, end_trans
    while True:
        if(end_trans):
            break
        if (not len(sendarr)):
            continue
        else:
            enc_send(start_seq)
            enc_send(sendarr)
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
###############################################################################################################

def receive():
    print("Waiting to Receive ...")
    data_queue=[0 for i in range(10)]
    barr=[]
    cpkt=[]
    ppkt=[]
    flag=0
    fname=''
    dflg=0
    lnx=0
    fobj=open('none','wb')
    while  True :
        while queuecomp(data_queue, start_seq) == False :
            if(len(queue>10)):
                val = int(queue.pop(0))
                data_queue.pop(0)
                data_queue.append(val)
        while True:
            q=[]
            for i in range(10):
                data_queue.pop(0)
                val = queue.pop(0)
                data_queue.append(int(val))
                q.append(val)
            if(queuecomp(data_queue, end_seq)==True):
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
                sendarr=bytearray(true_packet)
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
            sendarr=bytearray(true_packet) # true_seq shall act as replacement for Y
        if(flag==2):
            cpkt=[]
            sendarr=bytearray(false_packet) # false_seq shall act as replacement for N
    fobj.write(bytearray(barr))
    print("Reception Complete!")
    end_trans=1

gpio.cleanup()