class ArrayQeue:
    """
    We use modulus on the length of array, which makes it circular
    in order to simulate an infinite array. var 'j' keeps track of
    the ofset from 0 to find the next element to remove.
    """
    def __init__(self):
        self.a = [] # simulates infinite array with mod (%)
        self.j = 0  # keeps track of next element to remove
        self.n = 0

    def add(self, x):
        if self.n + 1 > len(self.a):
            self.resize()
        self.a[(self.j + self.n) % len(self.a)] = x
        self.n += 1
        return True

    def remove(self):
        x = self.a[self.j]
        self.j = (self.j + 1) % len(self.a)
        self.n -= 1
        self.a[self.j-1] = None
        if len(self.a) >= 3*self.n:
            self.resize()
        return x

    def resize(self):
        b = [None] * max(1, 2*self.n)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % len(self.a)]
        self.a = b
        self.j = 0
