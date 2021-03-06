# matplotlib without any blocking GUI
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from smst.utils import audio, peaks
from smst.models import dft

(fs, x) = audio.read_wav('../../../sounds/oboe-A4.wav')
N = 512 * 2
M = 511
t = -60
w = np.hamming(M)
start = .8 * fs
hN = N / 2
hM = (M + 1) / 2

x1 = x[start:start + M]
mX, pX = dft.from_audio(x1, w, N)
ploc = peaks.find_peaks(mX, t)
iploc, ipmag, ipphase = peaks.interpolate_peaks(mX, pX, ploc)
pmag = mX[ploc]
freqaxis = fs * np.arange(mX.size) / float(N)

plt.figure(1, figsize=(9, 5))
plt.plot(freqaxis, mX, 'r', lw=1.5)
plt.axis([0, 7000, -80, max(mX) + 1])
plt.plot(fs * iploc / N, ipmag, marker='x', color='b', linestyle='', markeredgewidth=1.5)
harms = np.arange(1, 20) * 440.0
plt.vlines(harms, -80, max(mX) + 1, color='g', lw=1.5)
plt.title('mX + peaks + f0 multiples (oboe-A4.wav)')

plt.tight_layout()
plt.savefig('spectral-peaks-and-f0.png')
