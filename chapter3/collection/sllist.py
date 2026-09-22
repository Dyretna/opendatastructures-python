from typing import Any, Optional
import copy

class Node:

    def __init__(self, x:Any):
        self.item = x
        self.next: Optional[Node] = None

# ------------------------------------------

class SingleLinkedList:
    """
    Attributes
    ----------
    n : int, number of Nodes
    head : Optional[Node], first (left) node
    tail : Optional[Node], last (right) node

    Methods
    -------
    - stack operations - constant time:
        - push(x)
        - pop()

    - queue operations - constant time:
        - add(x)
        - remove()

    Theorem
    -------
    An SLList implements the Stack and (FIFO) Queue interfaces.
    The push(x), pop(), add(x) and remove() operations run in O(1) time per
    operation.

    An SLList nearly implements the full set of Deque operations. The
    only missing operation is removing from the tail of an SLList. Removing
    from the tail of an SLList is difficult because it requires updating the value
    of tail so that it points to the node w that precedes tail in the SLList; this
    is the node w such that w.next = tail. Unfortunately, the only way to get
    to w is by traversing the SLList starting at head and taking n - 2 steps.
    """

    def __init__(self):
        self.n = 0
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    # --------------------------------------
    # Stack Operations - Constant time
    # --------------------------------------
    def push(self, x:Any):
        u = self._new_node(x)
        u.next = self.head
        self.head = u

        if self.n == 0:
            self.tail = u

        self.n += 1
        return x

    def pop(self):
        if self.n == 0:
            return None
        x = self.head.item

        self.head = self.head.next
        self.n -= 1

        if self.n == 0:
            self.tail = None

        return x

    # --------------------------------------
    # Queue Operations (FIFO) - Constant time
    # --------------------------------------

    def remove(self):
        return self.pop()

    def add(self, x:Any):
        u = self._new_node(x)
        if self.n == 0:
            self.head = u
        else:
            self.tail.next = u

        self.tail = u
        self.n += 1

        return True

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _new_node(self, x:Any):
        return Node(x)

    def _get_next_item(self):
        b = copy.deepcopy(self)

        while b.head:
            yield b.head.item

            b.head = b.head.next

    def __str__(self):
        header = "=== Single Linked List ==="
        n = f"n : {self.n}"
        gen = self._get_next_item()

        head_str = f"HEAD: {next(gen)}"
        nodes = [item for item in list(gen)]
        nodes_str = "node: " + "\nnode: ".join(nodes[:-1])
        tail_str = f"TAIL: {nodes[-1]}"

        return "\n".join([header, n, head_str, nodes_str, tail_str])
