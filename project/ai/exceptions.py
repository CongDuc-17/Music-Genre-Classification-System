class AudioDecodeError(Exception):
    """Raised when the backend cannot decode audio (e.g. MP3 without FFmpeg)."""
