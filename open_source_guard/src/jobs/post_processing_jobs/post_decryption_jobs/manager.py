import os
from open_source_guard.src.models.file_record import FileRecord
from open_source_guard.src.jobs.post_processing_jobs.base import AbsPostProcessingJobManager
from open_source_guard.src.jobs.responses import SingleJobResult, JobManagerResult
import typing
from open_source_guard.src.jobs.post_processing_jobs.shared import delete_leftovers
from open_source_guard.src.shared.types import DecryptionTransaction

if typing.TYPE_CHECKING:
    from open_source_guard.src.metadata import MetadataLoader



class PostDecryptionJobManager(AbsPostProcessingJobManager):
    success_msg = "Files have successfully been decrypted."
    failure_msg = "Failed to decrypt the files"
    transaction_type = DecryptionTransaction


    @classmethod
    def run_jobs(
        cls,
        transactions_completed: bool,
        metadata_manager: "MetadataLoader",
    ):
        """
        Finalizes the decryption process by cleaning up outputs or flushing metadata.

        - If all decryptions succeeded: flushes metadata and deletes original encoded files.
        - If any decryption failed: deletes partially decrypted files to avoid leaving incomplete data.

        :param transactions_completed: Whether all decryption operations were successful.
        :param metadata_manager: Object responsible for loading and managing decryption metadata.
        :return: CryptoGraphicTransactionResult indicating success or failure with a message.
        """

        file_records: list["FileRecord"] = metadata_manager.current_metadata

        # def delete_leftovers(records: list["FileRecord"]):
        #     """
        #     - If transaction was successful: delete encoded (encrypted) files.
        #     - If transaction failed: delete partially decrypted plaintext files.
        #     """
        #     try:
        #         for file_record in records:
        #             if transactions_completed:
        #                 file_to_delete = file_record.encoded_filepath
        #             else:
        #                 file_to_delete = file_record.filepath
        #
        #             if file_to_delete and os.path.exists(file_to_delete):
        #                 os.remove(file_to_delete)
        #     except Exception as e:
        #         raise RuntimeError(f"#TODO fix this bug {str(e)}")

        failed_jobs: list["SingleJobResult"] = []

        def run_job(func: typing.Callable, **kwargs) -> typing.Optional["SingleJobResult"]:
            result = func(**kwargs)
            if not result.status:
                failed_jobs.append(result)
            return result

        file_records = [file_record.to_dict() for file_record in file_records]

        run_job(
            func=delete_leftovers,
            file_records_arr=file_records,
            transactions_completed=transactions_completed,
            transaction_type=cls.transaction_type
        )

        # final 3: flush metadata_manager | can't fail
        metadata_manager.flush()

        return JobManagerResult(
            status=not failed_jobs,
            failed_jobs=failed_jobs,
            msg=cls.success_msg if not failed_jobs else cls.failure_msg
        )
