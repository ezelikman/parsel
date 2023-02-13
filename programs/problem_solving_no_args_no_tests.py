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
# given a list of lists representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city, return a new cost matrix with a new node corresponding to the sky.
def add_sky_node(cost_matrix, airport_costs):
    # First, add the new row and column representing the sky node
    for row in cost_matrix:
        row.append(0)
    cost_matrix.append([0]*len(cost_matrix[0]))
    # Now add the costs of the airports to the new row and column
    for i in range(len(airport_costs)):
        cost_matrix[i][-1] = airport_costs[i]
        cost_matrix[-1][i] = airport_costs[i]
    # Return the new cost matrix
    return cost_matrix

# given a list of lists representing the cost of each edge, return an adjacency matrix corresponding to the minimum spanning true. all entries in the adjacency matrix should be 0 or 1.
def min_spanning_tree(cost_matrix):
    n = len(cost_matrix)
    if n == 0:
        return []
    m = len(cost_matrix[0])
    if n != m:
        raise Exception("The cost matrix is not symmetric")
    adjacency_matrix = [[0] * n for i in range(n)]
    # Start with the first vertex.
    visited = [0]
    while len(visited) < n:
        min_cost = sys.maxsize
        min_edge = None
        for vertex in visited:
            for i in range(n):
                if i in visited:
                    continue
                if cost_matrix[vertex][i] < min_cost:
                    min_cost = cost_matrix[vertex][i]
                    min_edge = (vertex, i)
        adjacency_matrix[min_edge[0]][min_edge[1]] = 1
        adjacency_matrix[min_edge[1]][min_edge[0]] = 1
        visited.append(min_edge[1])
    return adjacency_matrix

# given a list of lists representing an adjacency matrix without self-loops, return a list of the nodes connected to the final node. However, if only one node is connected to the final node, return an empty list.
def find_connected_cities(adj_matrix):
    # YOUR CODE HERE
    finalNode = len(adj_matrix)
    lastRow = adj_matrix[finalNode-1]
    count = 0
    connectedCities = []
    for i in range(0, len(lastRow)):
        if lastRow[i] == 1:
            connectedCities.append(i)
            count += 1
    if count == 1:
        return []
    else:
        return connectedCities

# given a matrix representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city (where any two cities with airports are connected), return a list of the cities that should have airports built in them to minimize the total cost of building roads and airports such that all cities are connected. The list should be sorted in ascending order.
def min_cost_airports(cost_matrix, airport_costs):
    cost_matrix = add_sky_node(cost_matrix, airport_costs)
    adj_matrix = min_spanning_tree(cost_matrix)
    connected_cities = find_connected_cities(adj_matrix)
    return connected_cities


assert find_connected_cities([[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]]) == []
assert find_connected_cities([[0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0]]) == [0, 1, 2]
assert find_connected_cities([[0,1],[0,1],[1,0],[1,0],[0,0]]) == []
assert find_connected_cities([[0, 1, 0], [0, 0, 1], [1, 0, 0]]) == []
assert find_connected_cities([[0,1,1],[1,0,1],[1,1,0]]) == [0, 1]
assert find_connected_cities([[0,1],[1,0]]) == []
assert find_connected_cities([[0, 0, 1], [0, 0, 1], [1, 1, 0]]) == [0, 1]
assert find_connected_cities([[False, True, True], [True, False, False], [True, False, False]]) == []
assert find_connected_cities([[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,0,0]]) == [], "Test #1"
assert find_connected_cities([[False, True, False, True], [True, False, True, False], [False, True, False, True], [True, False, True, False]]) == [0, 2]
assert find_connected_cities([[0, 1, 1], [0, 0, 1], [1, 1, 0]]) == [0, 1]
assert find_connected_cities([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]) == []
assert find_connected_cities([[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]]) == [1,2]
assert find_connected_cities([[0, 1, 1],[1, 0, 1],[1, 1, 0]]) == [0, 1]
assert find_connected_cities([[0,1,1,0], [1,0,0,1], [1,0,0,1], [0,1,1,0]]) == [1,2]
assert min_spanning_tree([[0, 2, 3], [2, 0, 6], [3, 6, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert min_spanning_tree([[0, 1, 2], [1, 0, 1], [2, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert min_spanning_tree([[0, 1, 3, 1000], [1, 0, 1, 4], [3, 1, 0, 2], [1000, 4, 2, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert min_spanning_tree([[0, 1, 3], [1, 0, 1], [3, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert min_spanning_tree([[0, 1, 3, 5], [1, 0, 2, 4], [3, 2, 0, 1], [5, 4, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert min_spanning_tree([[0, 2, 5], [2, 0, 1], [5, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert min_spanning_tree([[0, 2, 5], [2, 0, 3], [5, 3, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert min_cost_airports([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [1, 1, 1, 1]) == []
assert min_cost_airports([[0, 1, 2, 4], [1, 0, 1, 3], [2, 1, 0, 2], [4, 3, 2, 0]], [3, 1, 2, 0]) == [1, 3]
assert min_cost_airports([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 1]) == []
assert min_cost_airports([[0, 2, 2], [2, 0, 2], [2, 2, 0]], [1, 2, 1]) == [0, 2]
assert min_cost_airports([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [0, 0, 0, 0]) == []
assert add_sky_node([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [1, 1, 1]) == [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
assert add_sky_node([[0, 1, 2], [3, 0, 4], [5, 6, 0]], [1, 1, 1]) == [[0, 1, 2, 1], [3, 0, 4, 1], [5, 6, 0, 1], [1, 1, 1, 0]]
assert add_sky_node([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [5, 1, 2]) == [[0, 1, 2, 5], [1, 0, 3, 1], [2, 3, 0, 2], [5, 1, 2, 0]]
assert add_sky_node([[0, 1, 2], [2, 0, 3], [4, 3, 0]], [1, 1, 1]) == [[0, 1, 2, 1], [2, 0, 3, 1], [4, 3, 0, 1], [1, 1, 1, 0]]
assert add_sky_node([[0, 1, 3], [1, 0, 4], [3, 4, 0]], [5, 6, 7]) == [[0, 1, 3, 5], [1, 0, 4, 6], [3, 4, 0, 7], [5, 6, 7, 0]]
assert add_sky_node([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [0, 1, 2]) == [[0, 1, 2, 0], [1, 0, 3, 1], [2, 3, 0, 2], [0, 1, 2, 0]]
assert add_sky_node([[0,1,2],[1,0,1],[2,1,0]], [0,1,2]) == [[0,1,2,0],[1,0,1,1],[2,1,0,2],[0,1,2,0]]
assert add_sky_node([[0, 10, 20], [10, 0, 30], [20, 30, 0]], [100, 200, 300]) == [[0, 10, 20, 100], [10, 0, 30, 200], [20, 30, 0, 300], [100, 200, 300, 0]]
assert add_sky_node([[0, 10], [10, 0]], [5, 5]) == [[0, 10, 5], [10, 0, 5], [5, 5, 0]]
assert add_sky_node([[0, 2, 5], [2, 0, 3], [5, 3, 0]], [1, 3, 2]) == [[0, 2, 5, 1], [2, 0, 3, 3], [5, 3, 0, 2], [1, 3, 2, 0]]