from __future__ import annotations

import uuid
from typing import Any, Dict, List

import streamlit as st


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _get_groups(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    cfg.setdefault("signal_groups", [])
    return cfg["signal_groups"]


def render_designer(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mutates cfg in-memory via Streamlit widgets and returns it.
    Saving to disk is handled by caller.
    """
    st.header("Signal Designer")
    st.caption("Edit Signal Groups and Signals. IDs stay stable to preserve history.")

    groups = _get_groups(cfg)

    # --- Add new group
    with st.expander("Add Signal Group", expanded=False):
        col1, col2 = st.columns([3, 1])
        new_name = col1.text_input("Group name", placeholder="e.g., GYM, Spending, Diet", key="ds_new_group_name")
        if col2.button("Add group", type="primary"):
            name = new_name.strip()
            if not name:
                st.warning("Group name cannot be empty.")
            else:
                groups.append({
                    "id": _new_uuid(),
                    "name": name,
                    "active": True,
                    "signals": [],
                })
                st.success(f"Added group: {name}")
                st.rerun()

    if not groups:
        st.info("No groups yet. Add one above.")
        return cfg

    # --- Select group to edit
    active_labels = [f"{g.get('name','(unnamed)')}  ({'active' if g.get('active', True) else 'inactive'})" for g in groups]
    idx = st.selectbox("Select group to edit", range(len(groups)), format_func=lambda i: active_labels[i])
    group = groups[idx]

    st.subheader("Group settings")
    c1, c2, c3 = st.columns([3, 1, 1])
    group["name"] = c1.text_input("Group name", value=group.get("name", ""), key=f"ds_group_name_{group['id']}")
    group["active"] = c2.checkbox("Active", value=bool(group.get("active", True)), key=f"ds_group_active_{group['id']}")

    if c3.button("Disable group", help="Soft delete (keeps history)."):
        group["active"] = False
        st.warning("Group disabled (soft delete).")
        st.rerun()

    # --- Signals list
    group.setdefault("signals", [])
    signals: List[Dict[str, Any]] = group["signals"]

    st.divider()
    st.subheader("Signals in this group")

    # Add signal
    with st.expander("Add Signal", expanded=True):
        colA, colB = st.columns([3, 2])
        label = colA.text_input("Signal label", placeholder="e.g., Cardio duration", key=f"ds_new_signal_label_{group['id']}")
        qtype = colB.selectbox(
            "Type",
            ["quantity", "yesno", "time", "hours", "number", "text"],
            key=f"ds_new_signal_type_{group['id']}",
        )
        unit = ""
        if qtype in ("quantity", "hours", "number"):
            unit = st.text_input("Unit (optional)", placeholder="e.g., kg, min, CAD, hrs", key=f"ds_new_signal_unit_{group['id']}")
        req = st.checkbox("Required", value=False, key=f"ds_new_signal_required_{group['id']}")

        if st.button("Add signal", type="primary", key=f"ds_add_signal_btn_{group['id']}"):
            clean = label.strip()
            if not clean:
                st.warning("Signal label cannot be empty.")
            else:
                signals.append({
                    "id": _new_uuid(),
                    "label": clean,
                    "type": qtype,
                    "unit": unit.strip() if unit else None,
                    "required": bool(req),
                    "default": None,
                    "active": True,
                })
                st.success(f"Added signal: {clean}")
                st.rerun()

    if not signals:
        st.info("No signals yet in this group.")
        return cfg

    # Edit signals
    for i, s in enumerate(signals):
        with st.container(border=True):
            top = st.columns([3, 2, 1, 1])
            s["label"] = top[0].text_input("Label", value=s.get("label", ""), key=f"ds_sig_label_{s['id']}")
            s["type"] = top[1].selectbox(
                "Type",
                ["quantity", "yesno", "time", "hours", "number", "text"],
                index=["quantity", "yesno", "time", "hours", "number", "text"].index(s.get("type", "text")),
                key=f"ds_sig_type_{s['id']}",
            )
            s["active"] = top[2].checkbox("Active", value=bool(s.get("active", True)), key=f"ds_sig_active_{s['id']}")
            if top[3].button("Disable", key=f"ds_sig_disable_{s['id']}"):
                s["active"] = False
                st.warning("Signal disabled (soft delete).")
                st.rerun()

            # unit + required (only show unit when it makes sense)
            col1, col2 = st.columns([2, 2])
            if s["type"] in ("quantity", "hours", "number"):
                s["unit"] = col1.text_input("Unit", value=(s.get("unit") or ""), key=f"ds_sig_unit_{s['id']}") or None
            else:
                s["unit"] = None
                col1.caption("Unit: (not applicable for this type)")
            s["required"] = col2.checkbox("Required", value=bool(s.get("required", False)), key=f"ds_sig_req_{s['id']}")

            st.caption(f"signal_id: {s['id']}")

    return cfg
