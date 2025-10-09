import os
from open_source_guard.src.cipher_excutor.helpers import delete_file
from open_source_guard.src.file_record import FileRecord
from open_source_guard.src.transactions import TransactionResult
from open_source_guard.src.jobs.post_processing_jobs.base import AbsPostProcessingJobManager
import typing

if typing.TYPE_CHECKING:
    from open_source_guard.src.metadata import MetadataLoader



class PostDecryptionJobManager(AbsPostProcessingJobManager):
    @staticmethod
    def run_jobs(transactions_completed: bool, metadata_loader: "MetadataLoader") -> TransactionResult:
        """
        Finalizes the decryption process by cleaning up outputs or flushing metadata.

        - If all decryptions succeeded: flushes metadata and deletes original encoded files.
        - If any decryption failed: deletes partially decrypted files to avoid leaving incomplete data.

        :param transactions_completed: Whether all decryption operations were successful.
        :param metadata_loader: Object responsible for loading and managing decryption metadata.
        :return: TransactionResult indicating success or failure with a message.
        """

        file_records: list["FileRecord"] = metadata_loader.current_metadata

        def delete_leftovers(records: list["FileRecord"]):
            """
            - If transaction was successful: delete encoded (encrypted) files.
            - If transaction failed: delete partially decrypted plaintext files.
            """
            try:
                for file_record in records:
                    if transactions_completed:
                        file_to_delete = file_record.encoded_filepath
                    else:
                        file_to_delete = file_record.filepath

                    if file_to_delete and os.path.exists(file_to_delete):
                        delete_file(file_to_delete)
            except Exception as e:
                raise RuntimeError(f"#TODO fix this bug {str(e)}")

        if transactions_completed:
            delete_leftovers(file_records)
            metadata_loader.flush()
            return TransactionResult(status=True, msg="Files have been successfully decrypted.")
        else:
            delete_leftovers(file_records)
            metadata_loader.flush()
            return TransactionResult(status=False, msg="Failed to decrypt one or more files.")
