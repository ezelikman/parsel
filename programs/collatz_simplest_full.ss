collatz_recursion(num, cur_list=list()): Calls base_case if 1, otherwise recursion_rule
19 -> [19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    base_case(num, cur_list): Returns the list with the number appended to it
    1, [1, 2, 3] -> [1, 2, 3, 1]
    recursion_rule(num, cur_list): Add num to list, collatz with 3n + 1 if odd or n / 2 if even
    2, [1, 2, 3] -> [1, 2, 3, 2, 1]
        collatz_recursion