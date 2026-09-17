import random
from math import ceil

class RandomQeue:
    def __init__(self):
        self.a = []
        self.n = 0

    def add(self, x):
        if self.n == len(self.a):
            self.resize()
        self.a[self.n] = x
        self.n += 1

    def remove(self):
        r = random.randrange(self.n)
        x = self.a[r]
        self.a[r] = self.a[self.n - 1]
        self.a[self.n - 1] = None
        self.n -= 1

        if self.n < ceil(len(self.a) / 3):
            self.resize()

        return x

    def resize(self):
        new = [None] * max(1, 2*self.n)
        for i in range(self.n):
            new[i] = self.a[i]
        self.a = new