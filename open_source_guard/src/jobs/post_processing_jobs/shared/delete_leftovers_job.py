import os
from open_source_guard.src.models.file_record import FileRecordAsDictType
from open_source_guard.src.jobs.responses import SingleJobResult
import typing
from open_source_guard.src.shared.types import DecryptionTransaction, EncryptionTransaction
if typing.TYPE_CHECKING:
    from open_source_guard.src.cipher_excutor import TransactionType


def delete_leftovers(
    file_records_arr: list[FileRecordAsDictType],
    transactions_completed: bool,
    transaction_type: "TransactionType"
) -> SingleJobResult:
    """
    - If transaction was successful - deletes encrypted files created during a failed encryption process.
    - Otherwise deletes the generated encrypted files so far
    """

    # Encryption completed: yes-filepath, no - encoded_filepath
    # Decryption completed: yes-encoded_filepath, no-filepath

    try:
        if transaction_type is EncryptionTransaction:
            file_to_delete_key: str = "filepath" if transactions_completed else "encoded_filepath"
        elif transaction_type is DecryptionTransaction:
            file_to_delete_key: str = "encoded_filepath" if transactions_completed else "filepath"
        else:
            raise RuntimeError("#TODO FIX this: wrong transaction type received.")

        for file_record_dict in file_records_arr:
            file_to_delete: str | os.PathLike | None = file_record_dict.get(file_to_delete_key)  # type: ignore

            if file_to_delete and os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    except Exception as e:
        return SingleJobResult(status=False, msg=str(e), job=delete_leftovers)
    else:
        return SingleJobResult(status=True, job=delete_leftovers)
