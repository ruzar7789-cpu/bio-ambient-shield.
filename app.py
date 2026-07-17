import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from core import BioShieldEngine, DecisionEngine

st.set_page_config(page_title="Bio-Ambient Shield Pro", layout="wide")

# Inicializace stavu
if 'engine' not in st.session_state:
    st.session_state.engine = BioShieldEngine()
    st.session_state.decision = DecisionEngine()
    st.session_state.history = pd.DataFrame(columns=["Čas", "Stav", "Dech (BPM)"])

st.title("🛡️ Bio-Ambient Shield: Health Monitor")

# Boční panel
st.sidebar.header("Testovací centrum")
force_alarm = st.sidebar.checkbox("Simulovat kritický stav (Apnoe)")

# Generování dat
if force_alarm:
    # VYNUCENÁ NULA pro testování alarmu
    data = np.zeros(128) 
else:
    # Simulace normálního dýchání
    data = np.sin(np.linspace(0, 10, 128)) + np.random.normal(0, 0.1, 128)

# Výpočty
freqs, mags = st.session_state.engine.process(data)
vitals = st.session_state.engine.extract(freqs, mags)
status = st.session_state.decision.update(vitals)

# Logování historie
if status == "CRITICAL":
    now = datetime.now().strftime("%H:%M:%S")
    new_entry = {"Čas": now, "Stav": "!!! ALARM !!!", "Dech (BPM)": f"{vitals['resp']:.1f}"}
    # Přidání, pokud záznam s tímto časem neexistuje
    if st.session_state.history.empty or st.session_state.history.iloc[0]["Čas"] != now:
        st.session_state.history = pd.concat([pd.DataFrame([new_entry]), st.session_state.history]).head(10)

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.line_chart(data)
with col2:
    st.metric("Dech", f"{vitals['resp']:.1f} BPM")
    st.metric("Stav", status)

st.subheader("Historie kritických událostí")
st.table(st.session_state.history)
