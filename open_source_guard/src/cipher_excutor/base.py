import os
from open_source_guard.src.transactions import TransactionResult
from .helpers import read_file, write_to_file
from open_source_guard.src.file_record import FileRecord


class CipherExecutorBase:
    @staticmethod
    def encrypt_file(file_record: "FileRecord") -> TransactionResult:
        encryption_key = file_record.key_record.key_bytes
        algo = file_record.algorithm(key=encryption_key)
        data = read_file(path=file_record.filepath)
        nonce = os.urandom(12)
        encrypted = algo.encrypt(nonce, data, None)

        try:
            with open(file_record.encoded_filepath, mode='wb') as bfile:
                bfile.write(nonce + encrypted)
            return TransactionResult(status=True, file_record=file_record)
        except Exception as e:
            return TransactionResult(status=False, msg=str(e))

    def decrypt_file(self, file_record: "FileRecord") -> TransactionResult:
        encryption_key = file_record.key_record.key_bytes
        algo = file_record.algorithm(key=encryption_key)
        data = read_file(file_record.encoded_filepath)
        nonce, ciphertext = data[:12], data[12:]
        decrypted = algo.decrypt(nonce, ciphertext, None)

        try:
            write_to_file(path=file_record.filepath, content=decrypted)
            return TransactionResult(status=True, msg=f"File {file_record.filepath} has been decrypted")
        except Exception as e:
            return TransactionResult(status=False, msg=f"Couldn't decrypt the file.\nReason: {str(e)}")
