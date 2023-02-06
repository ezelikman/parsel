import sys
import time
import itertools
from itertools import accumulate, product, permutations, combinations
import collections
from collections import Counter, OrderedDict, deque, defaultdict, ChainMap
from functools import lru_cache
import math
from math import sqrt, sin, cos, tan, ceil, fabs, floor, gcd, exp, log, log2
import fractions
from typing import List, Tuple
import numpy as np
import random
import heapq
# Returns the list with the number appended to it
def base_case(num, cur_list):
    cur_list.append(num)
    return cur_list

# Add num to list, collatz with 3n + 1 if odd or n / 2 if even
def recursion_rule(num, cur_list):
    cur_list.append(num)
    if num % 2 == 0:
        return collatz_recursion(num // 2, cur_list)
    else:
        return collatz_recursion(3 * num + 1, cur_list)

# Calls base_case if 1, otherwise recursion_rule
def collatz_recursion(num, cur_list=list()):
    if num == 1:
        return base_case(num, cur_list)
    else:
        return recursion_rule(num, cur_list)


assert [1] == collatz_recursion(1)
assert collatz_recursion(3) == [3, 10, 5, 16, 8, 4, 2, 1], 'incorrect'
assert collatz_recursion(1) == base_case(1, list())
assert (collatz_recursion(3) == [3, 10, 5, 16, 8, 4, 2, 1])
assert collatz_recursion(1, [1]) == [1, 1], 'First Call'
assert collatz_recursion(5) == [5, 16, 8, 4, 2, 1]
assert collatz_recursion(1) == [1], "Test 1 Failed"
assert collatz_recursion(1) == [1]
assert collatz_recursion(4) == [4, 2, 1]
assert base_case(13, [0]) == [0, 13]
assert base_case(2, [2]) == [2, 2]
assert base_case(5, [1]) == [1, 5]
assert base_case(1, []) == [1], 'error in base_case'
assert base_case(3, []) == [3]
assert base_case(1, []) == [1]
assert base_case(10, [1, 2, 3]) == [1, 2, 3, 10], "base_case should return the list with the number appended to it."
assert base_case(1, []) == [1], 'base_case is incorrect'
assert base_case(5, [-1, 0, 1, 2]) == [-1, 0, 1, 2, 5]
assert base_case(1, [0]) == [0,1], "base_case is incorrect: got {}, expected {}".format(base_case(1, [0]), [0,1])
assert base_case(0, []) == [0]
assert ( base_case(2, []) == [2] )
assert base_case(0, []) == [0], "base_case failed"
assert base_case(5, []) == [5], 'base_case test 1'
assert base_case(1,[1]) == [1, 1], 'base_case is incorrect'
assert base_case(2, []) == [2], "Test Failed"
assert base_case(1, []) == [ 1 ]
assert [1] == base_case(1, [])
assert base_case(2,[]) == [2], f"base_case failed with input: {(2,[])}"
assert [0] == base_case(0, [])
assert base_case(1, [2, 3]) == [2, 3, 1]
assert base_case(2, []) == [2]
assert base_case(7, [3, 2, 1]) == [3, 2, 1, 7]
assert (recursion_rule(2, [1]) == [1, 2, 1])
assert recursion_rule(3, []) == [3, 10, 5, 16, 8, 4, 2, 1]
assert collatz_recursion(2) == [2, 1]
assert recursion_rule(2, list()) == [2, 1]
assert collatz_recursion(3) == [3, 10, 5, 16, 8, 4, 2, 1]
assert collatz_recursion(1) == [1]
assert recursion_rule(15, []) == [15, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1], "recursion_rule returns incorrect results"
assert recursion_rule(3, [1]) == [1, 3, 10, 5, 16, 8, 4, 2, 1]
assert recursion_rule(5, []) == [5, 16, 8, 4, 2, 1]


