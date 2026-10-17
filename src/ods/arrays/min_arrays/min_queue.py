from typing import Any

from ..array_queue import ArrayQueue


class MinQueue:
    def __init__(self):
        self.main_queue = ArrayQueue()
        self.aux_queue = ArrayQueue()

    @property
    def size(self):
        return self.aux_queue.n

    def add(self, x: Any):
        self.main_queue.add(x)

        if self.size == 0:
            self.aux_queue.add(x)
        elif x >= self.aux_queue.get(self.size - 1):
            self.aux_queue.add(self.aux_queue.get(self.size - 1))
        else:
            self.aux_queue.add(x)

    def remove(self) -> Any:
        self.main_queue.remove()
        self.aux_queue.remove()

    def get_min(self):
        return self.aux_queue.get(self.size - 1)

    # ------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------

    def __str__(self):
        out = [" MinQueue ".center(40, "=")]
        out.append(f"MainQueue: {self.main_queue.a}")
        out.append(f"AuxQueue: {self.aux_queue.a}")
        out.append(f"Size: {self.size}")
        out.append(f"Min: {self.get_min()}")
        return "\n".join(out)
