from abc import ABC, abstractmethod
from typing import Any


class ArrayDequeBase(ABC):
    def __init__(self):
        self.a = []
        self.n = 0
        self.j = 0

    # ---------------------------------
    # Abstract interface requirements
    # ---------------------------------

    @property
    def size(self):
        return self.n

    def get(self, i: int):
        return self.a[self._get_mod_idx(i)]

    def set(self, i: int, x: Any):
        y = self.a[self._get_mod_idx(i)]
        self.a[self._get_mod_idx(i)] = x
        return y

    def add_first(self, x: Any):
        self.add(0, x)

    def add_last(self, x: Any):
        self.add(self.size, x)

    def remove_first(self):
        return self.remove(0)

    def remove_last(self):
        return self.remove(self.size - 1)

    # --------------------------------------------------------
    # implemented in childclass
    # --------------------------------------------------------

    def _get_mod_idx(i: int): ...

    @abstractmethod
    def add(self, i: int, x: Any): ...

    @abstractmethod
    def remove(self, i: int): ...
