import os

from open_source_guard import MetadataDumper
from open_source_guard.src.cipher_excutor.helpers import delete_file
from open_source_guard.src.shared import TransactionResult


class EncryptionFinalizerJob:
    @staticmethod
    def finalize(metadata_dumper: "MetadataDumper", transactions_completed: bool) -> TransactionResult:
        """
        Finalizes the encryption process by saving metadata or cleaning up partial results.

        If all file encryptions were successful, metadata is dumped to json, original files deleted, and dumper flushed.
        If any of encryptions failed, partial encrypted files are deleted and dumper flushed.

        :param metadata_dumper: Object responsible for collecting and writing encryption metadata.
        :param transactions_completed: Whether all encryption operations were successful.
        :return: TransactionResult indicating success or failure with a message.
        """

        def delete_leftovers(metadata: list[dict]):
            """
            - If transaction was successful - deletes encrypted files created during a failed encryption process.
            - Otherwise deletes the generated encrypted files so far
            """
            try:
                for file_record_dict in metadata:
                    if transactions_completed:
                        file_to_delete = file_record_dict.get("filepath")
                    else:
                        file_to_delete = file_record_dict.get("encoded_filepath")

                    if file_to_delete and os.path.exists(file_to_delete):
                        delete_file(file_to_delete)
            except Exception as e:
                raise RuntimeError(f"#TODO fix this bug {str(e)}")

        if transactions_completed:
            metadata_dumper.dump_metadata()
            delete_leftovers(metadata=metadata_dumper.cumulated_metadata)
            metadata_dumper.flush()
            return TransactionResult(status=True, msg="Files have successfully been encrypted.")
        else:
            delete_leftovers(metadata=metadata_dumper.cumulated_metadata)
            metadata_dumper.flush()
            return TransactionResult(status=False, msg="Failed to encrypt")
