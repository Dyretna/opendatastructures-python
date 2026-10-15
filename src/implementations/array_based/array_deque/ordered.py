from typing import Any


class OrderedDeque:
    """
    We create an deque without a circular buffer, and
    instead add from middle towards both ends. when any end is
    reached, we call rebuild() to create a new deque.


    """

    def __init__(self, min_capacity: int = 8):
        self.min_capacity = min_capacity
        self.capacity = None
        self.block_start = None
        self.block_end = None
        self._initialize_block()

        self.a = [None] * self.capacity
        self.n = 0

    # --------------------------------------------------------
    # Abstract interface requirements
    # --------------------------------------------------------

    @property
    def size(self):
        return self.n

    def add_first(self, x: Any):
        if self.block_start - 1 < 0:
            self._rebuild(self.capacity * 2)
        self.block_start -= 1
        self.a[self.block_start] = x
        self.n += 1

    def add_last(self, x: Any):
        if self.block_end + 1 >= len(self.a) - 1:
            self._rebuild(self.capacity * 2)
        self.block_end += 1
        self.a[self.block_end] = x
        self.n += 1

    def remove_first(self) -> Any:
        if self.n == 0:
            raise IndexError("pop from empty deque")
        val = self.a[self.block_start]
        self.a[self.block_start] = None
        self.block_start += 1
        self.n -= 1

        if self.size == 0:
            self._initialize_block()
        if self.size <= self.capacity // 3 and self.capacity != self.min_capacity:
            self._rebuild(self.capacity // 2)

        return val

    def remove_last(self) -> Any:
        if self.n == 0:
            raise IndexError("pop from empty deque")
        val = self.a[self.block_start]
        self.a[self.block_end] = None
        self.block_end -= 1
        self.n -= 1

        if self.size == 0:
            self._initialize_block()
        if self.size <= self.capacity // 3 and self.capacity != self.min_capacity:
            self._rebuild(self.capacity // 2)

        return val

    # --------------------------------------------------------
    # Additional public properties and methods
    # --------------------------------------------------------

    @property
    def capacity(self):
        return len(self.a)

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
        self.capacity = new_capacity

    def _initialize_block(self):
        # att init - block start and end has to have an offset,
        # since they step inside add before adding.
        self.capacity = self.min_capacity
        self.block_start = self.capacity // 2
        self.block_end = (self.capacity // 2) - 1

    def __str__(self):
        return (
            f"=== ArrayDequeOrdered ==="
            f"\n{self.a}"
            f"\nCapacity       : {self.capacity}"
            f"\nSize           : {self.size}"
            f"\nBlock Start    : {self.block_start}"
            f"\nBlock End      : {self.block_end}"
            "\n" + "-" * 30
        )
