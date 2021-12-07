import pathlib


class FileIndex:
    def __init__(self):
        self.path = pathlib.Path(__file__).parent.parent / "moodle_sync"
        self.index = self.scan()

    def scan(self):
        return [
            [i.name for i in p.iterdir() if i.is_file() and i.suffix == ".pdf"]
            for p in self.path.iterdir()
        ]
