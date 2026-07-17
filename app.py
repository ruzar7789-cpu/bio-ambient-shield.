import streamlit as st
import numpy as np
from core import BioShieldEngine, DecisionEngine
import pandas as pd

st.set_page_config(page_title="Bio-Ambient Shield", layout="wide")

# Backend inicializace
if 'engine' not in st.session_state:
    st.session_state.engine = BioShieldEngine()
    st.session_state.decision = DecisionEngine()

st.title("🛡️ Bio-Ambient Shield: Enterprise Monitor")

# Simulace dat (v budoucnu nahradíme vstupem ze senzoru)
data = np.sin(np.linspace(0, 10, 128)) + np.random.normal(0, 0.1, 128)
f, m = st.session_state.engine.process(data)
v = st.session_state.engine.extract(f, m)
state = st.session_state.decision.update(v)

# Vizualizace
col1, col2 = st.columns([2, 1])
with col1:
    st.line_chart(data)
with col2:
    st.metric("Dechová frekvence", f"{v['resp']:.1f} BPM")
    st.metric("Srdeční tep", f"{v['heart']:.1f} BPM")
    st.status(state)

# Historický log
st.subheader("Event Log")
st.table(pd.DataFrame(st.session_state.decision.history[-5:]))
