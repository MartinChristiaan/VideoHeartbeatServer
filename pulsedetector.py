
from signalprocessor import extract_pulse_chrominance,extract_pulse_PBV
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

class PulseDetector():
    def __init__(self,fs,fftlength=300):
        self.chromBPM = 0
        self.chromSNR = 0
        
        self.PBVBPM = 0
        self.PBVSNR = 0
        
        
        self.f = np.linspace(0,fs/2,fftlength/2 + 1) * 60
        self.normalized_amplitude_chrom = np.zeros_like(self.f)
        self.normalized_amplitude_PBV = np.zeros_like(self.f)
        self.useChrom = True
        self.usePBV = True
    def detect_pulse(self,fs,rppg,fftlength = 300):
        if rppg.shape[1] > fftlength:
            self.f = np.linspace(0,fs/2,fftlength/2 + 1) * 60                    
            if self.useChrom:
                self.normalized_amplitude_chrom = extract_pulse_chrominance(fs,rppg)
                bpm_id = np.argmax(self.normalized_amplitude_chrom)
                self.chromBPM = self.f[bpm_id]
                self.chromSNR = calculateSNR(self.normalized_amplitude_chrom,bpm_id)
            if self.usePBV:
                self.normalized_amplitude_PBV = extract_pulse_PBV(fs,rppg)
                bpm_id = np.argmax(self.normalized_amplitude_PBV)
                self.PBVBPM = self.f[bpm_id]
                self.PBVSNR = calculateSNR(self.normalized_amplitude_PBV,bpm_id)
                  
            

