#!/bin/python
import struct
import os
import errno
import matplotlib.pyplot as plt
import numpy as np


FIFO = '/tmp/mpd.fifo'

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

while True:
    print("Opening FIFO...")
    #black pipe/fifo magic
    left_channel = []#np.empty(1, dtype=np.int16) #initialize empty numpyarray to append later
    right_channel = []#np.empty(1, dtype =np.int16) #initialize empty numpyarray to append later
    #plt.ion()
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #freq = np.linspace(0,44100)
    #sp = np.zeros(44100)
    #spectrum, = plt.plot(freq, sp)
    with open(FIFO, 'rb') as fifo:  #read as raw bytes('rb')
        print("FIFO opened")
        time_step = None
        while True:
            chunk = fifo.read(4)
            #tuple with 2 signed shorts
            # 1 for left channel 1 for right
            # its left right alternating
            #print(struct.unpack( "<hh", chunk)) #h stands for short
            chunk_tuple = struct.unpack( "<hh", chunk) #h stands for short
            left_channel.append(chunk_tuple[0])
            right_channel.append(chunk_tuple[1])

            plt.ion() #activates interactive mode (non-blocking?)

            if len(left_channel) == 2048*2:
                #FFT_Magic
                #data = np.random.rand(301) - 0.5
                data = np.array(left_channel)
                left_channel =[]
                ps = 2*np.log(np.abs(np.fft.rfft(data)))

                if time_step == None:
                    time_step = 1 / (44100)
                    freqs = np.fft.rfftfreq(data.size, time_step)
                    idx = np.argsort(freqs)
                    fig = plt.figure()
                    plt.ylim(0,50)
                    ax = fig.add_subplot(111)
                    line1, =ax.plot(freqs[idx], ps[idx], 'r-')
                    #line1, =ax.plot(freqs[idx][:512], ps[idx][:512], 'r-') # 512 is used to truncate the higher frequencies

                line1.set_ydata(ps[idx])
                #line1.set_ydata(ps[idx][:512])
                fig.canvas.draw()
                fig.canvas.flush_events()
                #plt.show()





#
#x = np.linspace(0, 6*np.pi, 100)
#y = np.sin(x)
#
## You probably won't need this if you're embedding things in a tkinter plot...
#plt.ion()
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma
#
#for phase in np.linspace(0, 10*np.pi, 500):
#
