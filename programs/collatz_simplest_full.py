# Calls base_case if 1, otherwise recursion_rule
def collatz_recursion(num, cur_list=list()):
    if num == 1:
        return base_case(num, cur_list)
    else:
        return recursion_rule(num, cur_list)

# Returns the list with the number appended to it
def base_case(num, cur_list):
    cur_list.append(num)
    return cur_list


# Add num to list, collatz with 3n + 1 if odd or n / 2 if even
def recursion_rule(num, cur_list):
    cur_list.append(num)
    if num % 2 == 0:
        return collatz_recursion(int(num / 2), cur_list)
    else:
        return collatz_recursion(int(3 * num + 1), cur_list)


assert collatz_recursion(19) == [19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]

assert base_case(1, [1, 2, 3]) == [1, 2, 3, 1]

assert recursion_rule(2, [1, 2, 3]) == [1, 2, 3, 2, 1]
