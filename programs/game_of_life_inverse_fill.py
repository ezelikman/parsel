# Takes a board and returns the next iteration of the game of life, but with all values flipped
def game_of_life_inversion_iteration(array_at_time_t):
    next_array = game_of_life_iteration(array_at_time_t)
    return array_inversion(next_array)

# Takes a board with active and inactive cells as a list of lists and returns the next iteration of the game of life
def game_of_life_iteration(array_at_time_t):
    # Create an empty array to store the next iteration of the game of life
    array_at_time_t_plus_1 = []
    # Iterate over the rows of the board
    for row in range(len(array_at_time_t)):
        # Create an empty row to store the next iteration of the game of life
        array_at_time_t_plus_1_row = []
        # Iterate over the columns of the board
        for column in range(len(array_at_time_t[0])):
            # Get the number of active cells around the current cell
            active_cells_around_current_cell = get_number_of_active_cells_around_cell(row, column, array_at_time_t)
            # Check whether the current cell is active or inactive
            if array_at_time_t[row][column] == 1:
                # Check whether the current cell has two or three active cells around it
                if active_cells_around_current_cell == 2 or active_cells_around_current_cell == 3:
                    # Set the current cell to active for the next iteration
                    array_at_time_t_plus_1_row.append(1)
                else:
                    # Set the current cell to inactive for the next iteration
                    array_at_time_t_plus_1_row.append(0)
            else:
                # Check whether the current cell has three active cells around it
                if active_cells_around_current_cell == 3:
                    # Set the current cell to active for the next iteration
                    array_at_time_t_plus_1_row.append(1)
                else:
                    # Set the current cell to inactive for the next iteration
                    array_at_time_t_plus_1_row.append(0)
        # Add the row to the board for the next iteration
        array_at_time_t_plus_1.append(array_at_time_t_plus_1_row)
    # Return the next iteration of the game of life
    return array_at_time_t_plus_1


# Invert a square array by flipping 0's and 1's
def array_inversion(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 1:
                array[i][j] = 0
            else:
                array[i][j] = 1
    return array

# 
def get_number_of_active_cells_around_cell(row, column, array_at_time_t):
    active_cells_around_current_cell = 0
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if i >= 0 and j >= 0 and i < len(array_at_time_t) and j < len(array_at_time_t[0]):
                if array_at_time_t[i][j] == 1:
                    active_cells_around_current_cell += 1
    if array_at_time_t[row][column] == 1:
        active_cells_around_current_cell -= 1
    return active_cells_around_current_cell



assert game_of_life_inversion_iteration([[0, 0, 1], [1, 0, 0], [1, 0, 0]]) == [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
assert game_of_life_inversion_iteration([[0, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]) == [[1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]]



