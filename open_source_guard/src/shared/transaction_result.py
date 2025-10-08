import typing
import json

if typing.TYPE_CHECKING:
    from open_source_guard.src.file_record import FileRecord


class TransactionResult:
    """
    Represents the outcome of a single encryption or decryption operation.

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
        >>> result = TransactionResult(status=True, msg="Encryption successful.")
        >>> print(result.to_dict())
        {'status': True, 'file_record': None, 'msg': 'Encryption successful.'}
    """

    def __init__(
        self,
        status: bool,
        file_record: typing.Optional["FileRecord"] = None,
        msg: typing.Optional[str] = None
    ):
        self.status: bool = status
        self.file_record: typing.Optional["FileRecord"] = file_record
        self.msg: typing.Optional[str] = msg

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
