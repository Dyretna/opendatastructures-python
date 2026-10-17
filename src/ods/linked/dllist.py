import copy
from typing import Any, Optional


class Node:
    def __init__(self, x: Any):
        self.x = x
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

    def reverse(self):
        pass


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

    def get(self, i) -> Any:
        return self._get_node(i).x

    def set(self, i: int, x: Any):
        u = self._get_node(i)
        y = u.x
        u.x = x
        return y

    def add(self, i: int, x: Any):
        self._add_before(self._get_node(i), x)

    def append(self, node: Node):
        if not isinstance(node, Node):
            raise TypeError("Argument must of Node type (DLL)")
        if self.n == 0:
            self.dummy.next = node
            self.dummy.prev = node
            node.next = self.dummy
            node.prev = self.dummy
        else:
            last_n = self.dummy.prev
            last_n.next = node
            node.next = self.dummy
            self.dummy.prev = node

        self.n += 1

    def remove(self, i: int) -> Any:
        removed_node = self._remove_node(self._get_node(i))
        return removed_node.x

    # -----------------------------------------------
    # special methods
    # ----------------------------------------------

    def create_from_nodes(self, n: int, start_node: Node) -> "DLList":
        """
        Creates a new DLL from a chain of nodes.
        Starting Node should be a dummy.

        """
        if not isinstance(n, int):
            raise TypeError("arg - 'n' is not int!")
        if not isinstance(start_node, Node):
            raise TypeError("arg - 'dummy' is not Node!")

        new_inst = DLList()
        new_inst.n = n
        new_inst.dummy = start_node

        new_inst.check_size()

        return new_inst

    def check_size(self) -> None:
        """Raises AssertionError"""
        head = self.dummy.next

        i = 0
        while head != self.dummy:
            head = head.next
            i += 1

        if not i == self.n:
            raise AssertionError(
                f"Size of n: {self.n} is not equal to number of Nodes: {i}"
            )

    def is_palindrome(self) -> bool:
        head = self.dummy.next
        tail = self.dummy.prev

        while head != tail and head != tail.next:
            if head.x != tail.x:
                return False
            head = head.next
            tail = tail.prev

        return True

    def rotate(self, r: int):
        if r == 0:
            return
        elif r > 0:
            i = r
        else:
            i = self.n + r
        head = self._get_node(i)

        self._remove_node(self.dummy)
        self.dummy = self._add_before(head, None)

    def truncate(self, i: int) -> "DLList":
        t_node = self._get_node(i)
        new_dummy = self._add_before(t_node, None)

        temp_last = new_dummy.prev

        # Loop the new DLL
        new_dummy.prev = self.dummy.prev
        new_dummy.prev.next = new_dummy

        # loop the original truncated
        temp_last.next = self.dummy
        self.dummy.prev = temp_last

        old_n = self.n
        self.n = i

        return self.create_from_nodes(old_n - i - 1, new_dummy)

    def deal(self) -> "DLList":
        new_dll = DLList()
        head = self.dummy.next.next

        while head != self.dummy and head.prev != self.dummy:
            nxt = head.next.next
            new_dll.append(self._remove_node(head))
            head = nxt

        return new_dll

    def reverse(self):
        if self.n <= 1:
            return

        current = self.dummy.next

        while current != self.dummy:
            next_temp = current.next
            current.next = current.prev
            current.prev = next_temp
            current = next_temp

        self.dummy.next, self.dummy.prev = self.dummy.prev, self.dummy.next

    # -------------------------------------------------
    # Merge-sort methods...
    # -------------------------------------------------

    def absorb(self, l2: "DLList"):
        while l2.n:
            self.take_first(l2)

    def take_first(self, l2: "DLList"):
        if l2.n == 0:
            raise IndexError("DLL l2 cannot be empty")

        self.append(l2._remove_node(l2.dummy.next))

    @staticmethod
    def merge(l1: "DLList", l2: "DLList") -> "DLList":
        """
        Takes two sorted lists l1 and l2, merges them, and returns a new
        sorted list containing the result. This causes l1 and l2 to be emptied
        in the process. For example, if l1 contains a, c, d and l2 contains
        b, e, f, then this methods returns a new list containing a, b, c, d,
        e, f.

        merge(a0, a1, a)
            i0 ← i1 ← 0
            for i in 0, 1, 2, . . . , length(a) - 1 do
                if i0 = length(a0) then
                    a[i] ← a1[i1]
                    i1 ← i2
                else if i1 = length(a1)
                    a[i] ← a0[i0]
                    i0 ← i1
                else if a0[i0] ≤ a1[i1]
                    a[i] ← a0[i0]
                    i0 ← i1
                else
                    a[i] ← a1[i1]
                    i1 ← i2
        """
        pass

    def sort(self):
        if self.n <= 1:
            return self

        pass

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _get_node(self, i: int) -> Node:
        if i < self.n // 2:
            p = self.dummy.next
            for _ in range(i):
                p = p.next
        else:
            p = self.dummy
            for _ in range(self.n - i):
                p = p.prev
        return p

    def _remove_node(self, w: Node) -> Node:
        w.prev.next = w.next
        w.next.prev = w.prev
        self.n -= 1

        return w

    def _add_before(self, w: Node, x: Any) -> Node:
        u = self._new_node(x)
        u.prev = w.prev
        u.next = w
        u.next.prev = u
        u.prev.next = u
        self.n += 1
        return u

    def _new_node(self, x: Any) -> Node:
        return Node(x)

    def _get_next_item(self) -> Any:
        b = copy.deepcopy(self)
        head = b.dummy.next

        for _ in range(self.n):
            yield head.x

            head = head.next

    def __str__(self) -> str:
        header = "\n" + " Double Linked List ".center(50, "=")
        n = f"n : {self.n}"

        if self.n == 0:
            return header + "\nEmpty..."

        gen = self._get_next_item()
        nodes = [str(item) for item in list(gen)]
        nodes_str = "node: " + "\nnode: ".join(nodes)

        return "\n".join([header, n, nodes_str])
