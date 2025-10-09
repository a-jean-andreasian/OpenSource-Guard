from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from open_source_guard.src.transactions import TransactionResult
    from open_source_guard.src.metadata import MetadataLoader, MetadataDumper


class AbsPostProcessingJobManager(ABC):
    """Abstract base class for post-processing job managers."""

    @staticmethod
    @abstractmethod
    def run_jobs(
        transactions_completed: bool,
        metadata_manager: Union["MetadataLoader", "MetadataDumper"],
    ) -> "TransactionResult":
        """
        Execute post-processing tasks after encryption or decryption.

        Subclasses must define how metadata is flushed and how files are cleaned up.

        :param transactions_completed: Whether all transactions were successful.
        :param metadata_manager: Metadata handler instance (loader or dumper).
        :return: TransactionResult indicating success or failure.
        """
        pass
