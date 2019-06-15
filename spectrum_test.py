#!/bin/python
import sys
import os
import errno

FIFO = '/tmp/mpd.fifo'

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

while True:
    print("Opening FIFO...")
    with open(FIFO, 'rb') as fifo:
        print("FIFO opened")
        useable_chunk = []
        useable_chunk2 = []
        while True:
            chunk = fifo.read(2)
            #if useable_chunk == None:
            #    useable_chunk = chunk
            #    print('Read: "{0}" \n'.format(int.from_bytes(useable_chunk,byteorder='little', signed=True)))

            #else:
            #    useable_chunk += chunk
            #if len(chunk) == 0:
            #    print("Writer closed")
            #    break
            #if len(useable_chunk) >= 2**16:
            #    data = useable_chunk[:2**16]
            #    useable_chunk = useable_chunk[2**16:]
            #    print('Read: "{0}" \n'.format(int.from_bytes(useable_chunk,byteorder='little', signed=True)))
            #print(len(chunk))
            if len(useable_chunk2) <6:
                #useable_chunk.append(int.from_bytes(chunk,byteorder='big'))
                useable_chunk2.append(int.from_bytes(chunk,byteorder='little', signed = True))
            else:
                #print("big\t",useable_chunk)
                #print("little\t", useable_chunk2)
                print(useable_chunk2)
                #useable_chunk = []
                useable_chunk2 = []
                #print(sys.byteorder)
            #print('Read: "{0}" \n'.format(int.from_bytes(chunk,byteorder='little', signed=True)))
