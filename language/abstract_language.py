from abc import ABC, abstractmethod
from pattern.design_pattern import DesignPattern


class AbstractLanguage(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_artifacts(self, pattern: DesignPattern) -> []:
        pass

