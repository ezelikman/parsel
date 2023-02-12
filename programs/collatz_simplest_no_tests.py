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
        return collatz_recursion(num / 2, cur_list)
    else:
        return collatz_recursion(3 * num + 1, cur_list)

# Calls base_case if 1, otherwise recursion_rule
def collatz_recursion(num, cur_list=None):
    if cur_list is None:
        return collatz_recursion(num, [])
    else:
        return base_case(num, cur_list) if num == 1 else recursion_rule(num, cur_list)


assert base_case(2, []) == [2]
assert base_case(1, []) == [1]
assert base_case(0, []) == [0], "base_case incorrect"
assert base_case(2, [1]) == [1, 2]
assert base_case(10, [1, 2, 3]) == [1, 2, 3, 10]
assert base_case(1, []) == [1],         "The base_case is incorrect"
assert base_case(4, []) == [4]
assert base_case(5, [2,2,2]) == [2,2,2,5]
assert base_case(1, [0]) == [0, 1]
assert base_case(0, []) == [0], 'base_case(0, []) should return [0]'
assert base_case(1, [1]) == [1, 1]
assert base_case(2, [1]) == [1, 2], "base_case is not correct"
assert base_case(2, []) == [2], 'error1'
assert base_case(1, [1, 2, 3]) == [1, 2, 3, 1]
assert base_case(3, []) == [3]
assert base_case(0, []) == [0]
assert base_case(5, []) == [5]
assert base_case(1, []) == [1], 'base_case is incorrect'
assert base_case(5, [1,2,3,4]) == [1,2,3,4,5], 'base_case should return [1,2,3,4,5]'
assert collatz_recursion(3) == [3, 10, 5, 16, 8, 4, 2, 1]
assert collatz_recursion(1) == [1], "collatz_recursion is incorrect"
assert collatz_recursion(1, [1]) == [1, 1]
assert collatz_recursion(1) == [1], f"collatz_recursion(1) should return [1]"
assert collatz_recursion(5) == [5, 16, 8, 4, 2, 1]
assert collatz_recursion(2) == [2, 1]
assert collatz_recursion(9) == [9, 28, 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
assert [1] == collatz_recursion(1)
assert collatz_recursion(1) == [1]
assert collatz_recursion(1, []) == [1]
assert recursion_rule(5, []) == [5, 16, 8, 4, 2, 1]
assert recursion_rule(5, []) == [5, 16, 8, 4, 2, 1], "recursion_rule incorrect"
assert recursion_rule(3, [1]) == [1, 3, 10, 5, 16, 8, 4, 2, 1]
assert recursion_rule(5, []) == [5, 16, 8, 4, 2, 1], 'incorrect recursion rule'
assert recursion_rule(4, []) == [4, 2, 1]
assert recursion_rule(2, []) == [2, 1], 'recursion_rule(2, []) should return [2, 1]'
assert recursion_rule(3, []) == [3, 10, 5, 16, 8, 4, 2, 1]
assert recursion_rule(3, []) == [3, 10, 5, 16, 8, 4, 2, 1] # odd
assert recursion_rule(7, []) == [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
assert recursion_rule(2, []) == [2, 1]
assert recursion_rule(5, []) == [5, 16, 8, 4, 2, 1], 'recursion_rule does not work correctly'
assert recursion_rule(6, []) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
assert recursion_rule(3, [1, 2]) == [1, 2, 3, 10, 5, 16, 8, 4, 2, 1]
assert recursion_rule(2, [1]) == [1, 2, 1]
assert recursion_rule(11, []) == [11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]