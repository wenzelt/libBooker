import pathlib
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FileIndex:
    folder: Optional[str]
    files: List[str]


class FileIndexer:
    def __init__(self):
        self.path = pathlib.Path(__file__).parent.parent / "moodle_sync"
        self.index = self.scan()

    def scan(self):
        return [
            FileIndex(
                folder=p.name,
                files=[
                    i.name for i in p.iterdir() if i.is_file() and i.suffix == ".pdf"
                ],
            )
            for p in self.path.iterdir()
        ]
