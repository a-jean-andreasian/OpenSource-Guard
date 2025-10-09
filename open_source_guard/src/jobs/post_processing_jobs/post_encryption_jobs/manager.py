from open_source_guard.src.jobs.post_processing_jobs.base import AbsPostProcessingJobManager
import typing
from open_source_guard.src.jobs.post_processing_jobs.shared import delete_leftovers
from open_source_guard.src.jobs.responses import SingleJobResult, JobManagerResult
from open_source_guard.src.shared.types import EncryptionTransaction


if typing.TYPE_CHECKING:
    from open_source_guard.src.metadata import MetadataDumper



class PostEncryptionJobManager(AbsPostProcessingJobManager):
    success_msg = "Files have successfully been encrypted."
    failure_msg = "Failed to encrypt the files"
    transaction_type = EncryptionTransaction

    @classmethod
    def run_jobs(cls, metadata_manager: "MetadataDumper", encryptions_completed: bool):
        """
        Finalizes the encryption process by saving metadata or cleaning up partial results.

        If all file encryptions were successful, metadata is dumped to json, original files deleted, and dumper flushed.
        If any of encryptions failed, partial encrypted files are deleted and dumper flushed.

        :param metadata_manager: Object responsible for collecting and writing encryption metadata.
        :param encryptions_completed: Whether all encryption operations were successful.
        :return: CryptoGraphicTransactionResult indicating success or failure with a message.
        """

        failed_jobs: list["SingleJobResult"] = []

        def run_job(func: typing.Callable, **kwargs) -> typing.Optional["SingleJobResult"]:
            result = func(**kwargs)
            if not result.status:
                failed_jobs.append(result)
            return result

        if encryptions_completed:
            # job 1:  dump metadata
            run_job(metadata_manager.dump_metadata)

        # job 2: deleting leftovers
        run_job(
            func=delete_leftovers,
            file_records_arr=metadata_manager.cumulated_metadata,
            transactions_completed=encryptions_completed,
            transaction_type=cls.transaction_type
        )

        # final 3: flush metadata_manager | can't fail
        metadata_manager.flush()

        return JobManagerResult(
            status=not failed_jobs,
            failed_jobs=failed_jobs,
            msg=cls.success_msg if not failed_jobs else cls.failure_msg
        )
