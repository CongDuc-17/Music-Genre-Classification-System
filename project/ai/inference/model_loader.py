"""
Lazy singleton loader for the Keras .h5 model.
"""
from __future__ import annotations

import threading
from pathlib import Path

from django.conf import settings

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
            from ai.exceptions import AudioDecodeError

            raise AudioDecodeError(
                "Missing TensorFlow dependency. Install the project dependencies with "
                "`pip install -r project/requirements.txt`, then restart the server. "
                f"Details: {e}"
            ) from e

        path = Path(settings.AI_MODEL_PATH)
        if not path.is_file():
            from ai.exceptions import AudioDecodeError

            raise AudioDecodeError(f"Model file not found: {path}")
        tf.keras.backend.clear_session()
        _model = tf.keras.models.load_model(str(path))
        return _model
