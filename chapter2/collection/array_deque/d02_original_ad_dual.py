from ..array_stack import ArrayStack


class DualArrayDeque:
    def __init__(self):
        self.front = ArrayStack()
        self.back = ArrayStack()

    def size(self):
        return self.front.n + self.back.n

    def get(self, i):
        if i < self.front.n:
            return self.front.get(self.front.n - i - 1)
        else:
            return self.back.get(i - self.front.n)

    def set(self, i, x):
        if i < self.front.n:
            return self.front.set(self.front.n - i - 1, x)
        else:
            return self.back.set(i - self.front.n, x)

    def add(self, i, x):
        if i < self.front.n:
            self.front.add(self.front.n - i, x)
        else:
            self.back.add(i - self.front.n, x)
        self.balance()

    def remove(self, i):
        if i < self.front.n:
            x = self.front.remove(self.front.n - i - 1)
        else:
            x = self.back.remove(i - self.front.n)

        self.balance()
        return x

    def balance(self):
        n = self.size()
        mid = n // 2

        if (3 * self.front.n < self.back.n or
            3 * self.back.n < self.front.n):

            f = ArrayStack()
            for i in range(mid):
                f.add(i, self.get(mid - i - 1))

            b = ArrayStack()
            for i in range(n - mid):
                b.add(i, self.get(mid + i))

            self.front = f
            self.back = b
