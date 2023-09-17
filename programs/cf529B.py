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
# Splits l on space, converts each element to int, and returns the result of converting the result to a list.

def parse_line(l):
    return list(map(int, l.split()))

# Takes the input line and first splits on newline. Ignores the first line, and parses each of the remaining lines as a list of two numbers, which give a list L of lists. Returns L.
def parse_input(input_string):
    lines = input_string.split("\n")[1:]
    return [list(map(int, parse_line(line))) for line in lines if line]
# recusively enumerates the subsets of size k of the list L. Base cases: if k = 0, returns a list containing the empty list. If k > len(L), returns the empty list. Otherwise, first construct the subsets that contain the first element, then those that do not, and return their concatenation.
def enumerate_subsets(L, k):
    if k == 0:
        return [[]]
    elif k > len(L):
        return []
    else:
        subsets_with_first = [[L[0]] + subset for subset in enumerate_subsets(L[1:], k-1)]
        subsets_without_first = enumerate_subsets(L[1:], k)
        return subsets_with_first + subsets_without_first
# Returns all subsets of L with sizes ranging from 0 to k, inclusive.
def enumerate_subsets_at_most_k(L, k):
    subsets = []
    for i in range(k+1):
        subsets += enumerate_subsets(L, i)
    return subsets
# takes a list of pairs (width, height). Computes the sum of the widths and the maximum of the heights. Returns the product of those two numbers.

def compute_area(whs):
    sum_widths = sum([wh[0] for wh in whs])
    max_height = max([wh[1] for wh in whs])
    return sum_widths * max_height

# Takes a list of pairs of form [w, h] and a subset of indices to invert. Returns a list where the elements of whs whose index is in the subset are inverted to [h, w], and the others appear as given.

def apply_inversions(whs, subset):
    for i in subset:
        whs[i] = [whs[i][1], whs[i][0]]
    return whs

# First, calls enumerate_subsets_at_most_k passing integer list range from 0 to whs length and half the length of whs rounded down. Returns the minimum result of calling compute_area on the list given by apply_inversions with whs and of the subset.
def minimum_area(whs):
    k = len(whs) // 2
    subsets = enumerate_subsets_at_most_k(list(range(len(whs))), k)
    min_area = float('inf')
    for subset in subsets:
        inverted_whs = apply_inversions(whs, subset)
        area = compute_area(inverted_whs)
        if area < min_area:
            min_area = area
    return min_area
# Parses the input str to L and returns the minimum area of L. You should only call parse_input and minimum_area which have been implemented. You shouln't redefine them.
def main(input_string):
    L = parse_input(input_string)
    return minimum_area(L)

assert repr(str(main("3\n10 1\n20 2\n30 3"))) == repr(str(180)) or (main("3\n10 1\n20 2\n30 3") == 180)
assert repr(str(main("3\n3 1\n2 2\n4 3"))) == repr(str(21)) or (main("3\n3 1\n2 2\n4 3") == 21)

assert repr(str(parse_input("3\n10 1\n20 2\n30 3"))) == repr(str([[10, 1], [20, 2], [30, 3]])) or (parse_input("3\n10 1\n20 2\n30 3") == [[10, 1], [20, 2], [30, 3]])

assert repr(str(enumerate_subsets_at_most_k([1, 2, 3], 2))) == repr(str([[], [1], [2], [3], [1, 2], [1, 3], [2, 3]])) or (enumerate_subsets_at_most_k([1, 2, 3], 2) == [[], [1], [2], [3], [1, 2], [1, 3], [2, 3]])

assert repr(str(minimum_area([[10, 1], [20, 2], [30, 3]]))) == repr(str(180)) or (minimum_area([[10, 1], [20, 2], [30, 3]]) == 180)
assert repr(str(minimum_area([[3, 1], [2, 2], [4, 3]]))) == repr(str(21)) or (minimum_area([[3, 1], [2, 2], [4, 3]]) == 21)

assert repr(str(parse_line("10 1"))) == repr(str([10, 1])) or (parse_line("10 1") == [10, 1])

assert repr(str(enumerate_subsets([1, 2, 3], 2))) == repr(str([[1, 2], [1, 3], [2, 3]])) or (enumerate_subsets([1, 2, 3], 2) == [[1, 2], [1, 3], [2, 3]])

assert repr(str(compute_area([[1, 2], [3, 5]]))) == repr(str(20)) or (compute_area([[1, 2], [3, 5]]) == 20)
assert repr(str(compute_area([[10, 1], [20, 2], [30, 3]]))) == repr(str(180)) or (compute_area([[10, 1], [20, 2], [30, 3]]) == 180)

assert repr(str(apply_inversions([[1, 2], [3, 5]], [1]))) == repr(str([[1, 2], [5, 3]])) or (apply_inversions([[1, 2], [3, 5]], [1]) == [[1, 2], [5, 3]])
assert repr(str(apply_inversions([[1, 2], [3, 5]], []))) == repr(str([[1, 2], [3, 5]])) or (apply_inversions([[1, 2], [3, 5]], []) == [[1, 2], [3, 5]])
