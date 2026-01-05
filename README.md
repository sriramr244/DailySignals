# DailySignals

**DailySignals** is a config-driven daily KPI tracking app built with **Python + Streamlit**, using **Excel as the source of truth**.

You define *what to track* once, then log **one value per signal per day**. The system favors consistency, transparency, and long-term review over gamification.

---

## Core Concepts
- **Signal**: a single metric (sleep hours, calories, gym minutes, spend, etc.)
- **Signal Group**: a category of signals (Gym, Diet, Spending, Work)
- **Rule**: one reading per `(date, signal)` — saving again updates the value

---

## Features
- UI-based signal configuration (no manual JSON edits)
- Daily data entry with date selection
- Excel-backed storage (audit-friendly)
- Stable signal IDs (config changes never break history)
- Soft deletes for signals and groups

---

## Data Storage
- File: `data/dailysignals.xlsx`
- Sheet: `signal_readings`
- Long-format rows (append + upsert)

Each row represents one signal reading for one day.
