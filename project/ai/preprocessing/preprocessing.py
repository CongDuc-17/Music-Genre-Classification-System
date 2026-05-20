"""
Audio preprocessing — matches ThirdTraining.ipynb (mel chunks, truncate/pad).
Short files are tiled to one full chunk length so inference still runs (demo UX).
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

from ai.exceptions import AudioDecodeError
from ai.utils.config import load_preprocessing_config

logger = logging.getLogger(__name__)


def _load_audio_deps():
    try:
        import librosa
        import numpy as np
    except ImportError as e:
        raise AudioDecodeError(
            "Missing audio processing dependency. Install the project dependencies with "
            "`pip install -r project/requirements.txt`, then restart the server. "
            f"Current Python: {sys.executable}. "
            f"Details: {e}"
        ) from e
    return librosa, np


def _cfg() -> dict[str, Any]:
    return load_preprocessing_config()


def audio_to_mel_chunks(
    file_path: str | Path,
    *,
    chunk_duration: float | None = None,
    overlap_duration: float | None = None,
    sample_rate: int | None = None,
    n_mels: int | None = None,
    target_cols: int | None = None,
) -> list[np.ndarray]:
    librosa, np = _load_audio_deps()
    cfg = _cfg()
    chunk_duration = chunk_duration if chunk_duration is not None else cfg["chunk_duration"]
    overlap_duration = overlap_duration if overlap_duration is not None else cfg["overlap_duration"]
    sample_rate = sample_rate if sample_rate is not None else cfg["sample_rate"]
    n_mels = n_mels if n_mels is not None else cfg["n_mels"]
    target_cols = target_cols if target_cols is not None else cfg["target_cols"]

    try:
        audio, sr = librosa.load(str(file_path), sr=sample_rate, mono=True)
    except Exception as e:
        logger.warning("librosa.load failed for %s: %s", file_path, e)
        raise AudioDecodeError(
            "Could not decode this audio file. For MP3 on Windows, install FFmpeg "
            "(https://ffmpeg.org) and add it to PATH, or use WAV. "
            f"Details: {e}"
        ) from e

    chunk_samples = int(chunk_duration * sr)
    overlap_samples = int(overlap_duration * sr)
    step = chunk_samples - overlap_samples

    if len(audio) == 0:
        raise AudioDecodeError("Decoded audio is empty (0 samples).")

    # Training expects 4s chunks; tile short clips so we still produce valid mel input.
    if len(audio) < chunk_samples:
        reps = int(np.ceil(chunk_samples / len(audio)))
        audio = np.tile(audio, reps)[:chunk_samples]

    num_chunks = int(np.ceil((len(audio) - chunk_samples) / step)) + 1
    chunks_out: list[np.ndarray] = []

    for i in range(num_chunks):
        start = int(i * step)
        end = start + chunk_samples
        chunk = audio[start:end]

        if len(chunk) < chunk_samples:
            continue

        mel = librosa.feature.melspectrogram(y=chunk, sr=sr, n_mels=n_mels)
        mel_db = librosa.power_to_db(mel, ref=np.max)
        mel_min, mel_max = mel_db.min(), mel_db.max()
        mel_norm = (mel_db - mel_min) / (mel_max - mel_min + 1e-6)

        current_cols = mel_norm.shape[1]
        if current_cols >= target_cols:
            mel_fixed = mel_norm[:, :target_cols]
        else:
            pad = target_cols - current_cols
            mel_fixed = np.pad(mel_norm, ((0, 0), (0, pad)), mode="constant", constant_values=0)

        chunks_out.append(np.expand_dims(mel_fixed, axis=-1))

    return chunks_out


def get_audio_metadata(file_path: str | Path) -> dict[str, Any]:
    librosa, _ = _load_audio_deps()
    path = Path(file_path)
    try:
        y, sr = librosa.load(str(path), sr=None, mono=True)
        duration = float(len(y) / sr) if sr else 0.0
    except Exception as e:
        logger.debug("get_audio_metadata load failed: %s", e)
        duration = 0.0
        sr = None

    return {
        "filename": path.name,
        "size_bytes": path.stat().st_size if path.is_file() else 0,
        "duration_seconds": round(duration, 3),
        "sample_rate": int(sr) if sr is not None else None,
    }
