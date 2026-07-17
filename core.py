import numpy as np
import threading
import time
from collections import deque
import serial 

class RadarInterface:
    """Asynchronní čtení dat z radaru přes USB/UART."""
    def __init__(self, port='/dev/ttyUSB0', baudrate=921600, buffer_size=128):
        self.port = port
        self.baudrate = baudrate
        self.buffer = deque(maxlen=buffer_size)
        self.buffer.extend(np.zeros(buffer_size))
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._read_stream, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _read_stream(self):
        """Tato smyčka běží na pozadí a plní buffer daty z USB."""
        try:
            # PROZATÍMNÍ SIMULACE: Aby vlákno běželo a aplikace nespadla
            while self.running:
                time.sleep(0.05) 
        except Exception as e:
            print(f"Chyba připojení radaru: {e}")

    def get_data(self):
        return np.array(self.buffer)

class BioShieldEngine:
    """Robustní DSP jádro pro analýzu vitálních funkcí."""
    def __init__(self, sampling_rate=20):
        self.sr = sampling_rate

    def process(self, raw_data):
        if np.all(raw_data == 0):
            return np.array([0]), np.array([0])
            
        clean_data = raw_data - np.mean(raw_data)
        windowed = clean_data * np.hamming(len(clean_data))
        fft = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(clean_data), 1/self.sr)
        return freqs, fft

    def extract(self, freqs, fft):
        if len(fft) == 0 or np.max(fft) < 0.1:
            return {"resp": 0}
            
        r_band = (freqs >= 0.1) & (freqs <= 0.8)
        if any(r_band) and np.max(fft[r_band]) > 0.1:
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
        
