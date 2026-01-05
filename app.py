import streamlit as st

from src.dailysignals.config.store import load_config, save_config
from src.dailysignals.paths import CONFIG_PATH, EXCEL_PATH
from src.dailysignals.storage.excel_store import upsert_readings, ensure_workbook
from src.dailysignals.ui.pages.designer import render_designer
from src.dailysignals.ui.pages.snapshot import render_snapshot


st.set_page_config(page_title="DailySignals", layout="wide")
st.title("DailySignals")

# Load config into session state
if "cfg" not in st.session_state:
    st.session_state.cfg = load_config(CONFIG_PATH)

page = st.sidebar.radio("Navigation", ["Daily Snapshot", "Signal Designer"], index=0)

if page == "Signal Designer":
    updated = render_designer(st.session_state.cfg)
    st.divider()
    if st.button("Save config", type="primary"):
        save_config(CONFIG_PATH, updated)
        st.session_state.cfg = updated
        st.success("Saved config ✅")

    with st.expander("Preview config.json", expanded=False):
        st.json(updated)

else:
    # Daily Snapshot
    ensure_workbook(EXCEL_PATH)
    result = render_snapshot(st.session_state.cfg)
    rows = result["rows"]

    st.divider()
    col1, col2 = st.columns([1, 3])
    if col1.button("Save today's readings", type="primary"):
        result = upsert_readings(EXCEL_PATH, rows)
        st.success(f"Saved, Inserted: {result['inserted']} | Updated: {result['updated']}")

    with col2.expander("Preview rows to be saved", expanded=False):
        st.write(rows[:20])
        if len(rows) > 20:
            st.caption(f"Showing 20 of {len(rows)} rows.")
