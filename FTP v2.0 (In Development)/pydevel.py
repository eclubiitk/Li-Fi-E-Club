import serial
import time
import os
from Transmitter import transmit
from Receiver import receive
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

ch=input("(T)ransmitter or (R)eceiver : ")

if(ch[0]=='T' or ch[0]=='t'):
    transmit()
elif(ch[0]=='R' or ch[0]=='r'):
    receive()
else:
    print("Wrong Choice. Start pyLi-Fi again.")