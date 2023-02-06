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
def sky_city_cost(city_road_cost, city_airport_cost):
    # add a new node for the sky city
    sky_city_cost = [[0 for i in range(len(city_road_cost) + 1)] for j in range(len(city_road_cost) + 1)]
    for i in range(len(city_road_cost)):
        for j in range(len(city_road_cost)):
            sky_city_cost[i][j] = city_road_cost[i][j]
    for i in range(len(city_road_cost)):
        sky_city_cost[i][-1] = city_airport_cost[i]
        sky_city_cost[-1][i] = city_airport_cost[i]
    return sky_city_cost


# given a list of lists representing the cost of each edge, return an adjacency matrix corresponding to the minimum spanning true. all entries in the adjacency matrix should be 0 or 1.
def minimum_spanning_tree(cost_matrix):
    n = len(cost_matrix)
    # initialize adjacency matrix to 0
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # initialize set S to contain node 0
    S = {0}
    # initialize set T to be all the other nodes
    T = set(range(1,n))
    
    # for each node, find the minimum cost edge connecting that node to S
    # if there is no such edge, pick any edge connecting to S
    while len(T) > 0:
        best_cost = float('inf')
        best_edge = None
        for i in range(n):
            for j in range(n):
                if i in S and j in T and cost_matrix[i][j] < best_cost:
                    best_cost = cost_matrix[i][j]
                    best_edge = (i,j)
        if best_edge is None:
            # no edges left
            break
        i,j = best_edge
        adj_matrix[i][j] = 1
        adj_matrix[j][i] = 1
        S.add(j)
        T.remove(j)
    return adj_matrix

# given a list of lists representing an adjacency matrix, return a list of the nodes connected to the final node. However, if only one node is connected to the final node, return an empty list.
def final_node_connectors(adjacency_matrix):
    node_connectors = []
    for i in range(len(adjacency_matrix)):
        if adjacency_matrix[len(adjacency_matrix) - 1][i] == 1:
            node_connectors.append(i)
    if len(node_connectors) == 1:
        node_connectors = []
    return node_connectors

# given a matrix representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city (where any two cities with airports are connected), return a list of the cities that should have airports built in them to minimize the total cost of building roads and airports such that all cities are connected. The list should be sorted in ascending order.
def select_airport_cities(city_road_cost, city_airport_cost):
    cost_matrix = sky_city_cost(city_road_cost, city_airport_cost)
    tree = minimum_spanning_tree(cost_matrix)
    return sorted(final_node_connectors(tree))


assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [1, 1, 1, 1]) == []
assert select_airport_cities([[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]], [0, 0, 0, 0]) == [0, 1, 2, 3]
assert select_airport_cities([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [3, 2, 1]) == []
assert select_airport_cities([[0, 1], [1, 0]], [1, 1]) == []
assert select_airport_cities([[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]], [1, 2, 3, 4]) == []
assert select_airport_cities([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 1]) == []
assert select_airport_cities([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [1, 1, 1]) == []
assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [0, 1, 1, 1]) == []
assert select_airport_cities([[0, 3, 3], [3, 0, 3], [3, 3, 0]], [0, 1, 2]) == [0, 1, 2]
assert select_airport_cities([[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]], [1, 1, 1, 1]) == []
assert select_airport_cities([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [0, 0, 0, 0, 0]) == []
assert select_airport_cities([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]], [0,1,1,1,1]) == []
assert select_airport_cities([[0, 1, 2, 1], [1, 0, 2, 1], [2, 2, 0, 1], [1, 1, 1, 0]], [2, 1, 0, 3]) == [1, 2]
assert select_airport_cities([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]], [5,5,5,5,5]) == []
assert select_airport_cities([[0, 100, 100, 100], [100, 0, 100, 100], [100, 100, 0, 100], [100, 100, 100, 0]], [100, 100, 100, 100]) == []
assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [.25, .25, .25, .25]) == [0, 1, 2, 3]
assert select_airport_cities([[0, 5, 4], [5, 0, 3], [4, 3, 0]], [7, 8, 5]) == []
assert select_airport_cities([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [1, 1, 1]) == []
assert select_airport_cities([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [1, 2, 3]) == []
assert select_airport_cities([[0, 1, 3], [1, 0, 1], [3, 1, 0]], [2, 1, 0]) == []
assert select_airport_cities([[0, 0, 1], [0, 0, 1], [1, 1, 0]], [1, 1, 1]) == []
assert sky_city_cost([[0, 2, 3],[3, 0, 2],[3, 2, 0]], [1, 2, 3]) == [[0, 2, 3, 1], [3, 0, 2, 2], [3, 2, 0, 3], [1, 2, 3, 0]]
assert sky_city_cost([[0,1,3],[1,0,5],[3,5,0]], [2,2,2]) == [[0,1,3,2],[1,0,5,2],[3,5,0,2],[2,2,2,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [10, 10, 10]) == [[0, 1, 2, 10], [1, 0, 1, 10], [2, 1, 0, 10], [10, 10, 10, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [3, 3, 3]) == [[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]]
assert sky_city_cost([[0, 5, 4], [5, 0, 3], [4, 3, 0]], [5, 6, 4]) == [[0, 5, 4, 5], [5, 0, 3, 6], [4, 3, 0, 4], [5, 6, 4, 0]]
assert (sky_city_cost([[0,5,5],[5,0,5],[5,5,0]], [10,10,10]) == [[0,5,5,10],[5,0,5,10],[5,5,0,10],[10,10,10,0]])
assert sky_city_cost([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [100, 200, 300]) == [[0, 1, 2, 100], [1, 0, 2, 200], [2, 2, 0, 300], [100, 200, 300, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [3, 2, 1]) == [[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [10, 20, 30]) == [[0, 1, 2, 10], [1, 0, 3, 20], [2, 3, 0, 30], [10, 20, 30, 0]]
assert sky_city_cost([[0,2,3],[2,0,1],[3,1,0]], [0,1,2]) == [[0,2,3,0], [2,0,1,1], [3,1,0,2], [0,1,2,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [1, 2, 3]) == [[0, 1, 2, 1], [1, 0, 2, 2], [2, 2, 0, 3], [1, 2, 3, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [4, 5, 6]) == [[0, 1, 2, 4], [1, 0, 3, 5], [2, 3, 0, 6], [4, 5, 6, 0]]
assert sky_city_cost([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [1, 1, 1]) == [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [5, 6, 7]) == [[0, 1, 2, 5], [1, 0, 3, 6], [2, 3, 0, 7], [5, 6, 7, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [2, 3, 4]) == [[0, 1, 2, 2], [1, 0, 3, 3], [2, 3, 0, 4], [2, 3, 4, 0]]
assert sky_city_cost([[0,1,5], [1,0,2], [5,2,0]], [3,1,2]) == [[0, 1, 5, 3], [1, 0, 2, 1], [5, 2, 0, 2], [3, 1, 2, 0]]
assert sky_city_cost([[0, 10, 20], [10, 0, 15], [20, 15, 0]], [25, 30, 20]) == [[0, 10, 20, 25], [10, 0, 15, 30], [20, 15, 0, 20], [25, 30, 20, 0]]
assert sky_city_cost([[0,1,2],[1,0,2],[2,2,0]], [3,4,5]) == [[0,1,2,3],[1,0,2,4],[2,2,0,5],[3,4,5,0]]
assert sky_city_cost([[1, 2], [3, 4]], [5, 6]) == [[1, 2, 5], [3, 4, 6], [5, 6, 0]]
assert sky_city_cost([[0, 2, 1], [1, 0, 2], [2, 1, 0]], [0, 3, 2]) == [[0, 2, 1, 0], [1, 0, 2, 3], [2, 1, 0, 2], [0, 3, 2, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [1, 3, 3]) == [[0, 1, 2, 1], [1, 0, 3, 3], [2, 3, 0, 3], [1, 3, 3, 0]]
assert final_node_connectors([[0, 1, 0], [0, 0, 1], [0, 0, 0]]) == []
assert final_node_connectors([[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,1,0]]) == []
assert final_node_connectors([[0,1],[0,0]]) == [], 'incorrect'
assert final_node_connectors([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) == []
assert final_node_connectors([[0, 1, 1, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]) == []
assert final_node_connectors([[0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]) == []
assert final_node_connectors([[0,0,0,1,0],[0,0,0,0,0],[0,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0]]) == []
assert final_node_connectors([[1,1,0,0],[0,0,1,1],[0,0,0,1],[1,1,0,0]]) == [0,1]
assert final_node_connectors([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]) == []
assert final_node_connectors([[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == []
assert final_node_connectors([[0,1],[1,0]]) == []
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0]]) == [0, 1, 2, 3, 4]
assert final_node_connectors([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == [], "incorrect output"
assert final_node_connectors([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]) == []
assert final_node_connectors([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == []
assert final_node_connectors([[0,0,0],[0,0,0],[0,0,0]]) == []
assert final_node_connectors([[0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]) == []
assert final_node_connectors([[0,1,1],[1,0,1],[1,1,0]]) == [0,1]
assert final_node_connectors([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]) == [1, 2]
assert final_node_connectors([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]) == [] # only one node connected to the final node, so the answer is an empty list
assert final_node_connectors([[0, 1], [1, 0]]) == []
assert final_node_connectors([[0, 1, 0], [0, 0, 1], [1, 0, 0]]) == []
assert final_node_connectors([[0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]) == []
assert final_node_connectors([[0, 1], [1, 0]]) == [], 'test 1'
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0]]) == []
assert final_node_connectors([[0,0,0,0],[0,0,1,1],[0,1,0,0],[0,1,0,0]]) == []
assert final_node_connectors([[0,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]) == []
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]) == [], 'incorrect'
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 5], [3, 1, 0, 2], [100, 5, 2, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 2], [1, 0, 1], [2, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 3], [1, 0, 2], [3, 2, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 3], [2, 0, 1], [3, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 5], [2, 0, 3], [5, 3, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 2], [3, 1, 0, 1], [100, 2, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 1, 4], [2, 0, 4, 1], [1, 4, 0, 2], [4, 1, 2, 0]]) == [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 3, 1000], [1, 0, 1, 3], [3, 1, 0, 1], [1000, 3, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]], 'incorrect answer'
assert minimum_spanning_tree([]) == []
assert minimum_spanning_tree([[0,1],[1,0]]) == [[0,1],[1,0]]
assert minimum_spanning_tree([[0,1,3],[1,0,2],[3,2,0]]) == [[0,1,0],[1,0,1],[0,1,0]]
assert minimum_spanning_tree([[0, 1, 1], [1, 0, 1], [1, 1, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 3], [1, 0, 1], [3, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0,2,3],[2,0,1],[3,1,0]]) == [[0,1,0],[1,0,1],[0,1,0]]
assert minimum_spanning_tree([[0, 1, 2], [1, 0, 2], [2, 2, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 3, 4], [1, 0, 1, 2], [3, 1, 0, 1], [4, 2, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 5, 1], [2, 0, 3, 2], [5, 3, 0, 4], [1, 2, 4, 0]]) == [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
assert minimum_spanning_tree([[0, 2, 1], [2, 0, 3], [1, 3, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 3], [3, 1, 0, 1], [100, 3, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]



