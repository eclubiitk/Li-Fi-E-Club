from pydevel import *
# ignore warning due to circular-definition, comment-out the above line in production
def transmit():
    print("Initialising Transmitter. Please Wait ...")
    time.sleep(5)
    fl=input("File Path : ")
    # lines = []
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
    # else:
    #     lines.append('gentext')
    #     print("Start Entering Input")
    #     while True:
    #         line = input()
    #         if line:
    #             lines.append(line)
    #         else:
    #             break
    print("Sending ...")
    lbarr=len(barr)
    if(lbarr%packlen!=0):
        buff=(lbarr//packlen+1)*packlen-lbarr
        for bfind in range(buff):
            barr.append(0)
            lbarr+=1
    bfind=0
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
        # acknowledgement system below
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
                if(queuecomp(queue, end_seq)==True and len(buff)==packlen):
                    flag=1
                    if(bfind==packlen):
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
                # replace the code below with receiver protocols
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