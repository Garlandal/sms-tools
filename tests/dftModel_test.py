import numpy as np
from scipy.signal import get_window

from smst.models import dft

def test_simple_sinusoid():
    window_size = 1024
    t = np.linspace(0, 1, window_size)
    x = np.cos(4 * 2 * np.pi * t)
    window = get_window('hamming', window_size)
    mag_spectrum, phase_spectrum = dft.fromAudio(x, window, window_size)
    x_reconstructed = dft.toAudio(mag_spectrum, phase_spectrum, window_size) * sum(window)


    assert mag_spectrum.argmax() == 4
    assert round(mag_spectrum.max()) == -6
    assert round(mag_spectrum.mean()) == -147
    assert np.allclose(x_reconstructed, x * window)
