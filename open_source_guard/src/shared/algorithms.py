from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from typing import Type, Union

AlgorithmType = Type[Union[AESGCM, ChaCha20Poly1305]]

POSSIBLE_ALGORITHMS = {
    "AESGCM": AESGCM,
    "ChaCha20Poly1305": ChaCha20Poly1305,
}
