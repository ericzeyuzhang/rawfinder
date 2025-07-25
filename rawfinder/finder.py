import logging
import os
from pathlib import Path

from rawfinder.exceptions import FinderDirectoryDoesNotExistError, FinderNoExtensionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileFinder:
    def __init__(self, base_dir: Path, extensions: set[str]):
        if not base_dir.exists():
            raise FinderDirectoryDoesNotExistError(base_dir)
        if not extensions:
            raise FinderNoExtensionError

        self.base_dir = base_dir
        self.extensions = {ext.lower() for ext in extensions}

    def find_files(self) -> list[Path]:
        files = []
        for entry in os.scandir(self.base_dir):
            if entry.is_file() and Path(entry).suffix.lower() in self.extensions:
                files.append(Path(entry))
            elif entry.is_dir() and not entry.name.endswith(".lrdata"):
                logger.debug(f"Searching in subdirectory: {entry.path}")
                # Recursively find files in subdirectories
                subdir_files = FileFinder(Path(entry), self.extensions).find_files()
                files.extend(subdir_files)
        return files
