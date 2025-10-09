from os import PathLike
from typing import Iterable
import os


def are_paths_valid(filepaths: Iterable[PathLike]) -> None:
    """
    To run before encryption/decryption

    :raises FileNotFoundError: If filepath does not exist.
    """
    for path in filepaths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File: {path} does not exist.")


def read_file(path: PathLike) -> bytes:
    """
    Reads a file.

    Must be called after `.are_paths_valid` function.

    :param path: Path to the file.
    :return: Content of the file in bytes.
    :raises FileNotFoundError: If `.are_paths_valid` function was not called in advance and the `path` does not exist.
    """

    with open(path, mode='rb') as bfile:
        return bfile.read()


def write_to_file(path: PathLike, content: bytes) -> None:
    """
    Writes the binary content to a file.

    Must be called after `.are_paths_valid` function.

    :param path: Path to the encrypted file.
    :param content: Content to dump.
    :raises FileNotFoundError: If `.are_paths_valid` function was not called in advance and the `path` does not exist.
    """

    with open(path, mode='wb') as bfile:
        bfile.write(content)
