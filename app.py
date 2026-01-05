import streamlit as st

from src.dailysignals.config.store import load_config
from src.dailysignals.paths import CONFIG_PATH


st.set_page_config(page_title="DailySignals", layout="wide")

st.title("DailySignals")

cfg = load_config(CONFIG_PATH)

with st.expander("Current config.json", expanded=True):
    st.json(cfg)
