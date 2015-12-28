import numpy as np
# matplotlib without any blocking GUI
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import hamming, triang, blackmanharris
import os, functools, time

from smst.models import sine
from smst.models import stft
import smst.utils as utils

plt.figure(1, figsize=(9, 7))

plt.subplot(211)
(fs, x) = utils.wavread('../../../sounds/vibraphone-C6.wav'))
w = np.blackman(401)
N = 512
H = 100
t = -100
minSineDur = .02
maxnSines = 150
freqDevOffset = 20
freqDevSlope = 0.01
mX, pX = stft.fromAudio(x, w, N, H)
tfreq, tmag, tphase = sine.fromAudio(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)

maxplotfreq = 10000.0
maxplotbin = int(N*maxplotfreq/fs)
numFrames = int(mX[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = np.arange(maxplotbin+1)*float(fs)/N
plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:maxplotbin+1]))
plt.autoscale(tight=True)

tracks = tfreq*np.less(tfreq, maxplotfreq)
tracks[tracks<=0] = np.nan
plt.plot(frmTime, tracks, color='k', lw=1.5)
plt.autoscale(tight=True)
plt.title('mX + sine frequencies (vibraphone-C6.wav)')

plt.subplot(212)
(fs, x) = utils.wavread('../../../sounds/vignesh.wav'))
w = np.blackman(1101)
N = 2048
H = 250
t = -90
minSineDur = .1
maxnSines = 200
freqDevOffset = 20
freqDevSlope = 0.02
mX, pX = stft.fromAudio(x, w, N, H)
tfreq, tmag, tphase = sine.fromAudio(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)

maxplotfreq = 5000.0
maxplotbin = int(N*maxplotfreq/fs)
numFrames = int(mX[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = np.arange(maxplotbin+1)*float(fs)/N
plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:maxplotbin+1]))
plt.autoscale(tight=True)

tracks = tfreq*np.less(tfreq, maxplotfreq)
tracks[tracks<=0] = np.nan
plt.plot(frmTime, tracks, color='k', lw=1.5)
plt.autoscale(tight=True)
plt.title('mX + sine frequencies (vignesh.wav)')

plt.tight_layout()
plt.savefig('harmonic-inharmonic-sines.png')
