""" Abstract language module """
from abc import ABC, abstractmethod
from pattern.design_pattern import DesignPattern


class AbstractLanguage(ABC):
    """ Abstract language class """

    @abstractmethod
    def get_artifacts(self, pattern: DesignPattern) -> []:
        """ Returns all artifacts """
