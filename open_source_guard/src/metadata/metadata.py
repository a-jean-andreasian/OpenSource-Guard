import os
from multiprocessing import Lock
from open_source_guard.src.shared import POSSIBLE_ALGORITHMS


class MetadataBase:
    """
    For children enforces  declarative usage through a settings file, not dynamic.
    """

    def __init__(
        self,
        root: os.PathLike,
        metadata_folder: os.PathLike,
        metadata_filename: os.PathLike,
    ):
        """
        :param root: Root of the project

        Note: set the metadata folder path and metadata filename from settings.py file.
        """

        metadata_path = os.path.join(root, metadata_folder)
        if not os.path.exists(path=metadata_path):
            os.makedirs(metadata_folder, exist_ok=True)

        self.metadata_file = os.path.join(metadata_folder, metadata_filename)
        self.possible_algorithms = POSSIBLE_ALGORITHMS
        self.lock = Lock()

        self.current_metadata = []

    ...
    # shared methods
    ...

    @property
    def cumulated_metadata(self):
        return self.current_metadata

    def flush(self):
        self.current_metadata.clear()
