from socket import *
import sys
import select
from pygame import mixer 
host="0.0.0.0"
port = 5099
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1024
mixer.init()
while(True):
    f = open("output.wav",'wb')

    print("while")
    while(True):

        data,addr = s.recvfrom(buf)
        if(data):
            f.write(data)
        else:
            break;

	
    f.close()
    print("output.wav\n")
    mixer.music.load("output.wav")
    mixer.music.play()
