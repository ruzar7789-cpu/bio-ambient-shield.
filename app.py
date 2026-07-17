import streamlit as st
import numpy as np
import time
from core import BioShieldEngine, DecisionEngine

st.set_page_config(page_title="Bio-Ambient Shield", layout="wide")

# Inicializace
engine = BioShieldEngine()
decision = DecisionEngine()

st.title("🛡️ Bio-Ambient Shield: Safety Monitor")

# Boční panel pro ovládání
st.sidebar.header("Systémová nastavení")
sim_alarm = st.sidebar.button("Testovat poplach")

# Simulace dat
t = np.linspace(0, 6.4, 128)
# Pokud stiskneme tlačítko, pošleme "nulová" data pro vyvolání alarmu
if sim_alarm:
    mock_data = np.zeros(128) 
else:
    mock_data = np.sin(2 * np.pi * 0.5 * t) + np.random.normal(0, 0.1, 128)

# Zpracování
freqs, mags = engine.process_signal(mock_data)
vitals = engine.extract_vitals(freqs, mags)
status_msg = decision.evaluate_state(vitals)

# Vizuální logika alarmu
if decision.state == "CRITICAL_ALARM":
    st.error(f"### {status_msg}")
    st.balloons() # Pro extra pozornost
else:
    st.success(status_msg)

# Zobrazení grafu
st.line_chart(mock_data)
    
