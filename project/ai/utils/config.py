import json
from pathlib import Path
from typing import Any

from django.conf import settings


def load_preprocessing_config(path: Path | None = None) -> dict[str, Any]:
    p = path or settings.AI_PREPROCESSING_CONFIG_PATH
    with open(p, encoding="utf-8") as f:
        return json.load(f)
