import serial
import time
import os

recport=input('{:<25}'.format("Input Receiver Port : "))
traport=input('{:<25}'.format("Input Transmitter Port : "))

ser = serial.Serial()
ser.baudrate=230400
ser.port=recport #Receiver-(Slave/Master)
ser.open()

serftr = serial.Serial()
serftr.baudrate=9600
serftr.port=traport #Transmitter-(Master-Slave)
serftr.open()

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

ch=input("(T)ransmitter or (R)eceiver : ")

if(ch[0]=='T' or ch[0]=='t'):
    print("Initialising Transmitter. Please Wait ...")
    time.sleep(5)
    fl=input("Text File Path (Leave it empty for text transfer) : ")
    lines = []
    if(fl!=''):
        if(os.path.exists(fl) and os.path.isfile(fl)):
            if(os.name=='nt'):
                fname=fl.split('\\')
            else:
                fname=fl.split('/')
            fname=fname[-1]
            lines.append('file')
            lines.append(fname)
            fl=open(fl, 'r')
            for x in fl:
                lines.append(x)
            fl.close()
            print("File Loaded Successfully.")
        else:
            print("File Specified doesn't exist.")
    else:
        lines.append('gentext')
        print("Start Entering Input")
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
    lines.append('endtrans')
    print("Sending ...")
    response=""
    flag=0
    trans=''
    ind=0
    t1=0
    t2=0
    while (ind<len(lines)):
        trans=lines[ind]+'\n'
        serftr.write(trans.encode())
        t1=time.time()
        while  True :
            t2=time.time()
            if(t2-t1>1):
                serftr.write(trans.encode())
                t1=t2
            while queuecomp(queue, start_seq) == False :
                val = int(ser.readline().decode('ascii')[0])
                queue.pop(0)
                queue.append(val)
                t2=time.time()
                if(t2-t1>0.5):
                    serftr.write(trans.encode())
                    t1=t2
            while True:
                q=[]
                for i in range(10):
                    queue.pop(0)
                    val = (ser.readline().decode('ascii')[0])
                    queue.append(int(val))
                    q.append(val)
                if(queuecomp(queue, end_seq)==True):
                    flag=1
                    break
                queuex=''.join(q)
                q1=x2[queuex[0:5]]
                q2=x2[queuex[5:]]
                num=q1*16+q2
                response=response+chr(num)
            if(flag==1):
                if(response[0]=='N'):
                    response=''
                    break
                elif(response[0]=='Y'):
                    response=''
                    ind+=1
                    break
                else:
                    flag=0
    print("Sending Successful.")
elif(ch[0]=='R' or ch[0]=='r'):
    print("Waiting to Receive ...")
    st1=''
    st2=''
    flag=0
    typef=0
    fname=''
    lnx=0
    fobj=open('none','w')
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
                if(st1!=st2):
                    flag=1
                    st1=st2
                    break
                else:
                    flag=2
                    break
            queuex=''.join(q)
            q1=x2[queuex[0:5]]
            q2=x2[queuex[5:]]
            num=q1*16+q2
            st2=st2+chr(num)
        if(flag==1):
            st1=st2
            if(st2[:len(st2)-1]=='endtrans'):
                if(fname!=''):
                    fobj.close()
                serftr.write('Y\n'.encode())
                break
            if(typef==2):
                print(st2[:len(st2)-1])
            if(typef==1):
                if(fname==''):
                    fname=st2[:len(st2)-1]
                    fobj=open(fname,'w')
                else:
                    if(lnx==0):
                        lnx+=1
                        fobj.write(st2[:len(st2)-1])
                        fobj.write('\r')
                    else:
                        fobj.write(st2[1:])
                        # print(st2[:len(st2)-1])
            if(typef==0):
                if(st2=='file\n'):
                    typef=1
                else:
                    typef=2
            st2=''
            serftr.write('Y\n'.encode())
        if(flag==2):
            st2=''
            serftr.write('Y\n'.encode())
    print("Reception Complete!")
else:
    print("Wrong Choice. Start pyLi-Fi again.")