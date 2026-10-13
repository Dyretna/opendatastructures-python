from typing import Any, Optional

from ..array_based import BoundedDeque


class Node:
    def __init__(self, block_size: int):
        self.d = BoundedDeque(block_size)
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


# ------------------------------------------


class SELDeque:
    """
    Version of an SEList that supports all the Deque operations
    in constant amortized time per operation, independent of
    the value of b.

    """

    def __init__(self, block_size: int = 8):
        self.n = 0
        self.b = block_size  # BDeque has + 1 empty space

        self.dummy = Node(self.b)
        self.dummy.prev = self.dummy
        self.dummy.next = self.dummy

    def get_first(self):
        u = self.dummy.next
        return u.d.get(0)

    def get_last(self):
        u = self.dummy.prev
        return u.d.get(0)

    def add_first(self, x: Any):
        first = self.dummy.next
        if first == self.dummy or first.d.size() == self.b:
            first = self._add_before(self.dummy.next)
        first.d.add_first(x)
        self.n += 1

    def add_last(self, x: Any):
        last = self.dummy.prev
        if last == self.dummy or last.d.size() == self.b:
            last = self._add_before(self.dummy)
        last.d.add_last(x)
        self.n += 1

    def pop_first(self) -> Any:
        first = self.dummy.next

        if first is self.dummy:
            raise Exception("SEL is empty")

        x = first.d.pop_first()
        if first.d.size() == 0:
            self._remove_node(first)

        self.n -= 1
        return x

    def pop_last(self) -> Any:
        last = self.dummy.prev

        if last is self.dummy:
            raise Exception("SEL is empty")

        x = last.d.pop_last()
        if last.d.size() == 0:
            self._remove_node(last)

        self.n -= 1
        return x

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _new_node(self) -> Node:
        return Node(self.b)

    def _remove_node(self, w: Node):
        w.prev.next = w.next
        w.next.prev = w.prev

    def _add_before(self, w: Node) -> Node:
        u = self._new_node()
        u.prev = w.prev
        u.next = w
        u.next.prev = u
        u.prev.next = u
        return u

    # ---------------------------------------------
    # str... when testing
    # ---------------------------------------------

    def __str__(self):
        out = []
        out.append("\n" + " Space Efficient Linked Deque ".center(50, "="))
        out.append(f"n : {self.n}")

        u = self.dummy.next
        while u != self.dummy:
            block = []
            for raw_idx in range(u.d.n):
                block.append(u.d.get(raw_idx))
            empty_slots = [None] * (u.d.capacity - u.d.n)
            out.append("node: " + str(block + empty_slots))
            u = u.next

        return "\n".join(out)
