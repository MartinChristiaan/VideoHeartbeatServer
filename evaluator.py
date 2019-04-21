from signalprocessor import Proccessor
from TextWriter import write_text
import numpy as np

import scipy.stats as st
from numpy.linalg import norm

def dbv(x):
    return 20*np.log10(np.abs(x))

def calculateSNR(hwfft, f, nsig=1):
    hwfft = hwfft.squeeze()
    signalBins = np.arange(f - nsig + 1, f + nsig + 2, dtype='int64')
    signalBins = signalBins[signalBins > 0]
    signalBins = signalBins[signalBins <= max(hwfft.shape)]
    s = norm(hwfft[signalBins - 1]) # *4/(N*sqrt(3)) for true rms value;
    noiseBins = np.arange(1, max(hwfft.shape) + 1, dtype='int64')
    noiseBins = np.delete(noiseBins, noiseBins[signalBins - 1] - 1)
    n = norm(hwfft[noiseBins - 1])
    if n == 0:
        snr = np.Inf
    else:
        snr = dbv(s/n)
    return snr

class Evaluator():
    def __init__(self,processor:Proccessor):
        self.processor = processor
        self.write_on_frame = True
        self.f = np.linspace(0,processor.fs/2,processor.fftlength/2 + 1) * 60
        self.bpm = []
        self.snr = []
        self.curbpm = 0
        self.cursnr = 0
     
    def evaluate(self,frame):
        if self.processor.enough_samples:
            normalized_amplitude = self.processor.normalized_amplitude
            bpm_id = np.argmax(normalized_amplitude)
            self.bpm.append(self.f[bpm_id])

            
            if len(self.bpm) > 300:
                del self.bpm[0]
            self.snr.append(calculateSNR(normalized_amplitude,bpm_id))
            self.curbpm = self.f[bpm_id]
            self.cursnr = self.snr[-1]  

