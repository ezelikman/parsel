prompt = (
# """-----Solution Plan-----
# Propose an algorithmic solution plan describing how you can solve this problem.

# ANSWER as a step by step solution plan (in high-level English):
# \"\"\"
# 1."""

# """-----Solution-----

# Propose a clever and efficient high-level solution for this problem. Consider all edge cases and failure modes.

# \"\"\"
# 1."""
# )


# Brute force, Greedy algorithms, Constructive algorithms, Binary search, Depth-first search (DFS) and similar algorithms, Dynamic programming, Graphs, Math, Two pointers, Trees, Bitmasks, Strings, Geometry, Graph matchings, Hashing, Probabilities, Data structures, Sortings, Games, Number theory, Combinatorics, Divide and conquer, Disjoint set union (DSU), Expression parsing

"""-----Solution-----

Propose a clever and efficient high-level solution for this problem. Consider all edge cases and failure modes.

Some common strategies include:
Constructive algorithms, Binary search, Depth-first search (DFS) and similar algorithms, Dynamic programming, Bitmasks, Brute force, Greedy algorithms, Graphs, Two pointers, Trees, Geometry, Graph matchings, Hashing, Probabilities, Data structures, Sortings, Games, Number theory, Combinatorics, Divide and conquer, Disjoint set union (DSU), Expression parsing

Write out your reasoning first, and then describe your high-level solution and explain why it is correct.
\"\"\"
Let's think step by step to come up with a clever algorithm."""
)

solution_start = ""

prefix_prefix = "QUESTION:\n"

prefix_suffix = (
"""
Use Standard Input format

ANSWER in Python code:
"""
)

# # Here is an example of Parsel for the Collatz conjecture:
# \"\"\"
# collatz_recursion(input_str): Calls base_case if 1, otherwise call recursion_rule
#   parse_input(input_str): Takes a string and returns an integer and a list of integers
#   collatz_recursion_helper(input_str): Calls base_case if 1, otherwise call recursion_rule
#     base_case(num, cur_list): Returns the list with the number appended to it
#     recursion_rule(num, cur_list): Add num to list, recurse with num = 3n + 1 if odd or num = n / 2 if even
#       collatz_recursion_helper
#   to_output_str(collatz_list): Takes a list and returns a string representation of the list with each element separated by a space
# \"\"\"

# # And here is an example of the format applied to a function that generates all sets of subsequences such that X are left after all those with a difference of d are removed:
# \"\"\"
# generate_sequence(input_str): Generates and returns a sequence of integers based on the input values X and d.
#   parse_input(input_str): Takes a string and returns the values of X and d
#   generate_sequence_helper(X, d): Generates and returns the sequence of integers
#     init_sequence_and_cur(X, d): Initializes an empty list `sequence` and a variable `cur` to `1`.
#     check_bits_and_append(X, d, sequence, cur): Iterates over the range `(32)` and checks if the `i`th bit of `X` is set. If the bit is set, appends `cur` to the list `i` times, increments `cur` by `d`, appends `cur` to the list, and increments `cur` by `d` again.
#   to_output_str(sequence): Takes a list and returns a string representation with each element separated by a space
# \"\"\"

# # And here is an example of the format applied to a function that identifies optimal distances to each after abandoning roads:
# # Codefortia is a small island country located somewhere in the West Pacific. It consists of $n$ settlements connected by $m$ bidirectional gravel roads. Curiously enough, the beliefs of the inhabitants require the time needed to pass each road to be equal either to $a$ or $b$ seconds. It's guaranteed that one can go between any pair of settlements by following a sequence of roads.
# # Codefortia was recently struck by the financial crisis. Therefore, the king decided to abandon some of the roads so that: 
# # it will be possible to travel between each pair of cities using the remaining roads only,  the sum of times required to pass each remaining road will be minimum possible (in other words, remaining roads must form minimum spanning tree, using the time to pass the road as its weight),  among all the plans minimizing the sum of times above, the time required to travel between the king's residence (in settlement $1$) and the parliament house (in settlement $p$) using the remaining roads only will be minimum possible. 
# # The king, however, forgot where the parliament house was. For each settlement $p = 1, 2, \dots, n$, can you tell what is the minimum time required to travel between the king's residence and the parliament house (located in settlement $p$) after some roads are abandoned?
# \"\"\"
# shortest_path(input_str): Returns the minimum cost path from the starting vertex to all other vertices, finding the shortest path from the starting vertex to each vertex in the graph
#   parse_input(input_str): Takes a string and returns the graph, a, b, and starting vertex
#   find_connected_components(graph): Returns a list of connected components in the graph
#   remove_useless_edges(graph, components, a, b): Removes edges within a component with cost b, and removes components with fewer than three vertices
#   modified_dijkstra(graph, components, a, b): Returns the minimum cost path from the starting vertex to all other vertices, subject to the condition that for each component, the path must visit at least three vertices
#     modified_dijkstra_helper(graph, components, a, b, start, mask, distances): Updates the distances of the neighbors of start if a shorter path is found
#   to_output_str(distances): Takes a list of minimum distances and returns a string representation with each element separated by a space
# \"\"\"

