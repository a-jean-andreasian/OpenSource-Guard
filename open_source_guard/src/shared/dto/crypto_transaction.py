import json
import typing

from open_source_guard.src.models.file_record import FileRecord


class CryptoGraphicTransactionResult:
    """
    Represents the outcome of a SINGLE encryption or decryption operation.

    This class is used as a unified return type across the application for both
    file-level and operation-level results. It serves as a lightweight data
    transfer object (DTO) to indicate whether an operation succeeded, include
    optional details about the related file, and carry any relevant message.

    Attributes:
        status (bool): Indicates if the transaction succeeded (True) or failed (False).
        file_record (FileRecord | None): Optional reference to the file associated with this result.
        msg (str | None): Optional message describing the operation result or error reason.

    Methods:
        __bool__(): Returns the value of `status` when used in a boolean context.
        to_dict(): Returns a dictionary representation of the result.
        to_json(): Returns a JSON-formatted string representation of the result.

    Example:
        >>> result = CryptoGraphicTransactionResult(status=True, msg="Encryption successful.")
        >>> print(result.to_dict())
        {'status': True, 'file_record': None, 'msg': 'Encryption successful.'}
    """

    def __init__(
        self,
        status: bool,
        file_record: typing.Optional["FileRecord"] = None,
        msg: typing.Optional[str] = None,
        failed_func: typing.Callable = None
    ):
        self.status: bool = status
        self.file_record: typing.Optional["FileRecord"] = file_record
        self.msg: typing.Optional[str] = msg
        self.failed_func = failed_func

    def __bool__(self):
        return self.status is True

    def to_dict(self) -> dict:
        file_record = self.file_record.to_dict() if self.file_record else None  # it's an optional field

        return {
            "status": self.status,
            "msg": self.msg,
            "file_record": file_record
        }

    def to_json(self) -> str:
        """ Returns a JSON-formatted string of the transaction result. """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)


class CryptoGraphicTransactionsResult:
    """
    Represents the outcome of a GROUP of encryption or decryption operation.

    Attributes:
        transactions_status (bool): Indicates if all transaction succeeded (True) or failed (False).
        post_jobs_status (bool): Indicated if all post transaction jobs succeeded (True) or failed (False).
        transactions_msg (str): If transaction failed this will contain the details. Optionally on success as well.
        post_jobs_msg (str): If post-transaction jobs failed this will contain the details. Optionally on success.

    """

    def __init__(
        self,
        transactions_status: bool,
        post_jobs_status: bool,

        transactions_msg: str = None,
        post_jobs_msg: str = None,

        failed_transaction: typing.Callable = None,
        failed_transaction_reason: str = None,

        failed_jobs=None
    ):
        self.transactions_status = transactions_status
        self.post_jobs_status = post_jobs_status
        self.transactions_msg = transactions_msg
        self.post_jobs_msg = post_jobs_msg
        self.failed_transaction = failed_transaction
        self.failed_transaction_reason = failed_transaction_reason,
        self.failed_jobs = failed_jobs

    def __str__(self):
        return (
            f"CryptoGraphicTransactionsResult("
            f"transactions_status={self.transactions_status}, "
            f"post_jobs_status={self.post_jobs_status}, "
            f"transactions_msg={repr(self.transactions_msg)}, "
            f"post_jobs_msg={repr(self.post_jobs_msg)})"
        )
