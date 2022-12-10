# Takes a board and returns the next iteration of the game of life, but with all values flipped
def game_of_life_inversion_iteration(array_at_time_t):
    # Your code here
    #return game_of_life_iteration(invert_array(array_at_time_t))
    return invert_array(game_of_life_iteration(array_at_time_t))

# Takes a board and returns the next iteration of the game of life
def invert_array(array_at_time_t):
    return [list(map(lambda x: 1-x, row)) for row in array_at_time_t]

# Takes a board and returns the board with all values flipped
def game_of_life_iteration(array_at_time_t):
    # The array that will be returned
    array_at_time_t_plus_1 = []

    # Iterate through the rows of the array
    for i in range(0, len(array_at_time_t)):
        # The array that will contain the next row
        next_row = []

        # Iterate through the columns of the array
        for j in range(0, len(array_at_time_t[i])):
            # The number of neighbors
            num_neighbors = 0

            # Iterate through the neighbors of the cell
            for k in range(-1, 2):
                for l in range(-1, 2):
                    # Don't count the cell itself
                    if k == 0 and l == 0:
                        continue

                    # Check if the neighbor is valid
                    if i + k >= 0 and i + k < len(array_at_time_t) and j + l >= 0 and j + l < len(array_at_time_t[i]):
                        # If the neighbor is alive, increment the number of neighbors
                        if array_at_time_t[i + k][j + l] == 1:
                            num_neighbors += 1

            # If the cell is alive, check if it should die
            if array_at_time_t[i][j] == 1:
                if num_neighbors < 2 or num_neighbors > 3:
                    next_row.append(0)
                else:
                    next_row.append(1)
            # If the cell is dead, check if it should become alive
            else:
                if num_neighbors == 3:
                    next_row.append(1)
                else:
                    next_row.append(0)

        # Add the next row to the array
        array_at_time_t_plus_1.append(next_row)

    # Return the next array
    return array_at_time_t_plus_1



assert game_of_life_inversion_iteration([[0, 0, 1], [1, 0, 0], [1, 0, 0]]) == [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
assert game_of_life_inversion_iteration([[0, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]) == [[1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]]


