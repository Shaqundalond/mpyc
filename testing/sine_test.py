#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile

sampleRate = 44100
frequency = 440
frequency2 = 880
duration = 30

t = np.linspace(0, duration, sampleRate * duration)  #  Produces a 5 second Audio-File
y = np.sin(frequency * 2 * np.pi * t)  * (1- t/duration) + np.sin(frequency2 * 2 * np.pi * t) * (t/duration)#  Has frequency of 440Hz

wavfile.write('Sine2.wav', sampleRate, y)