translation_prompt = (
"""-----Translation-----
# Here is an example calculating the probability of landing on the same character in a random shift of an input string, based on the following problem:
# Vasya and Kolya play a game with a string, using the following rules. Initially, Kolya creates a string s, consisting of small English letters, and uniformly at random chooses an integer k from a segment [0, len(s) - 1]. He tells Vasya this string s, and then shifts it k letters to the left, i. e. creates a new string t = s_k + 1s_k + 2... s_ns_1s_2... s_k. Vasya does not know the integer k nor the string t, but he wants to guess the integer k. To do this, he asks Kolya to tell him the first letter of the new string, and then, after he sees it, open one more letter on some position, which Vasya can choose.
# Vasya understands, that he can't guarantee that he will win, but he wants to know the probability of winning, if he plays optimally. He wants you to compute this probability.
# Note that Vasya wants to know the value of k uniquely, it means, that if there are at least two cyclic shifts of s that fit the information Vasya knowns, Vasya loses. Of course, at any moment of the game Vasya wants to maximize the probability of his win.
\"\"\"
generate_cyclic_shifts(input_str): Calculates the average number of unique characters in the substrings of the input string that start with each character.
  parse_input(input_str): Takes a string and returns the input string
  compute_a_and_letter_pos(input_str): Generates the str_as_number_list and letter_pos lists. str_as_number_list is a list of integers that is used to store the character values of the input string. str_as_number_list is initialized as a list of 0s for twice the length of the input string. The values are calculated by taking the ASCII value of each character in the string and subtracting the ASCII value of the character 'a'. letter_pos is a list of lists, with each sublist containing the indices at which a particular character appears in the input string.
  compute_unique_characters(c, str_as_number_list, letter_pos) -> ans: Calculates the maximum number of unique characters in all substrings (for k=1 to length) that start with the character represented by c. letter_pos is a list of lists, with each sublist containing the indices at which a character appears in the input string. str_as_number_list is a list of integers that is used to store the character values of the input string.
    compute_unique_characters_for_k(c, k, str_as_number_list, letter_pos): Create a counts list of zeros for each of the 26 alphabetical characters. For each i in the sublist of positions of letter_pos[c], increment counts at str_as_number_list[i + k]. Return the number of counts which are exactly one.
  to_output_str(ans, input_str): Returns a string representation of ans divided by the length of the input string.
\"\"\"
(6 lines)

# And here is an example identifying the largest binary number according to the following rules:
# The Little Elephant has an integer a, written in the binary notation. He wants to write this number on a piece of paper.
# To make sure that the number a fits on the piece of paper, the Little Elephant ought to delete exactly one any digit from number a in the binary record. At that a new number appears. It consists of the remaining binary digits, written in the corresponding order (possible, with leading zeroes).
# The Little Elephant wants the number he is going to write on the paper to be as large as possible. Help him find the maximum number that he can obtain after deleting exactly one binary digit and print it in the binary notation.
\"\"\"
largest_binary_number(input_str): Returns the largest binary number that can be made by removing at most one digit from the input string.
  parse_input(input_str): Takes a string and returns the input string
  remove_zero(binary_str): Remove the first zero from the input string.
  to_output_str(bigger_str): Returns the bigger string.
\"\"\"
(4 lines)

# Here is an example of the format applied to identifying the winner of the following game:
# It is so boring in the summer holiday, isn't it? So Alice and Bob have invented a new game to play. The rules are as follows. First, they get a set of n distinct integers. And then they take turns to make the following moves. During each move, either Alice or Bob (the player whose turn is the current) can choose two distinct integers x and y from the set, such that the set doesn't contain their absolute difference |x - y|. Then this player adds integer |x - y| to the set (so, the size of the set increases by one).
# If the current player has no valid move, he (or she) loses the game. The question is who will finally win the game if both players play optimally. Remember that Alice always moves first.
\"\"\"
identify_winner(input_str): Returns the winner of the game.
  parse_input(input_str): Takes a string containing the length on the first line and the integers on the second and returns the list of integers
  num_moves(l): The number of moves is the largest element in the list divided by the greatest common divisor of all elements in the list, minus the length of the list.
    all_gcd(l): Returns the greatest common divisor of all elements in the list
  to_output_str(num_moves): Returns the string 'Alice' if the number of moves is odd and 'Bob' if the number of moves is even
\"\"\"
(5 lines)

# Limak is a little bear who loves to play. Today he is playing by destroying block towers. He built n towers in a row. The i-th tower is made of h_i identical blocks. For clarification see picture for the first sample.
# Limak will repeat the following operation till everything is destroyed.
# Block is called internal if it has all four neighbors, i.e. it has each side (top, left, down and right) adjacent to other block or to the floor. Otherwise, block is boundary. In one operation Limak destroys all boundary blocks. His paws are very fast and he destroys all those blocks at the same time.
# Limak is ready to start. You task is to count how many operations will it take him to destroy all towers.
\"\"\"
destroy_towers(input_str): Returns the number of operations it takes to destroy all towers.
  parse_input(input_str): Takes a string containing the number of towers on the first line and the heights of the towers on the second and returns the list of heights
  side_ones(heights_list): From a list of ints, set the first and last elements to 1 and return the list
  destroy_from_left(side_list): Copy the list and set each each element to the minimum of itself and one more than the element to its left, starting from the second element
  destroy_from_right(side_list): Copy the list and set each each element to the minimum of itself and one more than the element to its right, starting from the second to last element
  min_list(l1, l2): Return a list of the minimum of the corresponding elements of l1 and l2
  to_output_str(min_list): Return the string representation of the maximum element in the list
\"\"\"
(7 lines)

# Alex decided to go on a touristic trip over the country.
# For simplicity let's assume that the country has $n$ cities and $m$ bidirectional roads connecting them. Alex lives in city $s$ and initially located in it. To compare different cities Alex assigned each city a score $w_i$ which is as high as interesting city seems to Alex.
# Alex believes that his trip will be interesting only if he will not use any road twice in a row. That is if Alex came to city $v$ from city $u$, he may choose as the next city in the trip any city connected with $v$ by the road, except for the city $u$.
# Your task is to help Alex plan his city in a way that maximizes total score over all cities he visited. Note that for each city its score is counted at most once, even if Alex been there several times during his trip.
\"\"\"
max_score(input_str): Simple function returning the maximum score Alex can get.
  parse_input(input_str): Takes a string containing the number of cities and roads on one line, the scores of the cities on the next line, the roads on the next lines besides the last (1-indexed, make 0-indexed), and the starting city on the last line. It returns the city scores, the roads as an edge list, and the starting city.
  get_neighbors(edges): Returns a dictionary of the neighbors of each city, defaulting to an empty set.
  get_degrees_and_leaves(neighbors, root): Returns a dictionary of the degrees of each city, and a set of the leaves (excluding the root).
  remove_leaves(scores, neighbors, degrees, leaves, root): Create a 0-initialized defaultdict of total_extra, and an int of max_extra. Pop leaves until it is empty. Update total_extra and max_extra based on the parent's total_extra vs the leaf's score plus its total_extra, whichever is greater. Return max_extra.
    pop_leaf(neighbors, degrees, leaves, root): Pop off a leaf. Set parent to sole neighbor of the leaf and delete the leaf from the neighbors dictionary. Decrement the parent's degree. If the parent is not the root and has degree 1, add it to the leaves. Return the leaf and parent.
  to_output_str(scores, neighbors, root, max_extra): Returns the string of the maximum score Alex can get. If the root isn't in neighbors, return the score of the root. Otherwise, this is the sum of the scores of the cities left in neighbors, plus the returned encountered max_extra.
\"\"\"
(7 lines)

# Translate the following solution plan into the above format:
{solution_start}{solution_text}

TRANSLATE to Parsel.
\"\"\"
"""
)

