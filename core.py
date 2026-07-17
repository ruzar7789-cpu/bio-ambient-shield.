import numpy as np

class BioShieldEngine:
    def __init__(self, sampling_rate=20):
        self.sr = sampling_rate

    def process(self, raw_data):
        # Pokud jsou data samá nula, vrátíme nuly
        if np.all(raw_data == 0):
            return np.array([0]), np.array([0])
            
        clean_data = raw_data - np.mean(raw_data)
        windowed = clean_data * np.hamming(len(clean_data))
        fft = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(clean_data), 1/self.sr)
        return freqs, fft

    def extract(self, freqs, fft):
        # Bezpečnostní pojistka: pokud je max FFT příliš malé, dech je 0
        if len(fft) == 0 or np.max(fft) < 0.1:
            return {"resp": 0}
            
        r_band = (freqs >= 0.1) & (freqs <= 0.8)
        if any(r_band) and np.max(fft[r_band]) > 0.1:
            resp = freqs[r_band][np.argmax(fft[r_band])] * 60
        else:
            resp = 0
        return {"resp": resp}

class DecisionEngine:
    def __init__(self):
        self.threshold = 10 

    def update(self, vitals):
        # Pokud je resp 0, je to CRITICAL
        if vitals['resp'] < self.threshold:
            return "CRITICAL"
        return "STABLE"
        
