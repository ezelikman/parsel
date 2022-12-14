game_of_life_inversion_iteration(array_at_time_t): Takes a board and returns the next iteration of the game of life, but with all values flipped
[[0, 0, 1], [1, 0, 0], [1, 0, 0]] -> [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
[[0, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]] -> [[1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]]
    game_of_life_iteration(array_at_time_t): Takes a board with active and inactive cells as a list of lists and returns the next iteration of the game of life
    array_inversion(array): Invert a square array by flipping 0's and 1's