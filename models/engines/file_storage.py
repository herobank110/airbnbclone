import json
import os


class FileStorage:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self.data = {}
        # Try to load initial data.
        self.load()

    def save(self):
        with open(self._filepath, "w") as fp:
            json.dump(self.data, fp, indent=2)

    def load(self):
        # blank state - no file
        if not os.path.exists(self._filepath):
            self.data = {}
            return
        # load from disk
        with open(self._filepath) as fp:
            self.data = json.load(fp)
