import numpy as np
# matplotlib without any blocking GUI
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import hamming, hanning, triang, blackmanharris, resample
from scipy.fftpack import fft, ifft, fftshift
import math
import os, functools, time
from scipy.interpolate import interp1d



import smst.models.sineModel as SM
import smst.models.stft as STFT
import smst.models.sineModel as SM
import smst.utils as utils
import smst.transformations.sineTransformations as SMT


(fs, x) = utils.wavread('../../../sounds/mridangam.wav')
w = np.hamming(801)
N = 2048
t = -90
minSineDur = .005
maxnSines = 150
freqDevOffset = 20
freqDevSlope = 0.02
Ns = 512
H = Ns/4
mX, pX = STFT.stftAnal(x, w, N, H)
tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)
timeScale = np.array([.01, .0, .03, .03, .335, .4, .355, .42, .671, .8, .691, .82, .858, 1.2, .878, 1.22, 1.185, 1.6, 1.205, 1.62, 1.497, 2.0, 1.517, 2.02, 1.686, 2.4, 1.706, 2.42, 1.978, 2.8])
ytfreq, ytmag = SMT.sineTimeScaling(tfreq, tmag, timeScale)
y = SM.sineModelSynth(ytfreq, ytmag, np.array([]), Ns, H, fs)
mY, pY = STFT.stftAnal(y, w, N, H)

plt.figure(1, figsize=(12, 9))
maxplotfreq = 4000.0
plt.subplot(4,1,1)
plt.plot(np.arange(x.size)/float(fs), x, 'b')
plt.axis([0,x.size/float(fs),min(x),max(x)])
plt.title('x (mridangam.wav)')

plt.subplot(4,1,2)
numFrames = int(tfreq[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
tracks = tfreq*np.less(tfreq, maxplotfreq)
tracks[tracks<=0] = np.nan
plt.plot(frmTime, tracks, color='k', lw=1)
plt.autoscale(tight=True)
plt.title('mX + sine frequencies')

maxplotbin = int(N*maxplotfreq/fs)
numFrames = int(mX[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = np.arange(maxplotbin+1)*float(fs)/N
plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:maxplotbin+1]))
plt.autoscale(tight=True)

plt.subplot(4,1,3)
numFrames = int(ytfreq[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
tracks = ytfreq*np.less(ytfreq, maxplotfreq)
tracks[tracks<=0] = np.nan
plt.plot(frmTime, tracks, color='k', lw=1)
plt.autoscale(tight=True)
plt.title('mY + time-scaled sine frequencies')

maxplotbin = int(N*maxplotfreq/fs)
numFrames = int(mY[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = np.arange(maxplotbin+1)*float(fs)/N
plt.pcolormesh(frmTime, binFreq, np.transpose(mY[:,:maxplotbin+1]))
plt.autoscale(tight=True)

plt.subplot(4,1,4)
plt.plot(np.arange(y.size)/float(fs), y, 'b')
plt.axis([0,y.size/float(fs),min(y),max(y)])
plt.title('y')

plt.tight_layout()
utils.wavwrite(y, fs, 'mridangam-sineModelTimeScale.wav')
plt.savefig('sineModelTimeScale-mridangam.png')
