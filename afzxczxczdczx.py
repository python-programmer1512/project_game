import sys
import random
import time
import math
import serial
ser=serial.Serial('COM4',115200)
print("start")
while 1:
    if ser.readable():
        #("ASD")
        res=ser.readline()
        #print("RES")
        ready=res.decode()[:len(res)-2]
        ready=ready.split()
        if len(ready)!=6:
            #print(len(ready))
            continue
        ready=[int(ready[x])for x in range(len(ready))]
        #print(ready)
        if ready[2]==1:print(1)
        if ready[3]==1:print(2)
        if ready[4]==1:print(3)
        if ready[5]==1:print(4)
