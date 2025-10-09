from typing import TypedDict
from open_source_guard.src.algorithms import AlgorithmNameType


class FileRecordAsDictType(TypedDict):
    """
    Dictionary representation of a FileRecord object.

    Keys:
        - filepath (str): Original file path.
        - encoded_filepath (str): Path to the encoded file.
        - algorithm (AlgorithmNameType): Algorithm class name as a string.
        - key (str): Base64-encoded encryption key.
        - filename (str): Original filename.
    """
    filepath: str
    encoded_filepath: str
    algorithm: AlgorithmNameType
    key: str
    filename: str
