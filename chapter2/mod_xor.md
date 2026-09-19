## Exercise 2.7. replace % with ^

Modify the ArrayDeque implementation so that it does not
use the mod operator (which is expensive on some systems). Instead, it
should make use of the fact that, if length(a) is a power of 2, then

        k mod length(a) = k ∧ (length(a) − 1) .

(Here, ∧ is the bitwise-and operator.)


```python
# has to have 2, 4, 8 etc elements
a = ["a", "b", "c", "d"]

for k in range(12):
    print(f"k = {k:^3} | "
          f"k % len(a) = {k % len(a):^3} | "
          f"k^(len(a)) {k^(len(a)):^3} | "
          f"is_eq: {k % len(a) == k^(len(a))}"
    )
```

### list size 4:

| k  | k % len(a) | k^(len(a)) | is_eq  |
|----|------------|------------|--------|
| 0  | 0          | 4          | False  |
| 1  | 1          | 5          | False  |
| 2  | 2          | 6          | False  |
| 3  | 3          | 7          | False  |
| 4  | 0          | 0          | True   |
| 5  | 1          | 1          | True   |
| 6  | 2          | 2          | True   |
| 7  | 3          | 3          | True   |
| 8  | 0          | 12         | False  |
| 9  | 1          | 13         | False  |
| 10 | 2          | 14         | False  |
| 11 | 3          | 15         | False  |




### Array size 8:
| k  | k % len(a) | k^(len(a)) | is_eq  |
|----|------------|------------|--------|
| 0  | 0          | 4          | False  |
| 1  | 1          | 5          | False  |
| 2  | 2          | 6          | False  |
| 3  | 3          | 7          | False  |
| 4  | 0          | 0          | True   |
| 5  | 1          | 1          | True   |
| 6  | 2          | 2          | True   |
| 7  | 3          | 3          | True   |
| 8  | 0          | 12         | False  |
| 9  | 1          | 13         | False  |


### Array size 16:
| k  | k % len(a) | k^(len(a)) | is_eq  |
|----|------------|------------|--------|
| 6  | 6          | 14         | False  |
| 7  | 7          | 15         | False  |
| 8  | 0          |  0         | True   |
| 9  | 1          |  1         | True   |
|10  | 2          |  2         | True   |
|11  | 3          |  3         | True   |
|12  | 4          |  4         | True   |
|13  | 5          |  5         | True   |
|14  | 6          |  6         | True   |
|15  | 7          |  7         | True   |
|16  | 0          | 24         | False  |


### Array size 32:
| k  | k % len(a) | k^(len(a)) | is_eq  |
|----|------------|------------|--------|
| 14 | 14         | 30         | False  |
| 15 | 15         | 31         | False  |
| 16 |  0         |  0         | True   |
| 17 |  1         |  1         | True   |
| 18 |  2         |  2         | True   |
| 19 |  3         |  3         | True   |
| 20 |  4         |  4         | True   |
| 21 |  5         |  5         | True   |
| 22 |  6         |  6         | True   |
| 23 |  7         |  7         | True   |
| 24 |  8         |  8         | True   |
| 25 |  9         |  9         | True   |
| 26 | 10         | 10         | True   |
| 27 | 11         | 11         | True   |
| 28 | 12         | 12         | True   |
| 29 | 13         | 13         | True   |
| 30 | 14         | 14         | True   |
| 31 | 15         | 15         | True   |
| 32 |  0         | 48         | False  |