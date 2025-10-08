from os import PathLike
from typing import TYPE_CHECKING, Iterable
from open_source_guard.src.shared import TransactionResult
from multiprocessing import Lock
from open_source_guard.src.jobs.post_encryption_jobs import DecryptionFinalizerJob, EncryptionFinalizerJob
from open_source_guard.src.file_record import FileRecord
from .base import CipherExecutorBase

if TYPE_CHECKING:
    from open_source_guard.src.metadata import MetadataDumper, MetadataLoader
    from open_source_guard.src.shared import AlgorithmType


class CipherExecutorExtended:
    def __init__(self):
        self.cipher_exec_base = CipherExecutorBase()
        self.exec_lock = Lock()  # global lock for the whole operation

    def encrypt_files(
        self, files: Iterable[PathLike], metadata_dumper: "MetadataDumper", algorithm: "AlgorithmType", key=None
    ) -> TransactionResult:

        with self.exec_lock:
            transactions_completed = True
            for file in files:
                file_record = FileRecord(filepath=file, algorithm=algorithm, key=key)
                transaction_result = self.cipher_exec_base.encrypt_file(file_record)
                if not transaction_result.status:
                    transactions_completed = False
                    break
                metadata_dumper.add_metadata(file_record_dict=file_record.to_dict())
        return EncryptionFinalizerJob.finalize(metadata_dumper, transactions_completed)

    def decrypt_files(self, metadata_loader: "MetadataLoader"):
        with self.exec_lock:
            transactions_completed = True
            metadata_loader.load_metadata()
            for file_record in metadata_loader.current_metadata:
                transaction_result = self.cipher_exec_base.decrypt_file(file_record)
                if not transaction_result.status:
                    transactions_completed = False
                    break
        return DecryptionFinalizerJob.finalize(transactions_completed, metadata_loader)
