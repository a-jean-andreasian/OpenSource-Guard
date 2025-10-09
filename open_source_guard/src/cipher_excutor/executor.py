import os
from os import PathLike
from typing import TYPE_CHECKING, Iterable
from ._helpers import read_file, write_to_file
from open_source_guard.src.shared.dto.crypto_transaction import CryptoGraphicTransactionResult, \
    CryptoGraphicTransactionsResult
from multiprocessing import Lock
from open_source_guard.src.jobs.post_processing_jobs import PostDecryptionJobManager, PostEncryptionJobManager
from open_source_guard.src.models.file_record import FileRecord

if TYPE_CHECKING:
    from open_source_guard.src.metadata import MetadataDumper, MetadataLoader
    from open_source_guard.src.algorithms import AlgorithmType
    from open_source_guard.src.jobs.responses import JobManagerResult


class CipherExecutorBase:
    @staticmethod
    def encrypt_file(file_record: "FileRecord") -> CryptoGraphicTransactionResult:
        encryption_key = file_record.key_record.key_bytes
        algo = file_record.algorithm(key=encryption_key)
        data = read_file(path=file_record.filepath)
        nonce = os.urandom(12)
        encrypted = algo.encrypt(nonce, data, None)

        try:
            with open(file_record.encoded_filepath, mode='wb') as bfile:
                bfile.write(nonce + encrypted)
            return CryptoGraphicTransactionResult(
                status=True, file_record=file_record
            )
        except Exception as e:
            return CryptoGraphicTransactionResult(
                status=False,
                msg=f"Couldn't encrypt the file.\nReason: {str(e)}",
                failed_func=CipherExecutorBase.encrypt_file
            )

    @staticmethod
    def decrypt_file(file_record: "FileRecord") -> CryptoGraphicTransactionResult:
        encryption_key = file_record.key_record.key_bytes
        algo = file_record.algorithm(key=encryption_key)
        data = read_file(file_record.encoded_filepath)
        nonce, ciphertext = data[:12], data[12:]
        decrypted = algo.decrypt(nonce, ciphertext, None)

        try:
            write_to_file(path=file_record.filepath, content=decrypted)
            return CryptoGraphicTransactionResult(status=True, msg=f"File {file_record.filepath} has been decrypted")
        except Exception as e:
            return CryptoGraphicTransactionResult(
                status=False,
                msg=f"Couldn't decrypt the file.\nReason: {str(e)}",
                failed_func=CipherExecutorBase.decrypt_file
            )


class CipherExecutorExtended:
    def __init__(self):
        self.cipher_exec_base = CipherExecutorBase()
        self.exec_lock = Lock()  # global lock for the whole operation

    def encrypt_files(
        self, files: Iterable[PathLike], metadata_dumper: "MetadataDumper", algorithm: "AlgorithmType", key=None
    ) -> CryptoGraphicTransactionsResult:

        with self.exec_lock:
            encryptions_completed = True
            failed_transaction = None
            failed_transaction_reason = None

            for file in files:
                file_record: FileRecord = FileRecord(filepath=file, algorithm=algorithm, key=key)
                file_encryption_result: CryptoGraphicTransactionResult = self.cipher_exec_base.encrypt_file(file_record)

                if not file_encryption_result.status:
                    encryptions_completed = False
                    failed_transaction = file_encryption_result.failed_func
                    failed_transaction_reason = file_encryption_result.msg
                    break

                metadata_dumper.add_metadata(file_record_dict=file_record.to_dict())

            jobs_results: JobManagerResult = PostEncryptionJobManager.run_jobs(
                metadata_manager=metadata_dumper,
                encryptions_completed=encryptions_completed
            )

            return CryptoGraphicTransactionsResult(
                transactions_status=encryptions_completed,
                failed_transaction=failed_transaction,
                failed_transaction_reason=failed_transaction_reason,
                post_jobs_status=jobs_results.status,
                post_jobs_msg=jobs_results.msg,
                failed_jobs=jobs_results.failed_jobs,
                transactions_msg=f"Failed transaction: {failed_transaction}"
            )

    def decrypt_files(self, metadata_loader: "MetadataLoader"):
        with self.exec_lock:
            decryptions_completed = True
            failed_transactions = None

            metadata_loader.load_metadata()
            for file_record in metadata_loader.current_metadata:
                transaction_result = self.cipher_exec_base.decrypt_file(file_record)
                if not transaction_result.status:
                    decryptions_completed = False
                    break

            jobs_results: JobManagerResult = PostDecryptionJobManager.run_jobs(
                transactions_completed=decryptions_completed,
                metadata_manager=metadata_loader
            )

            return CryptoGraphicTransactionsResult(
                transactions_status=decryptions_completed,
                post_jobs_status=jobs_results.status,
                post_jobs_msg=f"Failed jobs: {jobs_results.failed_jobs}",
                transactions_msg=f"Failed transactions: {failed_transactions}"
            )
