import os
import base64
from typing import Optional
from ._helpers import take_std_key, take_key_from_environ, ensure_bytes


class EncryptionKeyRecord:
    """
    Handles encryption key retrieval and normalization.
    Ensures all keys are base64-encoded for consistent serialization.
    """

    def __init__(
        self,
        key: Optional[bytes | str] = None,
        use_environ: bool = False,
        environ_key: Optional[str] = None,
        use_std: bool = False,
    ):
        if key is not None:
            self._key_bytes = ensure_bytes(key)

        elif use_environ:
            key_from_environ: bytes = take_key_from_environ(environ_key)  # utf-8
            self._key_bytes = ensure_bytes(key_from_environ)

        elif use_std:
            std_key: bytes = take_std_key()
            self._key_bytes = ensure_bytes(std_key)

        else:
            self._key_bytes = os.urandom(32)

        assert len(self._key_bytes) == 32, "Encryption key must be exactly 32 bytes"
        self._key_b64 = base64.b64encode(self._key_bytes).decode("utf-8")

    @property
    def key_bytes(self) -> bytes:
        """Return raw 32-byte key"""
        return self._key_bytes

    @property
    def key_b64_text(self) -> str:
        """Return base64-encoded key (UTF-8 string)"""
        return self._key_b64
