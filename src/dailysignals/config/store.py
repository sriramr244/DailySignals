from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Loads config.json. If missing, creates a minimal default config.
    """
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))

    cfg: Dict[str, Any] = {
        "app": "DailySignals",
        "version": "1.0",
        "signal_groups": [],
    }
    save_config(config_path, cfg)
    return cfg


def save_config(config_path: Path, cfg: Dict[str, Any]) -> None:
    """
    Saves config.json (pretty printed).
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
