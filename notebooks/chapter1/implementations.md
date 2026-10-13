# Table 1.1: Summary of List and USet implementations.

| Implementation      | get(i)/set(i,x)              | add(i,x)/remove(i)                  | Section |
|---------------------|------------------------------|-------------------------------------|---------|
| ArrayStack          | O(1)                         | O(1 + n - i)^A                      | § 2.1   |
| ArrayDeque          | O(1)                         | O(1 + min{i, n - i})^A              | § 2.4   |
| DualArrayDeque      | O(1)                         | O(1 + min{i, n - i})^A              | § 2.5   |
| RootishArrayStack   | O(1)                         | O(1 + n - i)^A                      | § 2.6   |
| DLList              | O(1 + min{i, n - i})         | O(1 + min{i, n - i})                | § 3.2   |
| SEList              | O(1 + min{i, n - i}/b)       | O(b + min{i, n - i}/b)^A            | § 3.3   |
| SkiplistList        | O(log n)^E                   | O(log n)^E                          | § 4.3   |

| Implementation      | find(x)                      | add(x)/remove(x)                    | Section |
|---------------------|------------------------------|-------------------------------------|---------|
| ChainedHashTable    | O(1)^E                       | O(1)^A,E                            | § 5.1   |
| LinearHashTable     | O(1)^E                       | O(1)^A,E                            | § 5.2   |



# Table 1.2: Summary of SSet and priority Queue implementations.


| SSet implementations | find(x)            | add(x)/remove(x)        | Section |
|----------------------|--------------------|-------------------------|---------|
| SkiplistSSet         | O(log n)^E         | O(log n)^E              | § 4.2   |
| Treap                | O(log n)^E         | O(log n)^E              | § 7.2   |
| ScapegoatTree        | O(log n)           | O(log n)^A              | § 8.1   |
| RedBlackTree         | O(log n)           | O(log n)                | § 9.2   |
| BinaryTrie^I         | O(w)               | O(w)                    | § 13.1  |
| XFastTrie^I          | O(log w)^A,E       | O(w)^A,E                | § 13.2  |
| YFastTrie^I          | O(log w)^A,E       | O(log w)^A,E            | § 13.3  |

| (Priority) Queue implementations | find_min() | add(x)/remove(x) | Section |
|----------------------------------|------------|------------------|---------|
| BinaryHeap                       | O(1)       | O(log n)^A       | § 10.1  |
| MeldableHeap                     | O(1)       | O(log n)^E       | § 10.2  |
