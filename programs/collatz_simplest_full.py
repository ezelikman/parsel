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
        return collatz_recursion(3*num + 1, cur_list)
# Calls base_case if 1, otherwise recursion_rule
def collatz_recursion(num, cur_list=list()):
    if num == 1:
        return base_case(num, cur_list)
    else:
        cur_list.append(num)
        if num % 2 == 0:
            return collatz_recursion(num // 2, cur_list)
        else:
            return collatz_recursion(3 * num + 1, cur_list)

assert repr(str(collatz_recursion(19))) == repr(str([19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1])) or (collatz_recursion(19) == [19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1])

assert repr(str(base_case(1, [1, 2, 3]))) == repr(str([1, 2, 3, 1])) or (base_case(1, [1, 2, 3]) == [1, 2, 3, 1])

assert repr(str(recursion_rule(2, [1, 2, 3]))) == repr(str([1, 2, 3, 2, 1])) or (recursion_rule(2, [1, 2, 3]) == [1, 2, 3, 2, 1])
