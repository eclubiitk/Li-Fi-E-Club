# from pydevel import *
# ignore warning due to circular-definition, comment-out the above line in production
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
                        flag=2
                else:
                    flag=2
                break
            queuex=''.join(q)
            q1=x2[queuex[0:5]]
            q2=x2[queuex[5:]]
            num=q1*16+q2
            cpkt.append(num)
        if(flag==1):
            ppkt=cpkt
            if(dflg>2):
                barr=barr+cpkt
            else:
                dflg+=1
                for b in cpkt:
                    if(chr(b)!='0'):
                        fname=fname+chr(b)
            cpkt=[]
            for m in range(8):
                serftr.write(bytearray([1])) # true_seq shall act as replacement for Y
        if(flag==2):
            cpkt=[]
            for m in range(8):
                serftr.write(bytearray([0])) # false_seq shall act as replacement for N
    fobj.write(bytearray(barr))
    print("Reception Complete!")