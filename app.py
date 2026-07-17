import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from core import BioShieldEngine, DecisionEngine

# Konfigurace stránky
st.set_page_config(page_title="Bio-Ambient Shield Pro", layout="wide")

# Inicializace stavu aplikace (perzistence dat)
if 'engine' not in st.session_state:
    st.session_state.engine = BioShieldEngine()
    st.session_state.decision = DecisionEngine()
    # Inicializace historie
    st.session_state.history = pd.DataFrame(columns=["Čas", "Stav", "Dech (BPM)"])

# Simulace zpracování dat (zde bude později napojení na radar)
data = np.sin(np.linspace(0, 10, 128)) + np.random.normal(0, 0.1, 128)
freqs, mags = st.session_state.engine.process(data)
vitals = st.session_state.engine.extract(freqs, mags)
status = st.session_state.decision.update(vitals)

# Logování událostí do historie
if status != "STABLE":
    new_entry = {"Čas": datetime.now().strftime("%H:%M:%S"), "Stav": status, "Dech (BPM)": f"{vitals['resp']:.1f}"}
    st.session_state.history = pd.concat([pd.DataFrame([new_entry]), st.session_state.history]).head(10)

# UI Layout
st.title("🛡️ Bio-Ambient Shield: Health Monitor")

col1, col2 = st.columns([3, 1])
with col1:
    st.line_chart(data)
with col2:
    st.metric("Dech", f"{vitals['resp']:.1f} BPM")
    st.metric("Stav", status)

# Zobrazení historie (profesionální přehled)
st.subheader("Historie kritických událostí")
st.table(st.session_state.history)
