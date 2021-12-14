import os
import pathlib
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FileIndex:
    folder: Optional[str]
    files: List[str]


class FileIndexer:
    def __init__(self):
        self._root_path = pathlib.Path(__file__).parent.parent / "moodle_sync"
        #self.index = self.scan()

    def scan(self):
        return [
            FileIndex(
                folder=p.name,
                files=[
                    i.name for i in p.iterdir() if i.is_file() and i.suffix == ".pdf"
                ],
            )
            for p in self._root_path.iterdir()
        ]

    def check_if_file_exists(self, filename : str, course_name : str, extension : str):
        file_name = pathlib.Path(os.path.join(self._root_path, course_name,f"{filename}.{extension}"))
        if file_name.exists():
            return True
        else:
            return False
