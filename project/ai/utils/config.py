import json
from pathlib import Path
from typing import Any

from django.conf import settings


def _require_positive_number(cfg: dict[str, Any], key: str) -> float:
    value = cfg.get(key)
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"Invalid preprocessing config: `{key}` must be a positive number.")
    return float(value)


def _require_positive_int(cfg: dict[str, Any], key: str) -> int:
    value = cfg.get(key)
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"Invalid preprocessing config: `{key}` must be a positive integer.")
    return value


def validate_preprocessing_config(cfg: dict[str, Any]) -> dict[str, Any]:
    classes = cfg.get("classes")
    if not isinstance(classes, list) or not classes or not all(isinstance(x, str) and x.strip() for x in classes):
        raise ValueError("Invalid preprocessing config: `classes` must be a non-empty list of strings.")

    normalized = dict(cfg)
    normalized["classes"] = [x.strip() for x in classes]
    normalized["chunk_duration"] = _require_positive_number(normalized, "chunk_duration")
    overlap_duration = normalized.get("overlap_duration")
    if not isinstance(overlap_duration, (int, float)) or overlap_duration < 0:
        raise ValueError("Invalid preprocessing config: `overlap_duration` must be zero or a positive number.")
    normalized["overlap_duration"] = float(overlap_duration)
    if normalized["overlap_duration"] >= normalized["chunk_duration"]:
        raise ValueError("Invalid preprocessing config: `overlap_duration` must be smaller than `chunk_duration`.")

    normalized["sample_rate"] = _require_positive_int(normalized, "sample_rate")
    normalized["n_mels"] = _require_positive_int(normalized, "n_mels")
    normalized["target_cols"] = _require_positive_int(normalized, "target_cols")
    return normalized


def load_preprocessing_config(path: Path | None = None) -> dict[str, Any]:
    p = path or settings.AI_PREPROCESSING_CONFIG_PATH
    with open(p, encoding="utf-8") as f:
        return validate_preprocessing_config(json.load(f))
