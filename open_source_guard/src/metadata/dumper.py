import json

from open_source_guard.src.metadata.metadata import MetadataBase


class MetadataDumper(MetadataBase):
    def add_metadata(self, file_record_dict: dict):
        """
        :param file_record_dict: dictionary whose structure is the attributes of FileRecord class.
        """
        if not isinstance(file_record_dict, dict):
            raise TypeError("file_record must be a dictionary structure of a FileRecord object.")
        self.current_metadata.append(file_record_dict)

    def dump_metadata(self) -> None:
        with self.lock:
            with open(self.metadata_file, "w", encoding='utf-8') as f:
                json.dump(self.current_metadata, f, indent=4)
