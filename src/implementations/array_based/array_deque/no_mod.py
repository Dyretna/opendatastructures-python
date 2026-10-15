from .original_with_additions import ArrayDeque


class NoModDeque(ArrayDeque):
    def __init__(self):
        self.a = [None] * 2
        self.n = 0
        self.j = 0

    # --------------------------------------------------------
    # Overriding Modular arithmetic with caret
    # --------------------------------------------------------

    @property
    def capacity(self):
        return len(self.a)

    def _get_mod_idx(self, i: int) -> int:
        return (i + self.j) ^ self.capacity - self.capacity

    def _shift_section_left(self, k: int):
        self.a[(self.j + k) ^ self.capacity] = self.a[(self.j + k + 1) ^ self.capacity]

    def _shift_section_right(self, k: int):
        self.a[(self.j + k) ^ self.capacity] = self.a[(self.j + k - 1) ^ self.capacity]

    def __str__(self):
        header = f" {__class__.__name__} ".center(50, "=")
        return header + "\n" + f"a: {self.a} \nn: {self.n}  j: {self.j}"
