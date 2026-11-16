from typing import Any, Iterable, Optional

from ..validation import Validator as Val


class Node:
    def __init__(self, x: Any):
        self.x = x
        self.next: Optional[Node] = None


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

    def __init__(self, array: Optional[Iterable] = None):
        self.n = 0
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.add_all(0, array)

    @property
    def size(self):
        return self.n

    def get(self, i: int):
        Val.validate_index_access(i, self.size)
        head = self.head
        head = self._traverse_steps(i)

        return head.x

    def set(self, i: int, x: Any) -> None:
        Val.validate_index_access(i, self.size)
        head = self.head
        head = self._traverse_steps(i)

        head.x = x

    def add(self, i: int, x: Any) -> Any:
        Val.validate_index_insert(i, self.size)

        u = self._new_node(x)

        # push / add_first
        if i == 0:
            u.next = self.head
            self.head = u
            if self.n == 0:
                self.tail = u

        # add_last
        elif i == self.n:
            self.tail.next = u
            self.tail = u

        else:
            head = self._traverse_steps(i - 1)
            u.next = head.next
            head.next = u

        self.n += 1
        return x

    def remove(self, i: int) -> Any:
        if self.n == 0:
            return None

        Val.validate_index_access(i, self.size)

        # remove first
        if i == 0:
            x = self.head.x
            self.head = self.head.next
            if self.n == 1:
                self.tail = None

        # pop / remove last
        elif i == self.n - 1:
            head = self._traverse_steps(i - 1)
            x = head.next.x
            head.next = None
            self.tail = head

        else:
            head = self._traverse_steps(i - 1)
            x = head.next.x
            head.next = head.next.next

        self.n -= 1
        return x

    def push(self, x: Any) -> Any:
        return self.add(0, x)

    def add_first(self, x: Any) -> Any:
        return self.add(0, x)

    def add_last(self, x: Any) -> Any:
        return self.add(self.n, x)

    def pop(self) -> Any:
        return self.remove(0)

    def remove_first(self) -> Any:
        return self.remove(0)

    def remove_last(self) -> Any:
        return self.remove(self.n - 1)

    # --------------------------------------
    # Additional Public Utilities
    # --------------------------------------

    def add_all(self, i: int, array: Iterable):
        if not array:
            return None

        for j, x in enumerate(array):
            self.add(i + j, x)

    def check_size(self) -> None:
        """Raises AssertionError"""
        head = self.head

        i = 0
        while head is not None:
            head = head.next
            i += 1

        if not i == self.n:
            raise AssertionError(
                f"Size of n: {self.n} is not equal to number of Nodes: {i}"
            )

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

    def to_list(self):
        return list(iter(self))

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.x
            node = node.next

    def __repr__(self):
        return f"{self.__class__.__name__}({self.to_list()})"

    def __str__(self):
        header = "\n" + " Single Linked List ".center(50, "=")
        n = f"n : {self.n}"
        if self.n == 0:
            return header + "\nEmpty..."

        gen = iter(self)
        head_str = f"HEAD: {next(gen)}"
        nodes = [str(x) for x in list(gen)]
        nodes_str = "node: " + "\nnode: ".join(nodes[:-1])
        tail_str = f"TAIL: {self.tail.x}"

        return "\n" + "\n".join([header, n, head_str, nodes_str, tail_str])

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
