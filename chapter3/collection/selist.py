from typing import Any, Optional
import copy

from .bounded_deque import BDeque



class Node:

    def __init__(self, block_size:int):
        self.d = BDeque(block_size + 1)
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

# ------------------------------------------

class SEList:
    """

    Theorem
    -------
    An SEList implements the List interface. Ignoring the cost
    of calls to spread(u) and gather(u), an SEList with block size b
    supports the operations

    - get(i) and set(i, x) in O(1 + min{i, n - i}/b) time per operation; and
    - add(i, x) and remove(i) in O(b + min{i, n - i}/b) time per operation.

    Furthermore, beginning with an empty SEList, any sequence of m
    add(i, x) and remove(i) operations results in a total of O(bm)
    time spent during all calls to spread(u) and gather(u).

    The space (measured in words)1 used by an SEList that stores n
    elements is n + O(b + n/b).

    """

    def __init__(self, block_size:int = 7):
        self.n = 0
        self.b = block_size # BDeque has + 1 empty space

        self.dummy = Node(self.b)
        self.dummy.prev = self.dummy
        self.dummy.next = self.dummy


    def get(self, i:int):
        u, j = self._get_location(i)
        return u.d.get(j)

    def set(self, i:int, x:Any):
        u, j = self._get_location(i)
        return u.d.set(j, x)

    def append(self, x:Any):
        last = self.dummy.prev
        if last == self.dummy or last.d.size() == self.b + 1:
            last = self._add_before(self.dummy)
        last.d.add_right(x)
        self.n += 1

    def add(self, i:int, x:Any):

        # 1. if we add to end - simply append
        if i == self.n:
            self.append(x)
            return

        u, j = self._get_location(i)
        r = 0 # number of steps
        w = u

        # we increment steps until its still lower than block-size
        # Node 'w' cannot be dummy (go over one lap)
        # We make sure the BDeques in Nodes are full (spare space covered)
        while (r < self.b and
               w != self.dummy and
               w.d.size() == self.b + 1):

            w = w.next
            r += 1

        # if more steps than size of blocks
        # we have to add a new node, and spread
        # elements to make space
        if r == self.b: # b blocks, each with b+1 elements
            self._spread(u)
            w = u

        if w == self.dummy: # ran off the end - add new node
            w = self._add_before(w)

        while w != u: # work backwards, shifting as we go
            w.d.add_left(w.prev.d.pop_right())
            w = w.prev

        w.d.add(j, x)
        self.n += 1

    def remove(self, i:int):
        u, j = self._get_location(i)
        y = u.d.get(j)
        w = u
        r = 0

        while (r < self.b and
               w != self.dummy and
               w.d.size() == self.b - 1):
            w = w.next
            r += 1

        # r number of steps equals block size
        # we gather elements, and delete empty node
        if r == self.b: # b blocks, each with b - 1 elements
            print("remove, calling gather")
            self._gather(u)
        u.d.remove(j)

        while (u.d.size() < self.b - 1 and
               u.next    != self.dummy):
            u.d.add_right(u.next.d.pop_left())
            u = u.next

        if u.d.size() == 0:
            print("remove, size is 0")
            self._remove_node(u)

        self.n -= 1
        return y


    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _get_location(self, i:int) -> tuple[Node, int]:
        if i < self.n // 2:
            u = self.dummy.next
            while i >= u.d.size():
                i = i - u.d.size()
                u = u.next
            return u, i

        else:
            u = self.dummy
            idx = self.n
            while i < idx:
                u = u.prev
                idx -= u.d.size()
        return u, i - idx

    def _new_node(self) -> Node:
        return Node(self.b)

    def _remove_node(self, w:Node):
        w.prev.next = w.next
        w.next.prev = w.prev

    def _add_before(self, w:Node) -> Node:
        u = self._new_node()
        u.prev = w.prev
        u.next = w
        u.next.prev = u
        u.prev.next = u
        return u

    def _spread(self, u:Node) -> None:
        w = u
        for _ in range(self.b - 1):
            w = w.next

        w = self._add_before(w)
        while w != u:
            while w.d.size() < self.b:
                w.d.add_left(w.prev.d.pop_right())
            w = w.prev

    def _gather(self, u:Node) -> None:
        w = u
        for _ in range(self.b - 2):
            while w.d.size() < self.b:
                w.d.add_right(w.next.d.pop_left())
            w = w.next
        self._remove_node(w)

    # ---------------------------------------------
    # str... when testing
    # ---------------------------------------------

    def __str__(self):
        out = []
        out.append("=== Space-Efficient Linked List ===")
        out.append(f"n : {self.n}")

        u = self.dummy.next
        while u != self.dummy:
            # visa hela blocket, inklusive None
            block = []
            for raw_idx in range(u.d.n):
                block.append(u.d.get(raw_idx))
            empty_slots = [None] * (u.d.capacity - u.d.n)
            out.append("node: " + str(block + empty_slots))
            u = u.next

        return "\n".join(out)
