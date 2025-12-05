# app/config.py

from pathlib import Path
import json

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # app/.. = project root
CONFIG_PATH = BASE_DIR / "config.json"

with CONFIG_PATH.open("r", encoding="utf-8") as f:
    config = json.load(f)

TEST_CSV = BASE_DIR / config["TEST_CSV"]
USER_LINKS_CSV = BASE_DIR / config["USER_LINKS_CSV"]