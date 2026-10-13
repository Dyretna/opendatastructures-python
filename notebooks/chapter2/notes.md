# ideas on EvenFurtherImprovedRAS

## Idea 1. first bdeque with size of √n

### version 1.1: increase size of all blocks + 1, copy, then "pop-shift at ends"
main idea is that the size of the first array is √n, with the minimum of lets say 4. for example, we initialize ArrayStack with on Bdeque, with minimum size 4:
- [None, None, None, None]

when this is full, the next Bdeque has s capacity, of 5, then 6, and so on. when we have reached over 16 elements, that is the capacity of first Bdeque ** 2, then the first array grow to size 5.

So we could check if above is True, and make a call to _grow_first(). The implementation could mean that we have to copy (allowed?) the contents of the first deque to i new with its own size + 1, and then use "deque shifting" between blocks.

but then, the sizes of all consecive blocks needs to increase as well. So we reapeat the above (copy and grow) to all blocks? it seems very expensive...

### 1.2: copy not allowed - ordinary right index shift
if we cant copy, the alternitive is to exhaust, block number 2 using pop_right to the next block, and chain it to the end. This would be extremely expensive,
just like ordinary index shifting.


---

### Idea 2. ideas without a big first deque?
