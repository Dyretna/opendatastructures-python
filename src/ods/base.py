"""
base.py — contract-bearing base classes for all ODS implementations.

Directly ripped from PatMorins repo, with some small changes.
in BaseCollection:
  * size is a property, not a method.
  * added is_empty()

Note on Policies:
  * add(i, x), add_first, add_last          -> None
  * remove(i), remove_first, remove_last    -> x (the removed value)
  * remove on empty structure               -> IndexError
  * invalid index                           -> IndexError (negative indices not supported)
  * facades carry no error handling of their own -> edge cases live in add/remove
  * set(i, x)                               -> the OLD value
  * add(x) on sets                          -> bool (collection-style add)

"""


class BaseCollection(object):
    """Base class for everything"""

    def __init__(self):
        super(BaseCollection, self).__init__()
        self.n = 0

    @property
    def size(self):
        """This implementation works for almost every class in ODS"""
        return self.n

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __str__(self):
        return "[" + ",".join([str(x) for x in self]) + "]"

    def __repr__(self):
        return self.__class__.__name__ + "([" + ",".join([repr(x) for x in self]) + "])"


class BaseSet(BaseCollection):
    """Base class for Set implementations"""

    def __init__(self):
        super(BaseSet, self).__init__()

    def add_all(self, a):
        for x in a:
            self.add(x)

    def __contains__(self, x):
        return self.find(x) is not None

    def __eq__(self, a):
        if len(a) != len(self):
            return False
        for x in self:
            if x not in a:
                return False
        for x in a:
            if x not in self:
                return False
        return True

    def __ne__(self, a):
        return not self == a


class BaseList(BaseCollection):
    """Base class for List implementations"""

    def __init__(self):
        super(BaseList, self).__init__()

    def append(self, x):
        self.add(self.size, x)

    def add_all(self, iterable):
        for x in iterable:
            self.append(x)

    def clear(self):
        """This can be overridden with more efficient implementations"""
        while self.size > 0:
            self.remove(self.size - 1)

    def add_first(self, x):
        return self.add(0, x)

    def remove_first(self):
        return self.remove(0)

    def add_last(self, x):
        return self.add(self.size, x)

    def remove_last(self):
        return self.remove(self.size - 1)

    def insert(self, i, x):
        self.add(i, x)

    def __iter__(self):
        """This implementation is good enough for array-based lists"""
        for i in range(len(self)):
            yield (self.get(i))

    def to_list(self):
        return list(self)

    def __eq__(self, a):
        if len(a) != len(self):
            return False
        it1 = iter(a)
        it2 = iter(self)
        for i in range(len(a)):
            if it1.next() != it2.next():
                return False
        return True

    def __ne__(self, a):
        return not self == a

    def index(self, x):
        i = 0
        for y in self:
            if y == x:
                return i
            i += 1
        raise ValueError("%r is not in the list" % x)

    def remove_value(self, x):
        try:
            return self.remove(self.index(x))
        except ValueError:
            return False

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, i):
        self.remove(i)
