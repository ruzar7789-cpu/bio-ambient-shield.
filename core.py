import numpy as np

class BioShieldEngine:
    """Robustní DSP jádro pro analýzu vitálních funkcí."""
    def __init__(self, sampling_rate=20):
        self.sr = sampling_rate

    def process(self, raw_data):
        # Detrendování signálu (odstranění DC posunu)
        clean_data = raw_data - np.mean(raw_data)
        # Hammingovo okno pro potlačení bočních laloků
        windowed = clean_data * np.hamming(len(clean_data))
        # Rychlá Fourierova transformace
        fft = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(clean_data), 1/self.sr)
        return freqs, fft

    def extract(self, freqs, fft):
        # Definice frekvenčních pásem
        r_band = (freqs >= 0.1) & (freqs <= 0.8) # 0.1 - 0.8 Hz (dechová frekvence)
        
        # Pokud je signál v pásmu příliš slabý, vracíme 0
        if any(r_band) and np.max(fft[r_band]) > 0.01:
            resp = freqs[r_band][np.argmax(fft[r_band])] * 60
        else:
            resp = 0
            
        return {"resp": resp}

class DecisionEngine:
    """Stavový automat s historií pro detekci kritických událostí."""
    def __init__(self):
        self.history = []
        # Práh pro detekci apnoe (dech pod 10 BPM je považován za kritický)
        self.threshold = 10 

    def update(self, vitals):
        # Pokud je dech pod prahem, je to kritické
        if vitals['resp'] < self.threshold:
            return "CRITICAL"
        return "STABLE"
        
