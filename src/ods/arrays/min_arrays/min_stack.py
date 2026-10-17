from typing import Any

from ..array_stack import ArrayStack


class MinStack:
    def __init__(self):
        self.main_stack = ArrayStack()
        self.aux_stack = ArrayStack()

    def push(self, x: Any):
        self.main_stack.add(self.size(), x)

        if self.size() == 0:
            self.aux_stack.add(self.size(), x)
        elif x >= self.aux_stack.get(self.size() - 1):
            self.aux_stack.add(self.size(), self.aux_stack.get(self.size() - 1))
        else:
            self.aux_stack.add(self.size(), x)

    def pop(self) -> Any:
        self.main_stack.remove(self.size() - 1)
        self.aux_stack.remove(self.size() - 1)

    def size(self):
        return self.aux_stack.n

    def get_min(self):
        return self.aux_stack.get(self.size() - 1)

    # ------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------

    def __str__(self):
        out = [" MinStack ".center(40, "=")]
        out.append(f"MainStack: {self.main_stack.a}")
        out.append(f"AuxStack: {self.aux_stack.a}")
        out.append(f"Size: {self.size()}")
        out.append(f"Min: {self.get_min()}")
        return "\n".join(out)
