from typing import Any, Optional
import copy

class Node:

    def __init__(self, x:Any):
        self.x = x
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

# ------------------------------------------

class DLList:
    """
    Attributes
    ----------
    n : int, number of Nodes
    dummy : Node, helps wrapping all nodes into a cycle.

    Theorem
    -------
    A DLList implements the List interface.
    In this implementation, the get(i), set(i, x), add(i, x) and
    remove(i) operations run in O(1 +min{i, n - i}) time per operation.

    It is worth noting that, if we ignore the cost of the get node(i)
    operation, then all operations on a DLList take constant time. Thus,
    the only expensive part of operations on a DLList is finding the
    relevant node. Once we have the relevant node, adding, removing,
    or accessing the data at that node takes only constant time.

    """

    def __init__(self):
        self.n = 0
        self.dummy = Node(None)
        self.dummy.prev = self.dummy
        self.dummy.next = self.dummy

    def get(self, i):
        return self._get_node(i).x

    def set(self, i:int, x:Any):
        u = self._get_node(i)
        y = u.x
        u.x = x
        return y

    def add(self, i:int, x:Any):
        self._add_before(self._get_node(i), x)

    def remove(self, i:int):
        self._remove(self._get_node(i))

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _get_node(self, i:int):
        if i < self.n // 2:
            p = self.dummy.next
            for _ in range(i):
                p = p.next
        else:
            p = self.dummy
            for _ in range(self.n - i):
                p = p.prev
        return p

    def _remove(self, w:Node):
        w.prev.next = w.next
        w.next.prev = w.prev
        self.n -= 1


    def _add_before(self, w:Node, x:Any):
        u = self._new_node(x)
        u.prev = w.prev
        u.next = w
        u.next.prev = u
        u.prev.next = u
        self.n += 1
        return u

    def _new_node(self, x:Any):
        return Node(x)

    def _get_next_item(self):
        b = copy.deepcopy(self)
        head = b.dummy.next

        for _ in range(self.n):
            yield head.x

            head = head.next

    def __str__(self):
        header = "=== Double Linked List ==="
        n = f"n : {self.n}"
        gen = self._get_next_item()

        head_str = f"HEAD: {next(gen)}"
        nodes = [item for item in list(gen)]
        nodes_str = "node: " + "\nnode: ".join(nodes[:-1])
        tail_str = f"TAIL: {nodes[-1]}"

        return "\n".join([header, n, head_str, nodes_str, tail_str])
