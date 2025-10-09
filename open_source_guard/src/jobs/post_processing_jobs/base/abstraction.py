from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from open_source_guard.src.jobs.responses import JobManagerResult
    from open_source_guard.src.metadata import MetadataLoader, MetadataDumper
    from open_source_guard.src.cipher_excutor import TransactionType



class AbsPostProcessingJobManager(ABC):
    """Abstract base class for post-processing job managers."""
    success_msg: str
    failure_msg: str
    transaction_type: "TransactionType"

    @classmethod
    @abstractmethod
    def run_jobs(
        cls,
        transactions_completed: bool,
        metadata_manager: Union["MetadataLoader", "MetadataDumper"],
    ) -> "JobManagerResult":
        """
        Execute post-processing tasks after encryption or decryption.

        Subclasses must define how metadata is flushed and how files are cleaned up.

        :param transactions_completed: Whether all transactions were successful.
        :param metadata_manager: Metadata handler instance (loader or dumper).
        """
        pass
