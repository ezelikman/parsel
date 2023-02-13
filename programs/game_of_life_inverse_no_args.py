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
# Takes a board with active and inactive cells as a list of lists and returns the next iteration of the game of life
def next_board(board):
    # 1) Create a new, empty board that is the same size as the old one
    new_board = []
    for i in range(len(board)):
        new_board.append([])
        for j in range(len(board[i])):
            new_board[i].append(0)
    # 2) Iterate over the old board and determine the new state of each cell using the rules of the game of life
    for i in range(len(board)):
        for j in range(len(board[i])):
            # Determine the number of active cells in the neighbourhood
            live_neighbours = 0
            for x in range(i-1, i+2):
                for y in range(j-1, j+2):
                    # Check that the indices are valid
                    if x>=0 and y>=0 and x<len(board) and y<len(board[i]):
                        # Check that the cell is not the current cell
                        if not (x==i and y==j):
                            # Check that the cell is active
                            if board[x][y]==1:
                                live_neighbours += 1
            # Apply the rules of the game of life
            if board[i][j]==1 and live_neighbours==2:
                new_board[i][j] = 1
            elif board[i][j]==1 and live_neighbours==3:
                new_board[i][j] = 1
            elif board[i][j]==0 and live_neighbours==3:
                new_board[i][j] = 1
    # 3) Return the new board
    return new_board
    
# Invert a square array by flipping 0's and 1's
def invert_square_array(arr):
    # For every row in the array
    for row in range(len(arr)):
        # For every column in the row
        for col in range(len(arr[row])):
            # Invert the value at the location
            if arr[row][col] == 0:
                arr[row][col] = 1
            else:
                arr[row][col] = 0
    return arr

# Takes a board and returns the next iteration of the game of life, but with all values flipped
def invert_board(board):
    return invert_square_array(next_board(board))


assert repr(str(invert_board([[0, 0, 1], [1, 0, 0], [1, 0, 0]]))) == repr(str([[1, 1, 1], [1, 0, 1], [1, 1, 1]])) or (invert_board([[0, 0, 1], [1, 0, 0], [1, 0, 0]]) == [[1, 1, 1], [1, 0, 1], [1, 1, 1]])
assert repr(str(invert_board([[0, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]))) == repr(str([[1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]])) or (invert_board([[0, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]) == [[1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]])


