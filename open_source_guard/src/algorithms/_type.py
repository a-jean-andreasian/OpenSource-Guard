from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from typing import Type, Union

AlgorithmType = Type[Union[AESGCM, ChaCha20Poly1305]]
AlgorithmNameType = Type[Union["AESGCM", "ChaCha20Poly1305"]]
