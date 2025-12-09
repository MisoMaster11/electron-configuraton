import json
from pathlib import Path

CONFIG_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "background_color": "#FFFDA4",
    "button_color": "#D7CA38",
    "entry_and_label_color": "#FFFEEA",
    "text_color": "#000000"
}

def load_settings():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    else:
        save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict):
    CONFIG_FILE.write_text(json.dumps(settings, indent=4))