import copy
from typing import Any, Optional


class Node:
    def __init__(self, x: Any):
        self.x = x
        self.next: Optional[Node] = None


# ------------------------------------------


class SLList:
    """
    Attributes
    ----------
    n : int, number of Nodes
    head : Optional[Node], first (left) node
    tail : Optional[Node], last (right) node

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

    def get(self, i: int):
        head = self.head
        self._validate_index(i)
        head = self._traverse_steps(i)

        return head.x

    def set(self, i: int, x: Any) -> None:
        head = self.head
        self._validate_index(i)
        head = self._traverse_steps(i)

        head.x = x

    def push(self, x: Any) -> Any:
        u = self._new_node(x)
        u.next = self.head
        self.head = u

        if self.n == 0:
            self.tail = u

        self.n += 1
        return x

    def append(self, x: Any) -> bool:
        u = self._new_node(x)
        if self.n == 0:
            self.head = u
        else:
            self.tail.next = u

        self.tail = u
        self.n += 1

        return True

    def add(self, i: int, x: Any) -> bool:
        self._validate_index(i, adding=True)

        if self.n == 0 or i == 0:
            self.push(x)
            return True

        if i == self.n:
            self.append(x)
            return True

        u = self._new_node(x)
        head = self._traverse_steps(i - 1)
        u.next = head.next
        head.next = u

        self.n += 1
        return True

    def pop(self) -> Any:
        if self.n == 0:
            return None
        x = self.head.x

        self.head = self.head.next
        self.n -= 1

        if self.n == 0:
            self.tail = None

        return x

    def remove(self, i: int) -> Any:
        self._validate_index(i)
        if self.n == 0:
            raise IndexError("Linked List it empty")
        elif i == 0:
            return self.pop()
        else:
            head = self._traverse_steps(i - 1)

        x = head.next.x
        head.next = head.next.next
        self.n -= 1

        return x

    def reverse(self) -> None:
        current = self.head
        prev = None

        # traverse all nodes in SLL
        while current is not None:
            # store next
            nxt = current.next

            # reverese current nodes next pointer
            current.next = prev

            # move pointers one position ahead
            prev = current
            current = nxt

        self.head, self.tail = self.tail, self.head

    def second_last(self) -> Any:
        head = self.head

        if head is None or head.next is None:
            return None

        while head.next.next is not None:
            head = head.next

        return head.x

    def check_size(self):
        head = self.head

        i = 0
        while head:
            head = head.next
            i += 1

        if not i == self.n:
            raise AssertionError("Size of n is not equal to number of Nodes")

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _traverse_steps(self, i: int) -> Node:
        head = self.head

        for i in range(i):
            head = head.next

        return head

    def _new_node(self, x: Any):
        return Node(x)

    def _validate_index(self, i: int, adding: bool = False):
        if adding:
            bounds = self.n
        else:
            bounds = self.n - 1

        if not 0 <= i <= bounds:
            raise IndexError(f"Out of bounds: i={i}. Stay in range: 0 - {bounds}")

    def _get_next_item(self):
        b = copy.deepcopy(self)

        while b.head:
            yield str(b.head.x)

            b.head = b.head.next

    def __str__(self):
        header = "\n" + " Single Linked List ".center(50, "=")
        n = f"n : {self.n}"
        if self.n == 0:
            return header + "\nEmpty..."

        gen = self._get_next_item()
        head_str = f"HEAD: {next(gen)}"
        nodes = [x for x in list(gen)]
        nodes_str = "node: " + "\nnode: ".join(nodes[:-1])
        tail_str = f"TAIL: {self.tail.x}"

        return "\n" + "\n".join([header, n, head_str, nodes_str, tail_str])
