"""
This is just code off the internet intended to be modified and used to learn
how this project can be done.
"""

from pylab import *
from scipy.io import wavfile

sampFreq, snd = wavfile.read('440_sine.wav')

snd = snd / (2.**15)

s1 = snd[:, 0]

# creates an array containing the time points
timeArray = arange(0, 5292, 1)
timeArray = timeArray / sampFreq
timeArray = timeArray * 1000  #scale to milliseconds
n =  len(s1)
p = fft(s1) # this takes the fourier tranform

nUniquePts = int(ceil((n+1)/2.0))
p = p[0:nUniquePts]
p = abs(p)

# scale by the number of points so that
# the magnitude does not depend on the length
# of the signal or on its sampling frequency
p = p / float(n)

# square it to get the power
# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
p = p**2

# we've got odd number of points fft
if n % 2 > 0:
    p[1:len(p)] = p[1:len(p)] * 2
else:
    # we've got even number of points fft
    p[1:len(p) -1] = p[1:len(p) - 1] * 2

freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n);
plot(freqArray/1000, 10*log10(p), color='k')
xlabel('Frequency (kHz)')
ylabel('Power (dB)')

show()
