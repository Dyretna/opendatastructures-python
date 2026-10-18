from typing import Any


class OrderedDeque:
    """
    We create an deque without a circular buffer, and
    instead add from middle towards both ends. when any end is
    reached, we call rebuild() to create a new deque.

    """

    def __init__(self, min_capacity: int = 8):
        self.min_capacity = min_capacity
        self.a = [None] * self.min_capacity

        self.block_start = None
        self.block_end = None
        self._initialize_block()
        self.n = 0

    # ------------------------------------------------------
    # Abstract interface requirements
    # + convenience methods and properties
    # + get and set
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
        return self.a[self.block_start + i]

    def set(self, i: int, x: Any):
        y = self.a[self.block_start + i]
        self.a[self.block_start + i] = x
        return y

    def add_first(self, x: Any):
        if self.size == 0:
            self.a[self.block_start] = x
            self.n += 1
            return

        if self.block_start - 1 < 0:
            self._rebuild(self.capacity * 2)

        self.block_start -= 1
        self.a[self.block_start] = x
        self.n += 1

    def add_last(self, x: Any):
        if self.size == 0:
            self.a[self.block_start] = x
            self.n += 1
            return

        if self.block_end + 1 >= len(self.a) - 1:
            self._rebuild(self.capacity * 2)

        self.block_end += 1
        self.a[self.block_end] = x
        self.n += 1

    def remove_first(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty deque")

        x = self.a[self.block_start]
        self.a[self.block_start] = None
        self.block_start += 1
        self.n -= 1

        if self.size == 0:
            self._initialize_block()
        if self.size <= self.capacity // 3 and self.capacity != self.min_capacity:
            self._rebuild(self.capacity // 2)

        return x

    def remove_last(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty deque")

        x = self.a[self.block_end]
        self.a[self.block_end] = None
        self.block_end -= 1
        self.n -= 1

        if self.size == 0:
            self._initialize_block()
        if self.size <= self.capacity // 3 and self.capacity != self.min_capacity:
            self._rebuild(self.capacity // 2)

        return x

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _rebuild(self, new_capacity: int):
        b = [None] * new_capacity

        old_lp = self.block_start
        old_rp = self.block_end

        # we take about a quarter of empty space before block start
        self.block_start = new_capacity // 2 - (self.size // 2) - 1
        self.block_end = self.block_start + self.n - 1

        b[self.block_start : self.block_end + 1] = self.a[old_lp : old_rp + 1]
        self.a = b

    def _initialize_block(self):
        # att init - block start and end has to have an offset,
        # since they step inside add before adding.
        self.block_start = self.capacity // 2 - 1
        self.block_end = self.block_start

    def __str__(self):
        out = [" ArrayDequeOrdered ".center(50, "=")]
        out.append(f"a: {self.a}")
        out.append(f"Capacity       : {self.capacity}")
        out.append(f"Size           : {self.size}")
        out.append(f"Block Start    : {self.block_start}")
        out.append(f"Block End      : {self.block_end}")
        return "\n" + "\n".join(out)
