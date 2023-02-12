collatz_recursion(num, cur_list=None): Calls base_case if 1, otherwise recursion_rule
    base_case(num, cur_list): Returns the list with the number appended to it
    recursion_rule(num, cur_list): Add num to list, collatz with 3n + 1 if odd or n / 2 if even
        collatz_recursion