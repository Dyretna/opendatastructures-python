from typing import Any


class ArrayQueue:
    """
    We use modulus on the length of array, which makes it circular
    in order to simulate an infinite array. var 'j' keeps track of
    the ofset from 0 to find the next element to remove.
    """

    def __init__(self):
        self.a = [None] * 4  # simulates infinite array with mod (%)
        self.j = 0  # keeps track of next element to remove
        self.n = 0

    # ------------------------------------------------------
    # Abstract interface requirements
    # + convenience methods and properties
    # ------------------------------------------------------

    @property
    def size(self):
        return self.n

    @property
    def capacity(self):
        return len(self.a)

    def is_empty(self):
        return self.n == 0

    def get(self, i: int):
        return self.a[(i + self.j) % len(self.a)]

    def set(self, i: int, x: Any):
        y = self.a[(i + self.j) % len(self.a)]
        self.a[(i + self.j) % len(self.a)] = x
        return y

    def add(self, x: Any):
        if self.n + 1 > len(self.a):
            self._resize()
        self.a[(self.j + self.n) % len(self.a)] = x
        self.n += 1
        return True

    def remove(self):
        if self.is_empty():
            raise IndexError("remove from empty Queue")

        x = self.a[self.j]
        self.j = (self.j + 1) % len(self.a)
        self.n -= 1
        self.a[self.j - 1] = None
        if len(self.a) >= 3 * self.n:
            self._resize()
        return x

    # ---------------------------------
    # internal helpers
    # ---------------------------------

    def _resize(self):
        b = [None] * max(1, 2 * self.n)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % len(self.a)]
        self.a = b
        self.j = 0

    def __str__(self):
        out = [f" {__class__.__name__} ".center(50, "=")]
        out.append(f"{self.a}")
        out.append(f"n: {self.n}, j: {self.j}")

        return "\n".join(out)
