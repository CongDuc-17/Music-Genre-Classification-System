"""
Lazy singleton loader for the Keras .h5 model.
"""
from __future__ import annotations

import threading
from pathlib import Path

from django.conf import settings

from ai.exceptions import AudioDecodeError
from ai.utils.config import load_preprocessing_config

_model = None
_lock = threading.Lock()


def get_model():
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        try:
            import tensorflow as tf
        except ImportError as e:
            raise AudioDecodeError(
                "Missing TensorFlow dependency. Install the project dependencies with "
                "`pip install -r project/requirements.txt`, then restart the server. "
                f"Details: {e}"
            ) from e

        path = Path(settings.AI_MODEL_PATH)
        if not path.is_file():
            raise AudioDecodeError(f"Model file not found: {path}")
        tf.keras.backend.clear_session()
        _model = tf.keras.models.load_model(str(path))
        _validate_model_shape(_model)
        return _model


def _validate_model_shape(model) -> None:
    cfg = load_preprocessing_config()
    expected_input = (cfg["n_mels"], cfg["target_cols"], 1)
    input_shape = tuple(model.input_shape[1:]) if model.input_shape else ()
    if input_shape != expected_input:
        raise AudioDecodeError(
            "Model input shape does not match preprocessing_config.json. "
            f"Expected {expected_input}, got {input_shape}."
        )

    expected_outputs = len(cfg["classes"])
    output_shape = tuple(model.output_shape) if model.output_shape else ()
    actual_outputs = output_shape[-1] if output_shape else None
    if actual_outputs != expected_outputs:
        raise AudioDecodeError(
            "Model output class count does not match preprocessing_config.json. "
            f"Expected {expected_outputs}, got {actual_outputs}."
        )
