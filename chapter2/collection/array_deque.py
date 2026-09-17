import copy

class ArrayDeque:
    def __init__(self):
        self.a = []
        self.n = 0
        self.j = 0

    def get(self, i):
        return self.a[(i + self.j) % len(self.a)]

    def set(self, i, x):
        y = copy.copy(self.a[(i + self.j) % len(self.a)])
        self.a[(i + self.j) % len(self.a)] = x
        return y

    def add(self, i, x):
        if self.n == len(self.a):
            self.resize()

        if i < self.n / 2:
            self.j = (self.j-1) % len(self.a)
            for k in range(i):
                self.shift_left(k)
        else:
            for k in range(self.n, i, -1):
                self.shift_right(k)

        self.a[(self.j + i) % len(self.a)] = x
        self.n += 1

    def add_all(self, i:int, c:list):
        m = len(c)
        if m == 0:
            return

        # ensure capacity
        if self.n + m > len(self.a):
            new_capacity = max(1, 2*(self.n + m))
            b = [None] * new_capacity

            # copy left part
            for j in range(i):
                b[j] = self.a[j]

            # copy c
            for j in range(m):
                b[i + j] = c[j]

            # copy right part
            for j in range(i, self.n):
                b[j + m] = self.a[j]

            self.a = b
            self.n += m
            return

        # enough space: shift right
        # backwards to not overwrite data
        for j in range(self.n - 1, i - 1, -1):
            self.a[j + m] = self.a[j]

        # insert c
        for j in range(m):
            self.a[i + j] = c[j]

        self.n += m


    def remove(self, i):
        x = self.a[(self.j + i) % len(self.a)]

        if i < self.n / 2:
            # left-side
            for k in range(i, 0, -1):
                self.shift_right(k)
            self.a[self.j] = None
            self.j = (self.j + 1) % len(self.a)
        else:
            #right-side
            for k in range(i, self.n - 1):
                self.shift_left(k)

        self.n -= 1

        if len(self.a) >= 3*self.n:
            self.resize()

        return x

    def shift_left(self, k):
        self.a[(self.j + k) % len(self.a)] = \
            self.a[(self.j + k + 1) % len(self.a)]

    def shift_right(self, k):
        self.a[(self.j + k) % len(self.a)] = \
            self.a[(self.j + k - 1) % len(self.a)]

    def resize(self):
        b = [None] * max(1, 2*self.n)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % len(self.a)]
        self.a = b
        self.j = 0