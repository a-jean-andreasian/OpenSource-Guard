import os
from os import PathLike
from typing import TYPE_CHECKING, Type, Union, Optional
from pathlib import Path
from open_source_guard.src.key_record import EncryptionKeyRecord
from .helpers import get_folder_path_and_filename, encode_filepath

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305


class FileRecord:
    """
    Represents an encrypted file entry, storing its path, encryption key, and algorithm.

    Responsibilities:
      - Encapsulates `EncryptionKeyRecord` creation for consistent key handling
      - Uses helper functions to encode filenames deterministically
      - Provides dict serialization/deserialization for metadata storage

    Attributes:
        filepath (PathLike): Path to the original file
        encoded_filepath (PathLike): Path to the encoded file
        algorithm (Type): Encryption algorithm (AESGCM, ChaCha20Poly1305)
        filename (str): Extracted original filename
        key_record (EncryptionKeyRecord): Internal key manager
    """

    def __init__(
        self,
        filepath: PathLike,
        algorithm: Type[Union["AESGCM", "ChaCha20Poly1305"]],
        key: Optional[bytes] = None,
        use_environ: bool = False,
        environ_key: Optional[str] = None,
        use_std: bool = False,
    ):
        """
        :param filepath: Path to original file
        :param algorithm: The algorithm type
        """

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist.")

        self.key_record = EncryptionKeyRecord(key, use_environ, environ_key, use_std)
        self.algorithm = algorithm
        self.filepath = filepath

        folder, self.filename = get_folder_path_and_filename(original_filepath=self.filepath)
        self.encoded_filepath = encode_filepath(folder, self.filename, key=self.key_record.key_b64_text)

    def to_dict(self):
        """Serialize the record to a dictionary suitable for JSON storage."""
        return {
            "filepath": self.filepath,
            "encoded_filepath": self.encoded_filepath,
            "encryption_key": self.key_record.key_b64_text,  # base64 string
            "algorithm": self.algorithm.__name__,
            "filename": self.filename
        }

    def __str__(self) -> str:
        return (
            f"FileRecord("
            f"filepath='{self.filepath}', "
            f"encoded_filepath='{self.encoded_filepath}', "
            f"algorithm='{self.algorithm.__name__}')"
            f"filename='{self.filename}')"
        )

    @classmethod
    def from_dict(cls, data: dict, possible_algorithms: dict) -> "FileRecord":
        """
        Create a FileRecord instance directly from a serialized dictionary.

        Args:
            data (dict): Serialized record containing fields from to_dict()
            possible_algorithms (dict[str, Type]): Mapping of algorithm names to their classes

        Returns:
            FileRecord: A reconstructed instance
        """
        instance = cls.__new__(cls)
        instance.filepath = Path(data["filepath"])
        instance.filename = data["filename"]
        instance.encoded_filepath = Path(data["encoded_filepath"])
        instance.algorithm = possible_algorithms[data["algorithm"]]
        instance.key_record = EncryptionKeyRecord(data["encryption_key"])
        return instance
