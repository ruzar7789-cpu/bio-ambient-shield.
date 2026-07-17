import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from core import BioShieldEngine, DecisionEngine, RadarInterface

st.set_page_config(page_title="Bio-Ambient Shield Pro", layout="wide")

# Inicializace stavu a spuštění radaru na pozadí
if 'engine' not in st.session_state:
    st.session_state.engine = BioShieldEngine()
    st.session_state.decision = DecisionEngine()
    
    # Příprava na fyzický hardware
    st.session_state.radar = RadarInterface()
    st.session_state.radar.start()
    
    st.session_state.history = pd.DataFrame(columns=["Čas", "Stav", "Dech (BPM)"])

st.title("🛡️ Bio-Ambient Shield: Health Monitor")

st.sidebar.header("Testovací centrum")
force_alarm = st.sidebar.checkbox("Simulovat kritický stav (Apnoe)")

if force_alarm:
    data = np.zeros(128) 
else:
    # --- PŘÍPRAVA NA HARDWARE ---
    # Až připojíme hardware, smažeme simulaci a odkomentujeme řádek níže:
    # data = st.session_state.radar.get_data()
    
    data = np.sin(np.linspace(0, 10, 128)) + np.random.normal(0, 0.1, 128)

freqs, mags = st.session_state.engine.process(data)
vitals = st.session_state.engine.extract(freqs, mags)
status = st.session_state.decision.update(vitals)

# Logování historie
if status == "CRITICAL":
    now = datetime.now().strftime("%H:%M:%S")
    if st.session_state.history.empty or st.session_state.history.iloc[0]["Stav"] != "!!! ALARM !!!":
        new_entry = {"Čas": now, "Stav": "!!! ALARM !!!", "Dech (BPM)": f"{vitals['resp']:.1f}"}
        st.session_state.history = pd.concat([pd.DataFrame([new_entry]), st.session_state.history]).head(10)

col1, col2 = st.columns([3, 1])
with col1:
    st.line_chart(data)
with col2:
    st.metric("Dech", f"{vitals['resp']:.1f} BPM")
    st.metric("Stav", status)

st.subheader("Historie kritických událostí")
st.table(st.session_state.history)
