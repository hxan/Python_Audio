import pyaudio
import wave
import tkinter as tk
import tkinter.font as tf
import time
import threading
from socket import *
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
is_start = False

s = socket(AF_INET,SOCK_DGRAM)

def SendFile():
	
	print("sending")

	buf =1024
	addr = ('192.168.2.209',5099)

	f=open('output.wav',"rb") 


	data = f.read(buf)
	s.sendto(data,addr)
	while (data):
		data = f.read(buf)
		s.sendto(data,addr)
		time.sleep(0.0001)
	f.close()
	print("sending done")

def Record():
	global is_start
	while(True):

		if(is_start == False):
			time.sleep(0.01)
			continue;

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK)

		print("* recording")

		frames = []
		while(is_start):
		    data = stream.read(CHUNK)
		    frames.append(data)

		print("* done recording")

		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		SendFile()

def StartRecord():
	global is_start
	global sending_status
	is_start = True
	sending_status.set("recording")

def StopRecord():
	global is_start
	global sending_status
	is_start = False 
	sending_status.set("none")

windows = tk.Tk()
windows.geometry('300x250')
windows.title('Record')
windows.resizable(0,0)
windows.attributes("-alpha",0.95)

c = threading.Thread(target=Record)
c.setDaemon(True)
c.start()

Button1 = tk.Button(windows,text='开启',bg='#56BD50', fg='#FFFFFF',command=StartRecord,font=tf.Font(size=12,family='Microsoft YaHei'),relief=tk.FLAT)
Button1.place(height = 26,width = 199,x = 50,y = 48)

Button2 = tk.Button(windows,text='停止',bg='#56BD50', fg='#FFFFFF',command=StopRecord,font=tf.Font(size=12,family='Microsoft YaHei'),relief=tk.FLAT)
Button2.place(height = 26,width = 199,x = 50,y = 104)

sending_status = tk.StringVar()	
sending_status.set("none")
Label5 = tk.Label(windows,textvariable=sending_status,bg='#56BD50', fg='#FFFFFF',font=tf.Font(size=12,family='Microsoft YaHei'),relief=tk.FLAT)
Label5.place(height = 26,width = 199,x = 50,y = 160)

windows.mainloop()
