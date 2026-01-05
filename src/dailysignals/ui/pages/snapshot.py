from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

import streamlit as st


def _key(date_str: str, group_id: str, signal_id: str) -> str:
    return f"ds_snap__{date_str}__{group_id}__{signal_id}"


def render_snapshot(cfg: Dict[str, Any]) -> Dict[str, Any]:
    st.header("Daily Snapshot")

    picked_date = st.date_input("Date", value=date.today())
    date_str = picked_date.isoformat()

    rows: List[Dict[str, Any]] = []
    groups = cfg.get("signal_groups", [])

    if not groups:
        st.info("No Signal Groups yet. Go to Signal Designer and add groups/signals.")
        return {"date": date_str, "rows": rows}

    for g in groups:
        if not g.get("active", True):
            continue

        group_id = g.get("id", "")
        group_name = g.get("name", "(unnamed)")
        signals = g.get("signals", [])

        st.subheader(group_name)

        for s in signals:
            if not s.get("active", True):
                continue

            signal_id = s.get("id", "")
            label = s.get("label", "(unnamed)")
            qtype = s.get("type", "text")
            unit = s.get("unit") or ""

            widget_key = _key(date_str, group_id, signal_id)

            value: Any
            if qtype == "yesno":
                value = st.checkbox(label, key=widget_key)
            elif qtype == "time":
                value = st.time_input(label, key=widget_key)
            elif qtype in ("quantity", "number", "hours"):
                help_txt = f"Unit: {unit}" if unit else None
                value = st.number_input(label, key=widget_key, help=help_txt)
            else:
                value = st.text_input(label, key=widget_key)

            # Store as string to keep Excel simple
            if value is None:
                value_str = ""
            elif qtype == "time":
                value_str = value.strftime("%H:%M:%S")
            elif qtype == "yesno":
                value_str = "true" if value else "false"
            else:
                value_str = str(value)

            rows.append({
                "date": date_str,
                "group_id": group_id,
                "group_name": group_name,
                "signal_id": signal_id,
                "signal_label": label,
                "type": qtype,
                "value": value_str,
                "unit": unit,
                "source": "ui",
            })

    return {"date": date_str, "rows": rows}
