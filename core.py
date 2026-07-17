import numpy as np

class BioShieldEngine:
    def __init__(self, sampling_rate=20):
        self.sampling_rate = sampling_rate
        self.window_size = 128

    def process_signal(self, raw_data):
        windowed_data = raw_data * np.hamming(len(raw_data))
        fft_result = np.fft.rfft(windowed_data)
        frequencies = np.fft.rfftfreq(len(raw_data), 1/self.sampling_rate)
        return frequencies, np.abs(fft_result)

    def extract_vitals(self, frequencies, magnitude):
        resp_band = (frequencies > 0.3) & (frequencies < 0.8)
        heart_band = (frequencies > 1.0) & (frequencies < 2.0)
        resp_bpm = frequencies[resp_band][np.argmax(magnitude[resp_band])] * 60 if any(resp_band) else 0
        heart_bpm = frequencies[heart_band][np.argmax(magnitude[heart_band])] * 60 if any(heart_band) else 0
        return {"respiratory_bpm": resp_bpm, "heart_rate_bpm": heart_bpm}

class DecisionEngine:
    def __init__(self):
        self.state = "STABLE"
        self.alarm_counter = 0
        self.THRESHOLD = 3 

    def evaluate_state(self, vitals):
        if vitals['respiratory_bpm'] < 5:
            self.alarm_counter += 1
            if self.alarm_counter >= self.THRESHOLD:
                self.state = "CRITICAL_ALARM"
                return "🚨 ALARM: Ztráta dechu detekována!"
            return f"⚠️ Varování: Nízká aktivita"
        self.alarm_counter = 0
        return "✅ Systém v pořádku"
