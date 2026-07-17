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
        fft = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(clean_data), 1/self.sr)
        return freqs, fft

    def extract(self, freqs, fft):
        # Definice frekvenčních pásem
        r_band = (freqs >= 0.2) & (freqs <= 0.8)
        h_band = (freqs >= 1.0) & (freqs <= 2.5)
        
        resp = freqs[r_band][np.argmax(fft[r_band])] * 60 if any(r_band) else 0
        heart = freqs[h_band][np.argmax(fft[h_band])] * 60 if any(h_band) else 0
        return {"resp": resp, "heart": heart}

class DecisionEngine:
    """Stavový automat s historií (logování alarmů)."""
    def __init__(self):
        self.history = []
        self.threshold = 5 

    def update(self, vitals):
        is_critical = vitals['resp'] < self.threshold
        state = "CRITICAL" if is_critical else "STABLE"
        self.history.append({"time": np.datetime64('now'), "state": state})
        return state
        
