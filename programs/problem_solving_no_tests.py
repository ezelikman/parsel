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
    assert len(city_road_cost) == len(city_airport_cost)
    num_cities = len(city_airport_cost)
    sky_city_cost = [[0] * (num_cities + 1) for _ in range(num_cities + 1)]
    for i in range(num_cities):
        for j in range(num_cities):
            sky_city_cost[i][j] = city_road_cost[i][j]
        sky_city_cost[i][num_cities] = city_airport_cost[i]
        sky_city_cost[num_cities][i] = city_airport_cost[i]
    return sky_city_cost

# given a list of lists representing the cost of each edge, return an adjacency matrix corresponding to the minimum spanning true. all entries in the adjacency matrix should be 0 or 1.
def minimum_spanning_tree(cost_matrix):
    '''
    You will have to implement this method.
    '''
    # First we need to initialize the graph
    num_vertices = len(cost_matrix)
    graph = [[0 for i in range(num_vertices)] for j in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            graph[i][j] = cost_matrix[i][j]
            graph[j][i] = cost_matrix[i][j]

    # Now we need to use Prim's algorithm to find the minimum spanning tree
    # We will start with vertex 0
    visited = [0]
    edges = []
    # We will keep track of the edges and the total cost
    total_cost = 0
    # We need to find the next vertex to visit
    while len(visited) < num_vertices:
        # We need to find the lowest cost edge
        lowest_cost = float("inf")
        lowest_vertex = None
        lowest_edge = None
        for vertex in visited:
            for i in range(num_vertices):
                if i not in visited and graph[vertex][i] < lowest_cost:
                    lowest_cost = graph[vertex][i]
                    lowest_vertex = i
                    lowest_edge = (vertex, i)
        # Now we can add the lowest cost edge to the tree
        visited.append(lowest_vertex)
        edges.append(lowest_edge)
        total_cost += lowest_cost

    # Now we need to return the adjacency matrix of the minimum spanning tree
    adjacency_matrix = [[0 for i in range(num_vertices)] for j in range(num_vertices)]
    for edge in edges:
        adjacency_matrix[edge[0]][edge[1]] = 1
        adjacency_matrix[edge[1]][edge[0]] = 1

    return adjacency_matrix

# given a list of lists representing an adjacency matrix, return a list of the nodes connected to the final node. However, if only one node is connected to the final node, return an empty list.
def final_node_connectors(adjacency_matrix):
    final_node_connectors = []
    for i in range(0, len(adjacency_matrix)):
        if adjacency_matrix[i][-1] == 1:
            final_node_connectors.append(i)
    if len(final_node_connectors) == 1:
        final_node_connectors = []
    return final_node_connectors
        
# given a matrix representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city (where any two cities with airports are connected), return a list of the cities that should have airports built in them to minimize the total cost of building roads and airports such that all cities are connected. The list should be sorted in ascending order.
def select_airport_cities(city_road_cost, city_airport_cost):
    # YOUR CODE GOES HERE
    new_cost_matrix = sky_city_cost(city_road_cost, city_airport_cost)
    adjacency_matrix = minimum_spanning_tree(new_cost_matrix)
    airport_cities = final_node_connectors(adjacency_matrix)
    airport_cities.sort()

    return airport_cities


assert minimum_spanning_tree([[0, 2, 1], [2, 0, 4], [1, 4, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([[0,1],[1,0]]) == [[0,1],[1,0]]
assert minimum_spanning_tree([[0, 1, 2], [1, 0, 1], [2, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0,2,4],[2,0,2],[4,2,0]]) == [[0,1,0],[1,0,1],[0,1,0]]
assert minimum_spanning_tree([[0,2,1],[2,0,3],[1,3,0]]) == [[0,1,1],[1,0,0],[1,0,0]]
assert minimum_spanning_tree([[0, 2, 5], [2, 0, 3], [5, 3, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 1], [2, 0, 2], [1, 2, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 3], [3, 1, 0, 1], [100, 3, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 3, 5], [1, 0, 1, 4], [3, 1, 0, 2], [5, 4, 2, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 3], [1, 0, 2], [3, 2, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert isinstance(minimum_spanning_tree([[0, 2, 1], [2, 0, 1], [1, 1, 0]]), list)
assert minimum_spanning_tree([[0, 2, 5], [2, 0, 1], [5, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 3], [2, 0, 1], [3, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 1, 4], [2, 0, 4, 1], [1, 4, 0, 2], [4, 1, 2, 0]]) == [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 1], [1, 0, 1], [1, 1, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([[0,2,3],[2,0,1],[3,1,0]]) == [[0,1,0],[1,0,1],[0,1,0]]
assert minimum_spanning_tree([[0, 1, 3], [1, 0, 1], [3, 1, 0]]) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 1, 3], [2, 0, 3, 1], [1, 3, 0, 2], [3, 1, 2, 0]]) == [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
assert minimum_spanning_tree([[0, 1, 3, 1000], [1, 0, 1, 3], [3, 1, 0, 1], [1000, 3, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]], 'incorrect answer'
assert minimum_spanning_tree([[0, 2, 5, 1], [2, 0, 3, 2], [5, 3, 0, 4], [1, 2, 4, 0]]) == [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
assert minimum_spanning_tree([[0, 1, 2], [1, 0, 2], [2, 2, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert minimum_spanning_tree([]) == []
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 2], [3, 1, 0, 1], [100, 2, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 100], [3, 1, 0, 1], [100, 100, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 1, 3, 4], [1, 0, 1, 2], [3, 1, 0, 1], [4, 2, 1, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0,1,3],[1,0,2],[3,2,0]]) == [[0,1,0],[1,0,1],[0,1,0]]
assert minimum_spanning_tree([[0, 1, 3, 100], [1, 0, 1, 5], [3, 1, 0, 2], [100, 5, 2, 0]]) == [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
assert minimum_spanning_tree([[0, 2, 1], [2, 0, 3], [1, 3, 0]]) == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
assert sky_city_cost([[0, 1], [1, 0]], [2, 3]) == [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [100, 200, 300]) == [[0, 1, 2, 100], [1, 0, 2, 200], [2, 2, 0, 300], [100, 200, 300, 0]]
assert sky_city_cost([[0, 1, 2],[1, 0, 2], [2, 2, 0]], [3, 4, 5]) == [[0, 1, 2, 3], [1, 0, 2, 4], [2, 2, 0, 5], [3, 4, 5, 0]]
assert sky_city_cost([[0,1,5], [1,0,2], [5,2,0]], [3,1,2]) == [[0, 1, 5, 3], [1, 0, 2, 1], [5, 2, 0, 2], [3, 1, 2, 0]]
assert sky_city_cost([[0,1,1], [1,0,1], [1,1,0]], [1,2,3]) == [[0,1,1,1], [1,0,1,2], [1,1,0,3], [1,2,3,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [10, 20, 30]) == [[0, 1, 2, 10], [1, 0, 3, 20], [2, 3, 0, 30], [10, 20, 30, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [1, 2, 3]) == [[0, 1, 2, 1], [1, 0, 1, 2], [2, 1, 0, 3], [1, 2, 3, 0]]
assert sky_city_cost([[0, 2, 3],[3, 0, 2],[3, 2, 0]], [1, 2, 3]) == [[0, 2, 3, 1], [3, 0, 2, 2], [3, 2, 0, 3], [1, 2, 3, 0]]
assert sky_city_cost([[1,4,5],[4,2,6],[5,6,3]], [10,5,7]) == [[1,4,5,10],[4,2,6,5],[5,6,3,7],[10,5,7,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [3, 2, 1]) == [[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]
assert sky_city_cost([[0,2,3],[2,0,1],[3,1,0]], [0,1,2]) == [[0,2,3,0], [2,0,1,1], [3,1,0,2], [0,1,2,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [5, 6, 7]) == [[0, 1, 2, 5], [1, 0, 3, 6], [2, 3, 0, 7], [5, 6, 7, 0]]
assert sky_city_cost([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [1, 1, 1]) == [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [4, 5, 6]) == [[0, 1, 2, 4], [1, 0, 3, 5], [2, 3, 0, 6], [4, 5, 6, 0]]
assert sky_city_cost([[0, 1, 2], [2, 0, 3], [4, 3, 0]], [1, 2, 3]) == [[0, 1, 2, 1], [2, 0, 3, 2], [4, 3, 0, 3], [1, 2, 3, 0]]
assert sky_city_cost([[0, 10, 10], [10, 0, 10], [10, 10, 0]], [50, 50, 50]) == [[0, 10, 10, 50], [10, 0, 10, 50], [10, 10, 0, 50], [50, 50, 50, 0]]
assert sky_city_cost([[0, 2, 1], [1, 0, 2], [2, 1, 0]], [0, 3, 2]) == [[0, 2, 1, 0], [1, 0, 2, 3], [2, 1, 0, 2], [0, 3, 2, 0]]
assert sky_city_cost([[0,5,5],[5,0,5],[5,5,0]], [10,10,10]) == [[0,5,5,10],[5,0,5,10],[5,5,0,10],[10,10,10,0]]
assert sky_city_cost([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [1, 2, 1]) == [[0, 1, 1, 1], [1, 0, 1, 2], [1, 1, 0, 1], [1, 2, 1, 0]]
assert sky_city_cost([[0,1,1],[1,0,1],[1,1,0]], [1,1,1]) == [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [2, 3, 4]) == [[0, 1, 2, 2], [1, 0, 3, 3], [2, 3, 0, 4], [2, 3, 4, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [1, 2, 3]) == [[0, 1, 2, 1], [1, 0, 2, 2], [2, 2, 0, 3], [1, 2, 3, 0]]
assert sky_city_cost([[0,1], [1,0]], [2,3]) == [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [3, 3, 3]) == [[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]]
assert sky_city_cost([[0, 5, 4], [5, 0, 3], [4, 3, 0]], [5, 6, 4]) == [[0, 5, 4, 5], [5, 0, 3, 6], [4, 3, 0, 4], [5, 6, 4, 0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [10, 10, 10]) == [[0, 1, 2, 10], [1, 0, 1, 10], [2, 1, 0, 10], [10, 10, 10, 0]]
assert sky_city_cost([[0, 1, 10], [1, 0, 10], [10, 10, 0]], [10, 20, 30]) == [[0, 1, 10, 10], [1, 0, 10, 20], [10, 10, 0, 30], [10, 20, 30, 0]]
assert sky_city_cost([[0,1,2],[1,0,3],[2,3,0]], [4,5,6]) == [[0,1,2,4],[1,0,3,5],[2,3,0,6],[4,5,6,0]]
assert sky_city_cost([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [1, 3, 3]) == [[0, 1, 2, 1], [1, 0, 3, 3], [2, 3, 0, 3], [1, 3, 3, 0]]
assert sky_city_cost([[0, 10, 20], [10, 0, 15], [20, 15, 0]], [25, 30, 20]) == [[0, 10, 20, 25], [10, 0, 15, 30], [20, 15, 0, 20], [25, 30, 20, 0]]
assert sky_city_cost([[1,2,3], [2,3,4], [3,4,5]], [1,2,3]) == [[1,2,3,1],[2,3,4,2],[3,4,5,3],[1,2,3,0]]
assert sky_city_cost([[2, 3], [4, 5]], [1, 2]) == [[2, 3, 1], [4, 5, 2], [1, 2, 0]]
assert sky_city_cost([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 2]) == [[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 2], [0, 1, 2, 0]]
assert sky_city_cost([[0,1,2],[1,0,2],[2,2,0]], [3,4,5]) == [[0,1,2,3],[1,0,2,4],[2,2,0,5],[3,4,5,0]]
assert sky_city_cost([[0, 3, 5], [3, 0, 1], [5, 1, 0]], [6, 2, 4]) == [[0, 3, 5, 6], [3, 0, 1, 2], [5, 1, 0, 4], [6, 2, 4, 0]]
assert sky_city_cost([[1, 2], [3, 4]], [5, 6]) == [[1, 2, 5], [3, 4, 6], [5, 6, 0]]
assert sky_city_cost([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 1]) == [[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]]
assert sky_city_cost([[0,1,2],[1,0,0],[2,0,0]], [4,4,4]) == [[0,1,2,4],[1,0,0,4],[2,0,0,4],[4,4,4,0]]
assert sky_city_cost([[0,1,3],[1,0,5],[3,5,0]], [2,2,2]) == [[0,1,3,2],[1,0,5,2],[3,5,0,2],[2,2,2,0]]
assert select_airport_cities([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [10, 11, 12]) == []
assert select_airport_cities([[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]], [1, 2, 3, 4]) == []
assert select_airport_cities([[0, 1, 2], [1, 0, 1], [2, 1, 0]], [1, 1, 1]) == []
assert select_airport_cities([[0, 1], [1, 0]], [1, 1]) == []
assert select_airport_cities([[0, 1, 5], [1, 0, 2], [5, 2, 0]], [2, 3, 1]) == [0, 2]
assert select_airport_cities([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 1]) == [], "should be an empty list"
assert select_airport_cities([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [1, 2, 3]) == []
assert select_airport_cities([[0, 5, 4], [5, 0, 3], [4, 3, 0]], [7, 8, 5]) == []
assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [4, 5, 6, 7]) == []
assert select_airport_cities([[0, 1, 2, 1], [1, 0, 2, 1], [2, 2, 0, 1], [1, 1, 1, 0]], [2, 1, 0, 3]) == [1, 2]
assert select_airport_cities([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [0, 0, 0, 0, 0]) == []
assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [1, 1, 1, 1]) == []
assert select_airport_cities([[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]], [4, 5, 6, 7]) == []
assert select_airport_cities([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]],[2,2,2,2,2]) == []
assert select_airport_cities([[0, 1, 5], [1, 0, 2], [5, 2, 0]], [3, 3, 3]) == []
assert select_airport_cities([[0, 1, 2, 3], [1, 0, 2, 3], [2, 2, 0, 3], [3, 3, 3, 0]], [0, 0, 0, 0]) == [0, 1, 2, 3]
assert select_airport_cities([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]], [5,5,5,5,5]) == []
assert select_airport_cities([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3]) == []
assert select_airport_cities([[0, 1, 2], [1, 0, 2], [2, 2, 0]], [2, 3, 1]) == []
assert select_airport_cities([[0, 1, 5, 9], [1, 0, 2, 6], [5, 2, 0, 4], [9, 6, 4, 0]], [10, 5, 3, 1]) == [2, 3]
assert select_airport_cities([[0, 0, 1], [0, 0, 1], [1, 1, 0]], [1, 1, 1]) == []
assert select_airport_cities([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 1]) == []
assert select_airport_cities([[0, 1, 2], [1, 0, 3], [2, 3, 0]], [3, 2, 1]) == []
assert select_airport_cities([[0, 100, 100, 100], [100, 0, 100, 100], [100, 100, 0, 100], [100, 100, 100, 0]], [100, 100, 100, 100]) == []
assert select_airport_cities([[0,2,2,2,1],[2,0,2,2,1],[2,2,0,2,1],[2,2,2,0,1],[1,1,1,1,0]], [5,5,5,5,5]) == []
assert select_airport_cities([[0,1,1,100,100,100], [1,0,100,1,100,100], [1,100,0,100,1,100], [100,1,100,0,100,1], [100,100,1,100,0,100], [100,100,100,1,100,0]], [0,0,0,0,0,0])
assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [.25, .25, .25, .25]) == [0, 1, 2, 3]
assert select_airport_cities([[0, 3, 3], [3, 0, 3], [3, 3, 0]], [0, 1, 2]) == [0, 1, 2]
assert select_airport_cities([[0, 1, 3], [1, 0, 1], [3, 1, 0]], [2, 1, 0]) == []
assert select_airport_cities([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [1, 1, 1]) == []
assert select_airport_cities([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], [0, 1, 1, 1]) == []
assert select_airport_cities([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]], [0,1,1,1,1]) == []
assert select_airport_cities([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]], [1,1,1,1]) == []
assert final_node_connectors([[0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]) == []
assert final_node_connectors([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]) == []
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0]]) == []
assert final_node_connectors([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11]]) == []
assert final_node_connectors([[0, 1, 1, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]) == []
assert final_node_connectors([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]]) == [1, 2]
assert final_node_connectors([[0,0],[1,0]]) == []
assert final_node_connectors([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) == []
assert final_node_connectors([[0],[1],[0],[0]]) == [], "expected []"
assert final_node_connectors([[0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]) == [1, 2]
assert final_node_connectors([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]) == [1, 2]
assert final_node_connectors([[0,0,0,1,0],[0,0,0,0,0],[0,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0]]) == []
assert final_node_connectors([[0,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]) == []
assert final_node_connectors([[0,1],[1,0]]) == []
assert final_node_connectors([[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,1,0]]) == []
assert final_node_connectors([[0,0,0],[1,0,0],[1,1,0]]) == []
assert final_node_connectors([[0,0,0,0],[0,0,1,1],[0,1,0,0],[0,1,0,0]]) == []
assert final_node_connectors([[0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]]) == [], "Test 1 failed"
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 1, 0]]) == []
assert final_node_connectors([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]) == [1, 2]
assert final_node_connectors([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == []
assert final_node_connectors([[0, 1], [1, 0]]) == [], 'test 1'
assert final_node_connectors([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]) == [0, 2]
assert final_node_connectors([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]) == [] # only one node connected to the final node, so the answer is an empty list
assert final_node_connectors([[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,1,0]]) == []
assert final_node_connectors([[0, 1, 1], [0, 0, 1], [0, 0, 0]]) == [0, 1]
assert final_node_connectors([[0, 1], [1, 0]]) == []
assert final_node_connectors([[0,1,1,1],[1,0,1,0],[1,1,0,1],[1,0,1,0]]) == [0,2]
assert final_node_connectors([[0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [0, 1, 0, 0, 1], [0, 0, 0, 1, 0]]) == [2, 3]
assert final_node_connectors([[0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0]]) == [1,2]
assert final_node_connectors([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]) == []
assert final_node_connectors([[0, 1, 0], [0, 0, 1], [0, 0, 0]]) == []
assert final_node_connectors([[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == []
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]) == []
assert final_node_connectors([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]) == []
assert final_node_connectors([[0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]) == [], 'incorrect'
assert final_node_connectors([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]) == []
assert final_node_connectors([[0, 1, 0], [0, 0, 1], [1, 0, 0]]) == []
assert final_node_connectors([[0,0,0],[0,0,0],[0,0,0]]) == []
assert final_node_connectors([[0, 0, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]) == [0, 1, 2]
assert final_node_connectors([[0,1,1],[1,0,1],[1,1,0]]) == [0,1]
assert final_node_connectors([[1, 2], [2]]) == []
assert final_node_connectors([[0,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0]]) == []
assert final_node_connectors([[0,0,0,0,1],[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0]]) == []
assert final_node_connectors([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]) == []
assert final_node_connectors([[0,1],[0,0]]) == [], 'incorrect'
assert final_node_connectors([[0, 1, 1], [1, 0, 0], [1, 0, 0]]) == []
assert final_node_connectors([[0,1,0,0,0,0], [1,0,1,0,0,0], [0,1,0,1,0,0], [0,0,1,0,1,1], [0,0,0,1,0,1], [0,0,0,1,1,0]]) == [3, 4], 'incorrect'
assert final_node_connectors([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == [], "incorrect output"
assert final_node_connectors([[0,0,0],[0,0,1],[0,0,0]]) == []
