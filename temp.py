class ArrayDeque:
    def __init__(self, array:list = []):
        self.a = [e for e in array if e is not None]
        self.n = len(self.a)
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



class TreQueue:
    def __init__(self):
        self.left  = ArrayDeque()
        self.mid   = ArrayDeque()
        self.right = ArrayDeque()

    def set(self, i:int, x:Any) -> None:
        block, idx = self._get_block_and_idx(i)
        block.set(idx, x)

    def get(self, i:int) -> Any:
        block, idx = self._get_block_and_idx(i)
        return block.get(idx)

    def add(self, i:int, x:Any) -> None:
        block, idx = self._get_block_and_idx(i, adding=True)
        block.add(idx, x)
        self.balance()

    def remove(self, i:int) -> Any:
        block, idx = self._get_block_and_idx(i)
        x = block.remove(idx)
        self.balance()
        return x

    def balance(self):
        biggest = max([self.left.n, self.mid.n, self.right.n])
        smallest = min([self.left.n, self.mid.n, self.right.n])
        # biggest must be bigger than 3 to balance
        if not biggest > max([3, smallest * 3]):
            return

        ordered_c = self._get_ordered_collection()
        new_block_len = len(ordered_c) // 3
        print("1/3 of ordered len: ", new_block_len)

        self.left = ArrayDeque()
        self.mid = ArrayDeque()
        self.right = ArrayDeque()

        self.left.add_all(0, ordered_c[:new_block_len])
        self.mid.add_all(0, ordered_c[new_block_len:new_block_len*2])
        self.right.add_all(0, ordered_c[new_block_len*2:])

    # --------------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------------

    def _get_block_and_idx(self, i, adding:bool = False):
        self._validate_i(i, adding=adding)
        if not all([self.left.n, self.mid.n, self.right.n]):
            if not self.left.n:
                return self.left, i
            elif not self.mid.n:
                return self.mid, i
            else:
                return self.right, i

        if i <= self.left.n - 1:
            return self.left, i
        elif i <= self.left.n + self.mid.n - 1:
            return self.mid,  i - self.left.n
        else:
            return self.right, i - (self.left.n + self.mid.n)

    def _validate_i(self, i:int, adding:bool = False):
        i_end = (self.left.n + self.mid.n + self.right.n) - 1
        if adding:
            i_end += 1
        if i_end < 0:
            raise ValueError("Container has no values!")
        if not 0 <= i <= i_end:
            raise IndexError(f"Index must be in range: 0 - {i_end}, got {i}")

    def _get_ordered_collection(self):
        ordered_c = []
        for block in [self.left, self.mid, self.right]:
            for k in range(block.n):
                ordered_c.extend(block.a[(block.j + k) % len(block.a)])

        return ordered_c

    def __str__(self):
        return f"{self._get_ordered_collection()}"
