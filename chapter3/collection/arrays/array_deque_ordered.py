
from typing import Any

class ArrayDequeOrdered:
    """
    We create an deque without a circular buffer, and
    instead add from middle towards both ends. when any end is
    reached, we call rebuild() to create a new deque.

        +-----------------+----------------+
        |  <- add left    |  add right ->  |
        +-----------------+----------------+

    """

    def __init__(self, min_capacity:int=8):
        self.min_capacity = min_capacity
        self.capacity = self.min_capacity

        # att init - they are inverted,
        # since they step inside add before adding.
        self.left_pointer = self.capacity // 2
        self.right_pointer = (self.capacity // 2) - 1

        self.a = [None] * self.capacity
        self.n = 0

    # -----------------------------------------------------------
    # Public Methods
    # -----------------------------------------------------------

    @ property
    def size(self):
        return self.n

    def add_left(self, x:Any):
        if self.left_pointer -1 < 0:
            self.rebuild(self.capacity * 2)
        self.left_pointer -= 1
        self.a[self.left_pointer] = x
        self.n += 1

    def add_right(self, x:Any):
        if self.right_pointer +1 >= len(self.a) -1:
            self.rebuild(self.capacity * 2)
        self.right_pointer += 1
        self.a[self.right_pointer] = x
        self.n += 1

    def pop_left(self) -> Any:
        if self.n == 0:
            raise IndexError("pop from empty deque")
        val = self.a[self.left_pointer]
        self.a[self.left_pointer] = None
        self.left_pointer += 1
        self.n -= 1

        if self.size <= self.capacity // 3:
            self.rebuild(self.capacity // 2)

        return val

    def pop_right(self) -> Any:
        if self.n == 0:
            raise IndexError("pop from empty deque")
        val = self.a[self.left_pointer]
        self.a[self.right_pointer] = None
        self.right_pointer -= 1
        self.n -= 1

        if self.size <= self.capacity // 3:
            self.rebuild(self.capacity // 2)

        return val

    def rebuild(self, new_capacity:int):
        b = [None] * new_capacity

        old_lp = self.left_pointer
        old_rp = self.right_pointer

        # we take a quarter of empty space before array start
        self.left_pointer = (new_capacity // 4) + 1
        self.right_pointer = self.left_pointer + self.n - 1

        b[self.left_pointer:self.right_pointer + 1] = self.a[old_lp:old_rp + 1]
        self.a = b
        self.capacity = new_capacity

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------


    def __str__(self):
        return (
            f"=== ArrayDequeOrdered ==="
            f"\n{self.a}"
            f"\nCapacity       : {self.capacity}"
            f"\nSize           : {self.size}"
            f"\nleft pointer   : {self.left_pointer}"
            f"\nright pointer  : {self.right_pointer}"
            "\n" + "-"*30
        )