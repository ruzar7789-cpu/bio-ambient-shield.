import streamlit as st
import numpy as np
from core import BioShieldEngine, DecisionEngine

st.set_page_config(page_title="Bio-Ambient Shield Pro", layout="wide")

# CSS pro profesionální vzhled
st.markdown("""<style>
    .stApp { background-color: #0e1117; color: white; }
    .css-1r6slp0 { background-color: #1e1e1e; }
</style>""", unsafe_allow_html=True)

engine = BioShieldEngine()
decision = DecisionEngine()

st.title("🛡️ Bio-Ambient Shield: Monitoring Center")

# Simulace senzoru (nahradíme daty z radaru)
data = np.random.normal(0, 0.1, 128) + np.sin(np.linspace(0, 10, 128))
freqs, mags = engine.process_signal(data)
vitals = engine.extract_vitals(freqs, mags)
status = decision.evaluate(vitals)

# Dashboard Layout
col1, col2 = st.columns([3, 1])
with col1:
    st.line_chart(data)
with col2:
    st.metric("Dech", f"{vitals['resp']:.0f} BPM")
    st.metric("Tep", f"{vitals['heart']:.0f} BPM")

# Alarmová logika
if status == "CRITICAL_ALARM":
    st.error("!!! KRITICKÝ STAV - ZTRÁTA DECHU !!!")
elif status == "WARNING":
    st.warning("Detekována nepravidelnost...")
else:
    st.success("Systém monitoruje v normě.")
