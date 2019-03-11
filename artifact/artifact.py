import os

_DEFAULT_DIR = "/Users/Kerem/Downloads/"


class Artifact:

    def __init__(self):
        self.name = ""
        self.description = ""
        self.file_name = ""
        self.content = []

    def save_to_disk(self, directory: str = _DEFAULT_DIR):
        if self.file_name == "":
            raise Exception("Can't save artifact to disk, file name missing")
        path = os.path.join(directory, self.file_name)
        with open(path, "w") as f:
            for c in self.content:
                print(c, file=f)
