
from typing import Any

class ArrayDequeOrdered:
    """
    We create an deque without a circular buffer, and
    instead add from middle towards both ends. when any end is
    reached, we call rebuild() to create a new deque.

        +-----------------+----------------+
        |  <- add left    |  add right ->  |
        +-----------------+----------------+

    This makes sure we reach the amortised time complexity
    requirement. To speed up copying in rebuild, we will
    check options in itertools or other python builtins,
    but not 3rd party.
    """

    def __init__(self, min_size:int=8):
        self.min_size = min_size
        self.size = self.min_size

        self.middle = self.size // 2
        # att init - they are inverted,
        # since they step inside add before adding.
        self.left_pointer = self.middle
        self.right_pointer = self.middle -1

        self.a = [None] * self.min_size
        self.n = 0

    # -----------------------------------------------------------
    # Public Methods
    # -----------------------------------------------------------

    def add_left(self, x:Any):
        if self.left_pointer -1 < 0:
            self.rebuild()
        self.left_pointer -= 1
        self.a[self.left_pointer] = x
        self.n += 1

    def add_right(self, x:Any):
        if self.right_pointer +1 >= len(self.a) -1:
            self.rebuild()
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
        return val

    def pop_right(self) -> Any:
        if self.n == 0:
            raise IndexError("pop from empty deque")
        val = self.a[self.left_pointer]
        self.a[self.right_pointer] = None
        self.right_pointer -= 1
        self.n -= 1
        return val

    def rebuild(self):
        self.size *= 2
        b = [None] * self.size

        old_lp = self.left_pointer
        old_rp = self.right_pointer

        self.left_pointer = (self.size // 4) + 1
        self.right_pointer = self.left_pointer + self.n - 1

        b[self.left_pointer:self.right_pointer + 1] = self.a[old_lp:old_rp + 1]
        self.a = b

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------


    def __str__(self):
        return (
            f"=== ArrayDequeOrdered ==="
            f"\n{self.a}"
            f"\nDeque size     : {self.size}"
            f"\nMiddle         : {self.middle}"
            f"\nleft pointer   : {self.left_pointer}"
            f"\nright pointer  : {self.right_pointer}"
            f"\nn (elements)   : {self.n}"
            "\n" + "-"*30
        )