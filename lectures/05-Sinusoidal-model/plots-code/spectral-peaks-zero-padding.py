# matplotlib without any blocking GUI
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft
from scipy.signal import hamming, triang, blackmanharris

from smst.utils import audio, peaks
from smst.models import dft

(fs, x) = audio.wavread('../../../sounds/oboe-A4.wav')
N = 512*2
M = 511
t = -60
w = np.hamming(M)
start = .8*fs
hN = N/2
hM = (M+1)/2

x1 = x[start:start+M]
mX, pX = dft.fromAudio(x1, w, N)
ploc = peaks.peakDetection(mX, t)
pmag = mX[ploc]
freqaxis = fs*np.arange(mX.size)/float(N)

plt.figure(1, figsize=(9.5, 5.5))
plt.subplot (2,1,1)
plt.plot(freqaxis,mX,'r', lw=1.5)
plt.axis([300,2500,-70,max(mX)])
plt.plot(fs * ploc / N, pmag, marker='x', color='b', linestyle='', markeredgewidth=1.5)
plt.title('mX + spectral peaks (oboe-A4.wav), zero padding = 2')

plt.subplot (2,1,2)
plt.plot(freqaxis,pX,'c', lw=1.5)
plt.axis([300,2500,min(pX),-1])
plt.plot(fs * ploc / N, pX[ploc], marker='x', color='b', linestyle='', markeredgewidth=1.5)
plt.title('pX + spectral peaks (oboe-A4.wav), zero padding = 2')

plt.tight_layout()
plt.savefig('spectral-peaks-zero-padding.png')
