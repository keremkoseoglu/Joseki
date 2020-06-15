""" Artifact module """
import os

_DEFAULT_DIR = "/Users/Kerem/Downloads/"


class Artifact:
    """ Artifact class """

    def __init__(self):
        self.name = ""
        self.description = ""
        self.file_name = ""
        self.content = []

    def save_to_disk(self, directory: str = _DEFAULT_DIR):
        """ Writes artifact to disk """
        if self.file_name == "":
            raise Exception("Can't save artifact to disk, file name missing")
        path = os.path.join(directory, self.file_name)
        with open(path, "w") as content_file:
            for content_line in self.content:
                print(content_line, file=content_file)
