SHEET_READINGS = "signal_readings"

READING_COLUMNS = [
    "date",          # YYYY-MM-DD
    "group_id",
    "group_name",
    "signal_id",
    "signal_label",
    "type",          # quantity/yesno/time/hours/number/text
    "value",         # stored as string (Excel-safe)
    "unit",
    "source",        # ui | excel_upload
    "created_at",    # ISO timestamp
]
