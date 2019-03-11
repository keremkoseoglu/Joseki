from language.abstract_language import AbstractLanguage
from language.abap import Abap
from config import oop

_PACKAGE = "language"


def get_all_languages() -> []:
    return oop.get_all_concrete_classes(_PACKAGE)


def get_lang_obj(name: str) -> AbstractLanguage:
    if name.lower() == "abap":
        return Abap()
    else:
        raise Exception("Unknown language: " + name)
