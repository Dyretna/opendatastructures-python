"""
Source of what implementations are tested against what contract.

1.  At lowest level we do basic invariance tests (size, empty, etc)

2.  At next level, we test basic list and set operations (set is upcoming)
    List tests are split into deque and index operations in testing,
    Some implementations are only pure deque implementations, for example
    the 'OrderedDeque'.

3.  at next level we run tests specific to each implementation.
    Some implementations only have tests at this level, for
    example 'BoundedDeque' and others that use it as underlying structure,
    for example the SEList and SEDeque.

"""

from ods.arrays import (
    ArrayDeque,
    ArrayQueue,
    ArrayStack,
    DualArrayDeque,
    ImprovedRAS,
    MinDeque,
    MinQueue,
    MinStack,
    NoModDeque,
    OrderedDeque,
    RootishArrayStack,
    Treque,
)
from ods.linked import DLList, SLList
from ods.skip_list import SkiplistList

# add_first/add_last/remove_first/remove_last
# test_deque_ops.py
DEQUE_IMPLS = [
    # arrays
    ArrayStack,
    ArrayDeque,
    DualArrayDeque,
    MinDeque,
    NoModDeque,
    OrderedDeque,
    RootishArrayStack,
    ImprovedRAS,
    Treque,
    # linked
    SLList,
    DLList,
    # skiplist
    SkiplistList,
]

# get/set/add/remove
# test_index_ops.py
INDEX_IMPLS = [
    # arrays
    ArrayStack,
    ArrayDeque,
    DualArrayDeque,
    NoModDeque,
    RootishArrayStack,
    ImprovedRAS,
    Treque,
    # linked
    SLList,
    # skiplist
    SkiplistList,
]

# add/remove
QUEUE_IMPLS = [
    ArrayQueue,
    MinQueue,
]

# push/pop
STACK_IMPLS = [
    ArrayStack,
    MinStack,
]

# minimal base contract: size/is_empty + facades.
# test_invariants.py
ALL_IMPLS = sorted(
    {*DEQUE_IMPLS, *INDEX_IMPLS, *QUEUE_IMPLS, *STACK_IMPLS}, key=lambda c: c.__name__
)
