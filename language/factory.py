""" Language factor module """
from vibhaga.inspector import Inspector
from language.abstract_language import AbstractLanguage
from language.abap import Abap


_PACKAGE = "language"


def get_all_languages() -> []:
    """ Returns all language modules dynamically """
    return Inspector().get_modules_in_cwd_path(
        _PACKAGE,
        ["factory", "abstract"])


def get_lang_obj(name: str) -> AbstractLanguage:
    """ Returns a new language object """
    if name.lower() == "abap":
        return Abap()
    raise Exception("Unknown language: " + name)
