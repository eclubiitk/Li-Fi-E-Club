from pydevel import *
# ignore warning due to circular-definition, comment-out the above line in production
def receive():
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
                        fobj.write(st2[:len(st2)-1].strip('\r'))
                        fobj.write('')
                    else:
                        # fobj.write(st2[0])
                        fobj.write(st2[:])
                        # print(st2[:len(st2)-1])
            if(typef==0):
                if(st2=='file\n'):
                    typef=1
                else:
                    typef=2
            st2=''
            serftr.write(true_seq) # true_seq shall act as replacement for Y
        if(flag==2):
            st2=''
            serftr.write(false_seq) # false_seq shall act as replacement for N
    print("Reception Complete!")