direct_prompt = (
"""-----Solution-----
# Here is an example calculating the probability of landing on the same character in a random shift of an input string, based on the following problem:
# Vasya and Kolya play a game with a string, using the following rules. Initially, Kolya creates a string s, consisting of small English letters, and uniformly at random chooses an integer k from a segment [0, len(s) - 1]. He tells Vasya this string s, and then shifts it k letters to the left, i. e. creates a new string t = s_k + 1s_k + 2... s_ns_1s_2... s_k. Vasya does not know the integer k nor the string t, but he wants to guess the integer k. To do this, he asks Kolya to tell him the first letter of the new string, and then, after he sees it, open one more letter on some position, which Vasya can choose.
# Vasya understands, that he can't guarantee that he will win, but he wants to know the probability of winning, if he plays optimally. He wants you to compute this probability.
# Note that Vasya wants to know the value of k uniquely, it means, that if there are at least two cyclic shifts of s that fit the information Vasya knowns, Vasya loses. Of course, at any moment of the game Vasya wants to maximize the probability of his win.
\"\"\"
generate_cyclic_shifts(input_str): Calculates the average number of unique characters in the substrings of the input string that start with each character.
  parse_input(input_str): Takes a string and returns the input string
  compute_a_and_letter_pos(input_str): Generates the str_as_number_list and letter_pos lists. str_as_number_list is a list of integers that is used to store the character values of the input string. str_as_number_list is initialized as a list of 0s for twice the length of the input string. The values are calculated by taking the ASCII value of each character in the string and subtracting the ASCII value of the character 'a'. letter_pos is a list of lists, with each sublist containing the indices at which a particular character appears in the input string.
  compute_unique_characters(c, str_as_number_list, letter_pos) -> ans: Calculates the maximum number of unique characters in all substrings (for k=1 to length) that start with the character represented by c. letter_pos is a list of lists, with each sublist containing the indices at which a character appears in the input string. str_as_number_list is a list of integers that is used to store the character values of the input string.
    compute_unique_characters_for_k(c, k, str_as_number_list, letter_pos): Create a counts list of zeros for each of the 26 alphabetical characters. For each i in the sublist of positions of letter_pos[c], increment counts at str_as_number_list[i + k]. Return the number of counts which are exactly one.
      count_ones(l): Return the number of elements that are one.
  to_output_str(ans, input_str): Returns a string representation of ans divided by the length of the input string.
\"\"\"

# And here is an example identifying the largest binary number according to the following rules:
# The Little Elephant has an integer a, written in the binary notation. He wants to write this number on a piece of paper.
# To make sure that the number a fits on the piece of paper, the Little Elephant ought to delete exactly one any digit from number a in the binary record. At that a new number appears. It consists of the remaining binary digits, written in the corresponding order (possible, with leading zeroes).
# The Little Elephant wants the number he is going to write on the paper to be as large as possible. Help him find the maximum number that he can obtain after deleting exactly one binary digit and print it in the binary notation.
\"\"\"
largest_binary_number(input_str): Returns the largest binary number that can be made by removing at most one digit from the input string.
  parse_input(input_str): Takes a string and returns the input string
  remove_zero(binary_str): Remove the first zero from the input string.
  to_output_str(bigger_str): Returns the bigger string.
\"\"\"

# Here is an example of the format applied to identifying the winner of the following game:
# It is so boring in the summer holiday, isn't it? So Alice and Bob have invented a new game to play. The rules are as follows. First, they get a set of n distinct integers. And then they take turns to make the following moves. During each move, either Alice or Bob (the player whose turn is the current) can choose two distinct integers x and y from the set, such that the set doesn't contain their absolute difference |x - y|. Then this player adds integer |x - y| to the set (so, the size of the set increases by one).
# If the current player has no valid move, he (or she) loses the game. The question is who will finally win the game if both players play optimally. Remember that Alice always moves first.
\"\"\"
identify_winner(input_str): Returns the winner of the game.
  parse_input(input_str): Takes a string containing the length on the first line and the integers on the second and returns the list of integers
  num_moves(l): The number of moves is the largest element in the list divided by the greatest common divisor of all elements in the list, minus the length of the list.
    all_gcd(l): Returns the greatest common divisor of all elements in the list
  to_output_str(num_moves): Returns the string 'Alice' if the number of moves is odd and 'Bob' if the number of moves is even
\"\"\"

# Limak is a little bear who loves to play. Today he is playing by destroying block towers. He built n towers in a row. The i-th tower is made of h_i identical blocks. For clarification see picture for the first sample.
# Limak will repeat the following operation till everything is destroyed.
# Block is called internal if it has all four neighbors, i.e. it has each side (top, left, down and right) adjacent to other block or to the floor. Otherwise, block is boundary. In one operation Limak destroys all boundary blocks. His paws are very fast and he destroys all those blocks at the same time.
# Limak is ready to start. You task is to count how many operations will it take him to destroy all towers.
\"\"\"
destroy_towers(input_str): Returns the number of operations it takes to destroy all towers.
  parse_input(input_str): Takes a string containing the number of towers on the first line and the heights of the towers on the second and returns the list of heights
  side_ones(heights_list): From a list of ints, set the first and last elements to 1 and return the list
  destroy_from_left(side_list): Copy the list and set each each element to the minimum of itself and one more than the element to its left, starting from the second element
  destroy_from_right(side_list): Copy the list and set each each element to the minimum of itself and one more than the element to its right, starting from the second to last element
  min_list(l1, l2): Return a list of the minimum of the corresponding elements of l1 and l2
  to_output_str(min_list): Return the string representation of the maximum element in the list
\"\"\"

# Alex decided to go on a touristic trip over the country.
# For simplicity let's assume that the country has $n$ cities and $m$ bidirectional roads connecting them. Alex lives in city $s$ and initially located in it. To compare different cities Alex assigned each city a score $w_i$ which is as high as interesting city seems to Alex.
# Alex believes that his trip will be interesting only if he will not use any road twice in a row. That is if Alex came to city $v$ from city $u$, he may choose as the next city in the trip any city connected with $v$ by the road, except for the city $u$.
# Your task is to help Alex plan his city in a way that maximizes total score over all cities he visited. Note that for each city its score is counted at most once, even if Alex been there several times during his trip.
\"\"\"
max_score(input_str): Simple function returning the maximum score Alex can get.
  parse_input(input_str): Takes a string containing the number of cities and roads on one line, the scores of the cities on the next line, the roads on the next lines besides the last (1-indexed, make 0-indexed), and the starting city on the last line. It returns the city scores, the roads as an edge list, and the starting city.
  get_neighbors(edges): Returns a dictionary of the neighbors of each city, defaulting to an empty set.
  get_degrees_and_leaves(neighbors, root): Returns a dictionary of the degrees of each city, and a set of the leaves (excluding the root).
  remove_leaves(scores, neighbors, degrees, leaves, root): Create a 0-initialized defaultdict of total_extra, and an int of max_extra. Pop leaves until it is empty. Update total_extra and max_extra based on the parent's total_extra vs the leaf's score plus its total_extra, whichever is greater. Return max_extra.
    pop_leaf(neighbors, degrees, leaves, root): Pop off a leaf. Set parent to sole neighbor of the leaf and delete the leaf from the neighbors dictionary. Decrement the parent's degree. If the parent is not the root and has degree 1, add it to the leaves. Return the leaf and parent.
  to_output_str(scores, neighbors, root, max_extra): Returns the string of the maximum score Alex can get. If the root isn't in neighbors, return the score of the root. Otherwise, this is the sum of the scores of the cities left in neighbors, plus the returned encountered max_extra.
\"\"\"

You must write a function in the following format that takes a string as input and returns a string as output. The input string will be in the format described in the problem statement. The output string must be in the format described in the problem statement. Each line is one definition.

# ANSWER in the above format, using at most 6 definitions besides the main definition:
\"\"\"
"""
)