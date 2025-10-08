import os
import base64


def take_std_key() -> bytes:
    """
    Prompt the user for a 32-character key via stdin.

    Returns:
        bytes: The UTF-8 encoded representation of the entered key.
               Limited to printable ASCII/UTF-8 characters (not arbitrary binary).
    """
    while True:
        try:
            key = input("Enter 32-character key: ").strip().encode()
        except TypeError as e:
            print(f"Error: {e}, try again.")
            continue
        if len(key) != 32:
            print("Key must be exactly 32 bytes. Try again.")
            continue
        return key


def take_key_from_environ(environ_key: str) -> bytes:
    """
    Retrieve an encryption key from an environment variable.

    Args:
        environ_key (str): The name of the environment variable.

    Returns:
        bytes: UTF-8 encoded value of the environment variable.
               Note: environment variables can only store text, not raw binary.
    """
    env_value = os.environ.get(environ_key)
    if not env_value:
        raise ValueError(f"Environment variable '{environ_key}' not found.")
    return env_value.encode() if isinstance(env_value, str) else bytes(env_value)


def ensure_bytes(key: bytes | str) -> bytes:
    """
    Normalize a key to raw bytes.

    - If the key is a base64-encoded string, it is decoded and validated.
    - If the key is a regular string (not base64), it is UTF-8 encoded.
    - If the key is already bytes, it is returned unchanged.

    Raises:
        TypeError: If the input is not a `bytes` or `str` type.
        ValueError: If the decoded base64 key is not exactly 32 bytes long.

    Returns:
        bytes: A 32-byte encryption key ready for use in cryptographic operations.
    """
    if isinstance(key, str):
        try:
            # Try to decode if it’s base64 string
            decoded = base64.b64decode(key, validate=True)
            if len(decoded) == 32:
                return decoded
        except Exception:
            # Not base64 - treating as plain string key
            key = key.encode()
    if not isinstance(key, bytes):
        raise TypeError("key must be bytes or base64 string")
    return key
