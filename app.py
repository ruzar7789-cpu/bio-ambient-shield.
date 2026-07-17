import streamlit as st
import numpy as np
import pandas as pd
import time
from core import BioShieldEngine

st.set_page_config(page_title="Bio-Ambient Shield", layout="wide")

st.title("🛡️ Bio-Ambient Shield: Real-Time Monitor")

# Inicializace
engine = BioShieldEngine()
if 'data' not in st.session_state:
    st.session_state.data = []

# Layout dashboardu
col1, col2 = st.columns([2, 1])

with col1:
    chart = st.empty() # Místo pro graf

with col2:
    status_box = st.empty() # Místo pro status

# Simulace živých dat
for i in range(100):
    # Generování simulovaného signálu
    t = np.linspace(0, 6.4, 128)
    mock_data = np.sin(2 * np.pi * 0.5 * t) + np.random.normal(0, 0.1, 128)
    
    # Analýza
    freqs, mags = engine.process_signal(mock_data)
    vitals = engine.extract_vitals(freqs, mags)
    
    # Aktualizace dashboardu
    chart.line_chart(mock_data)
    
    status_box.metric("Dechová frekvence", f"{vitals['respiratory_bpm']:.1f} BPM")
    status_box.metric("Stav systému", "✅ Monitoruji")
    
    time.sleep(0.5)
