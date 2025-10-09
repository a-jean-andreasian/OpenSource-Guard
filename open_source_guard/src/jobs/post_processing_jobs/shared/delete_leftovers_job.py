from open_source_guard.src.file_record import FileRecordAsDictType


def delete_leftovers(
    metadata: list[FileRecordAsDictType],
    transaction_type
):
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
