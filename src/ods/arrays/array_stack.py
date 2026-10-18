from typing import Any


class ArrayStack:
    def __init__(self):
        self.a = [None] * 4
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
        return self.a[i]

    def set(self, i: int, x: Any) -> Any:
        y = self.a[i]
        self.a[i] = x
        return y

    def push(self, x: Any):
        self.add(self.size, x)

    def pop(self):
        return self.remove(self.n - 1)

    # ------------------------------------------------------
    # additional methods - index ops, etc
    # -----------------------------------------------------

    def add(self, i: int, x: Any):
        if self.n == len(self.a):
            self._resize(max(4, len(self.a) * 2))

        # shift right: go backwards
        for j in range(self.n, i, -1):
            self.a[j] = self.a[j - 1]

        self.a[i] = x
        self.n += 1

    def remove(self, i: int):
        if self.is_empty():
            raise IndexError("remove from empty stack")
        x = self.a[i]

        # shift left
        for j in range(i, self.n - 1):
            self.a[j] = self.a[j + 1]

        # leave a None at the end
        self.a[self.n - 1] = None

        self.n -= 1

        self._maybe_shrink()

        return x

    def add_all(self, i: int, c: list):
        """inserts elements of an iterable in order at index."""
        m = len(c)
        if m == 0:
            return

        # ensure capacity
        if self.n + m > self.capacity:
            b = [None] * self._new_capacity(m)

            # copy left part
            for j in range(i):
                b[j] = self.a[j]

            # copy c
            for j in range(m):
                b[i + j] = c[j]

            # copy right part
            for j in range(i, self.n):
                b[j + m] = self.a[j]
            self.a = b
        else:
            # enough space: shift right
            # backwards to not overwrite data
            for j in range(self.n - 1, i - 1, -1):
                self.a[j + m] = self.a[j]

            # insert c
            for j in range(m):
                self.a[i + j] = c[j]

        self.n += m

    # ---------------------------------
    # internal helpers
    # ---------------------------------

    def _new_capacity(self, extra):
        cap = max(1, self.capacity)
        while self.n + extra > cap:
            cap *= 2
        return cap

    def _resize(self, new_capacity):
        b = [None] * new_capacity
        for j in range(self.n):
            b[j] = self.a[j]
        self.a = b

    def _maybe_shrink(self):
        if len(self.a) >= 4 and len(self.a) >= 3 * self.n:
            self._resize(len(self.a) // 2)

    def __str__(self):
        out = [f" {__class__.__name__} ".center(50, "=")]
        out.append(f"{self.a}")
        out.append(f"n: {self.n}")

        return "\n".join(out)
