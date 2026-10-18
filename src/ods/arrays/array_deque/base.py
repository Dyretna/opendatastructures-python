from abc import ABC, abstractmethod
from typing import Any


class ArrayDequeBase(ABC):
    def __init__(self):
        self.a = [None]
        self.n = 0
        self.j = 0

    # ----------------------------------------------
    # Abstract interface requirements
    # ----------------------------------------------

    @property
    def size(self):
        return self.n

    @abstractmethod
    def add_first(self, x: Any): ...

    @abstractmethod
    def add_last(self, x: Any): ...

    @abstractmethod
    def remove_first(self): ...

    @abstractmethod
    def remove_last(self): ...
