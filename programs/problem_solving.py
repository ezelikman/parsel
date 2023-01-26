# given a list of lists representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city, return a new cost matrix with a new node corresponding to the sky.
def sky_city_cost(city_road_cost, city_airport_cost):
    """
    :param city_road_cost: list of lists representing cost of road between any two cities
    :param city_airport_cost: list representing cost of an airport in a city
    :return: new cost matrix with a new node corresponding to the sky
    """
    # add new node for sky to cost matrix
    num_cities = len(city_road_cost)
    sky_city_cost = [[0 for _ in range(num_cities + 1)] for _ in range(num_cities + 1)]
    for i in range(num_cities):
        for j in range(num_cities):
            sky_city_cost[i][j] = city_road_cost[i][j]
    for i in range(num_cities):
        sky_city_cost[i][-1] = city_airport_cost[i]
        sky_city_cost[-1][i] = city_airport_cost[i]
    return sky_city_cost


# given a list of lists representing the cost of each edge, return an adjacency matrix corresponding to the minimum spanning true.
def minimum_spanning_tree(cost_matrix):
    # This is a list of the vertices that have been added to the MST
    visited = [0]
    # This is a list of the vertices that have not been added to the MST
    unvisited = [i for i in range(1, len(cost_matrix))]
    # This is a list of edges that are part of the MST
    edges = []
    # This is the adjacency matrix corresponding to the MST
    adjacency_matrix = [[0 for i in range(len(cost_matrix))] for j in range(len(cost_matrix))]
    while len(unvisited) > 0:
        # Get the index of the minimum edge
        min_edge_index = -1
        min_edge_value = float('inf')
        for i in range(len(visited)):
            for j in range(len(unvisited)):
                if cost_matrix[visited[i]][unvisited[j]] < min_edge_value:
                    min_edge_index = (visited[i], unvisited[j])
                    min_edge_value = cost_matrix[visited[i]][unvisited[j]]
        # Add the minimum edge to our MST
        edges.append(min_edge_index)
        # Add the unvisited vertex to the list of visited vertices
        visited.append(min_edge_index[1])
        # Remove the unvisited vertex from the list of unvisited vertices
        unvisited.remove(min_edge_index[1])
    # Add edges to the adjacency matrix
    for edge in edges:
        adjacency_matrix[edge[0]][edge[1]] = 1
        adjacency_matrix[edge[1]][edge[0]] = 1
    return adjacency_matrix

# given a list of lists representing an adjacency matrix, return a list of the nodes connected to the final node. However, if only one node is connected to the final node, return an empty list.
def final_node_connectors(adjacency_matrix):
    final_node = len(adjacency_matrix) - 1
    final_node_connectors = []
    for i in range(len(adjacency_matrix) - 1):
        if adjacency_matrix[i][final_node] == 1:
            final_node_connectors.append(i)
    if len(final_node_connectors) == 1:
        return []
    return final_node_connectors

# given a matrix representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city (where any two cities with airports are connected), return a list of the cities that should have airports built in them to minimize the total cost of building roads and airports such that all cities are connected. The list should be sorted in ascending order.
def select_airport_cities(city_road_cost, city_airport_cost):
    cost_matrix = sky_city_cost(city_road_cost, city_airport_cost)
    adjacency_matrix = minimum_spanning_tree(cost_matrix)
    return final_node_connectors(adjacency_matrix)


assert repr(str(select_airport_cities([[0, 3, 3], [3, 0, 3], [3, 3, 0]], [0, 0, 0]))) == repr(str([0, 1, 2]))
assert repr(str(select_airport_cities([[0, 3, 3], [3, 0, 3], [3, 3, 0]], [10, 10, 10]))) == repr(str([]))
assert repr(str(select_airport_cities([[0, 10, 3], [10, 0, 11], [3, 11, 0]], [1, 4, 5]))) == repr(str([0, 1]))

assert repr(str(sky_city_cost([[1, 2, 3], [1, 2, 3], [1, 2, 3]], [4, 5, 6]))) == repr(str([[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 3, 6], [4, 5, 6, 0]]))

assert repr(str(minimum_spanning_tree([[0, 1, 3, 4], [1, 0, 2, 100], [3, 2, 0, 5], [4, 100, 5, 0]]))) == repr(str([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]))

assert repr(str(final_node_connectors([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]))) == repr(str([]))
assert repr(str(final_node_connectors([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]))) == repr(str([0, 2]))
