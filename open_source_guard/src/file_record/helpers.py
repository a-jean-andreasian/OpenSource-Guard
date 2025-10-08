import os
import hashlib


def get_folder_path_and_filename(original_filepath) -> tuple[os.PathLike, str]:
    """
    Gets a file path, returns the folder path and the filename
    """
    folder_path = os.path.dirname(original_filepath)
    filename = os.path.basename(original_filepath)
    return folder_path, filename


def encode_filepath(original_folder: os.PathLike, original_filename: os.PathLike, key: bytes) -> os.PathLike:
    """
    1. Gets a file path
    2. Detects the file and the folder
    3. Encodes the filename
    4. Returns a new filepath with the same folder but encoded filename

    :param original_folder: The folder of a file
    :param original_filename: The name of a file
    :param key: Encoding key
    """

    ...

    def encode_filename(filename: str, key: bytes | str) -> str:
        """
        Encodes the filename using SHA-256 with the given key.

        :param filename: The name of the file
        :param key: The encoding key (bytes or string)
        :return: Hexadecimal hash string
        """
        if isinstance(key, str):
            key = key.encode()
        name_hash = hashlib.sha256(filename.encode() + key).hexdigest()
        return name_hash

    ...

    encoded_filename = encode_filename(filename=original_filename, key=key)
    encoded_filepath = os.path.join(original_folder, encoded_filename)
    return encoded_filepath
