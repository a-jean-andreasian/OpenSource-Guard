from .metadata import MetadataBase
import json
from open_source_guard.src.file_record import FileRecord


class MetadataLoader(MetadataBase):
    def load_metadata(self) -> None:
        with self.lock:  # keeping the file locked till the function hasn't returned info
            with open(self.metadata_file, "r", encoding='utf-8') as f:
                metadata_list: list[dict] = json.load(f)

            for json_record in metadata_list:
                file_record: "FileRecord" = FileRecord.from_dict(json_record, self.possible_algorithms)
                self.current_metadata.append(file_record)
