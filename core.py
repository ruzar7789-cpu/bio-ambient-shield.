import numpy as np

class BioShieldEngine:
    def __init__(self, sampling_rate=20):
        self.sampling_rate = sampling_rate

    def process_signal(self, raw_data):
        # Aplikace Hammingova okna pro eliminaci okrajových artefaktů
        windowed = raw_data * np.hamming(len(raw_data))
        fft = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(len(raw_data), 1/self.sampling_rate)
        return freqs, np.abs(fft)

    def extract_vitals(self, freqs, mag):
        # Detekce dominantní frekvence v pásmech
        resp_mask = (freqs >= 0.2) & (freqs <= 0.8)
        heart_mask = (freqs >= 1.0) & (freqs <= 2.5)
        
        resp_bpm = freqs[resp_mask][np.argmax(mag[resp_mask])] * 60 if any(resp_mask) else 0
        heart_bpm = freqs[heart_mask][np.argmax(mag[heart_mask])] * 60 if any(heart_mask) else 0
        
        return {"resp": resp_bpm, "heart": heart_bpm}

class DecisionEngine:
    def __init__(self):
        self.state = "STABLE"
        self.counter = 0
        self.LIMIT = 5 # Vyšší práh pro vyšší spolehlivost

    def evaluate(self, vitals):
        # Pokud je dech pod 5 BPM po dobu 5 cyklů -> ALARM
        if vitals['resp'] < 5:
            self.counter += 1
            if self.counter >= self.LIMIT:
                self.state = "CRITICAL"
                return "CRITICAL_ALARM"
            return "WARNING"
        
        self.counter = 0
        self.state = "STABLE"
        return "OK"
        
