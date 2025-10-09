from .cipher_excutor import CipherExecutorExtended
from open_source_guard.src.algorithms import AlgorithmType
import os
from typing import TYPE_CHECKING, Container

if TYPE_CHECKING:
    from .metadata import MetadataDumper, MetadataLoader


class OpenSourceGuard:
    def __init__(self):
        self.enc = CipherExecutorExtended()

    def encrypt(
        self,
        files: Container[os.PathLike],
        metadata_dumper: "MetadataDumper",
        algorithm: AlgorithmType,
        key=None,
    ):
        return self.enc.encrypt_files(files, metadata_dumper, algorithm, key)

    def decrypt(
        self,
        metadata_loader: "MetadataLoader"
    ):
        return self.enc.decrypt_files(metadata_loader)
