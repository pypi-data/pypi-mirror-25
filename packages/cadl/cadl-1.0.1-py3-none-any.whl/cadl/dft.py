"""Utils for performing a DFT using numpy.
"""
"""
Copyright 2017 Parag K. Mital.  See also NOTICE.md.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import numpy as np
from scipy.signal import hann


def ztoc(re, im):
    """Summary

    Parameters
    ----------
    re : TYPE
        Description
    im : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    return np.sqrt(re**2 + im**2), np.angle(re + im * 1j)


def ctoz(mag, phs):
    """Summary

    Parameters
    ----------
    mag : TYPE
        Description
    phs : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    return mag * np.cos(phs), mag * np.sin(phs)


def dft_np(signal, hop_size=256, fft_size=512):
    """Summary

    Parameters
    ----------
    signal : TYPE
        Description
    hop_size : int, optional
        Description
    fft_size : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    n_hops = len(signal) // hop_size
    s = []
    hann_win = hann(fft_size)
    for hop_i in range(n_hops):
        frame = signal[(hop_i * hop_size):(hop_i * hop_size + fft_size)]
        frame = np.pad(frame, (0, fft_size - len(frame)), 'constant')
        frame *= hann_win
        s.append(frame)
    s = np.array(s)
    N = s.shape[-1]
    k = np.reshape(np.linspace(0.0, 2 * np.pi / N * (N // 2), N // 2), [1, N // 2])
    x = np.reshape(np.linspace(0.0, N - 1, N), [N, 1])
    freqs = np.dot(x, k)
    reals = np.dot(s, np.cos(freqs)) * (2.0 / N)
    imags = np.dot(s, np.sin(freqs)) * (2.0 / N)
    return reals, imags


def idft_np(re, im, hop_size=256, fft_size=512):
    """Summary

    Parameters
    ----------
    re : TYPE
        Description
    im : TYPE
        Description
    hop_size : int, optional
        Description
    fft_size : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    N = re.shape[1] * 2
    k = np.reshape(np.linspace(0.0, 2 * np.pi / N * (N // 2), N // 2), [N // 2, 1])
    x = np.reshape(np.linspace(0.0, N - 1, N), [1, N])
    freqs = np.dot(k, x)
    signal = np.zeros((re.shape[0] * hop_size + fft_size,))
    recon = np.dot(re, np.cos(freqs)) + np.dot(im, np.sin(freqs))
    for hop_i, frame in enumerate(recon):
        signal[(hop_i * hop_size): (hop_i * hop_size + fft_size)] += frame
    return signal
