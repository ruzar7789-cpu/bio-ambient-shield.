import numpy as np

class BioShieldEngine:
    """Robustní DSP jádro pro analýzu vitálních funkcí."""
    def __init__(self, sampling_rate=20):
        self.sr = sampling_rate

    def process(self, raw_data):
        # Detrendování a okno
        clean_data = raw_data - np.mean(raw_data)
        windowed = clean_data * np.hamming(len(clean_data))
        # FFT analýza
        fft = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(clean_data), 1/self.sr)
        return freqs, fft

    def extract(self, freqs, fft):
        # Definice dechového pásma 0.1 - 0.8 Hz
        r_band = (freqs >= 0.1) & (freqs <= 0.8)
        
        # Pokud je maximální amplituda v pásmu příliš nízká, vracíme 0 (apnoe)
        if any(r_band) and np.max(fft[r_band]) > 0.05:
            resp = freqs[r_band][np.argmax(fft[r_band])] * 60
        else:
            resp = 0
            
        return {"resp": resp}

class DecisionEngine:
    """Stavový automat pro detekci kritických událostí."""
    def __init__(self):
        self.threshold = 10 

    def update(self, vitals):
        if vitals['resp'] < self.threshold:
            return "CRITICAL"
        return "STABLE"
