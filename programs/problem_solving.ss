select_airport_cities(city_road_cost, city_airport_cost): given a matrix representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city (where any two cities with airports are connected), return a list of the cities that should have airports built in them to minimize the total cost of building roads and airports such that all cities are connected. The list should be sorted in ascending order.
[[0,3,3],[3,0,3],[3,3,0]],[0,0,0] -> [0,1,2]
[[0,3,3],[3,0,3],[3,3,0]],[10,10,10] -> []
[[0,10,3],[10,0,11],[3,11,0]],[1,4,5] -> [0,1]
    sky_city_cost(city_road_cost, city_airport_cost): given a list of lists representing the cost of building a road between any two cities, and a list representing the cost of building an airport in a city, return a new cost matrix with a new node corresponding to the sky.
    [[1,2,3],[1,2,3],[1,2,3]],[4,5,6] -> [[1,2,3,4],[1,2,3,5],[1,2,3,6],[4,5,6,0]]
    minimum_spanning_tree(cost_matrix): given a list of lists representing the cost of each edge, return an adjacency matrix corresponding to the minimum spanning true.
    [[0,1,3,4],[1,0,2,100],[3,2,0,5],[4,100,5,0]] -> [[0,1,0,1],[1,0,1,0],[0,1,0,0],[1,0,0,0]]
    final_node_connectors(adjacency_matrix): given a list of lists representing an adjacency matrix, return a list of the nodes connected to the final node. However, if only one node is connected to the final node, return an empty list.
    [[0,1,0,1],[1,0,1,0],[0,1,0,0],[1,0,0,0]] -> []
    [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]] -> [0,2]