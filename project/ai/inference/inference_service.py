"""
Inference: chunk predictions averaged (same as training notebook).
Heavy deps (NumPy, TensorFlow) load only when this runs.
"""
from __future__ import annotations

from typing import Any

from ai.exceptions import AudioDecodeError
from ai.utils.config import load_preprocessing_config


def predict_genre_from_path(
    file_path: str,
    *,
    top_k: int = 5,
    batch_size: int = 16,
) -> dict[str, Any] | None:
    try:
        import numpy as np
    except ImportError as e:
        raise AudioDecodeError(
            "Missing AI dependency. Install the project dependencies with "
            "`pip install -r project/requirements.txt`, then restart the server. "
            f"Details: {e}"
        ) from e

    from ai.inference.model_loader import get_model
    from ai.preprocessing.preprocessing import audio_to_mel_chunks

    cfg = load_preprocessing_config()
    classes: list[str] = list(cfg["classes"])

    chunks = audio_to_mel_chunks(file_path)
    if not chunks:
        return None  # should not happen after successful decode + padding

    model = get_model()
    x_input = np.array(chunks, dtype=np.float32)
    y_pred_chunks = model.predict(x_input, batch_size=batch_size, verbose=0)
    avg_scores = y_pred_chunks.mean(axis=0)
    predicted_idx = int(np.argmax(avg_scores))
    top_k_idx = np.argsort(avg_scores)[::-1][:top_k]
    top_k_preds = [{"genre": classes[i], "score": float(avg_scores[i])} for i in top_k_idx]

    probabilities = {classes[i]: float(avg_scores[i]) for i in range(len(classes))}

    return {
        "genre": classes[predicted_idx],
        "confidence": float(avg_scores[predicted_idx]),
        "num_chunks": len(chunks),
        "probabilities": probabilities,
        "top_k_predictions": top_k_preds,
    }
