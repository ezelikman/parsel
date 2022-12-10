# happy_numbers takes a positive integer n and returns a list of all the happy numbers between 1 and n, inclusive.
def happy_numbers(n):
    return [i for i in range(1, n + 1) if _is_happy_number(i)]

# _is_happy_number takes a positive integer and returns True if the number is a happy number, False otherwise.
def _is_happy_number(number):
    # We want to make sure that the number is positive
    if number < 0:
        return False
    # We want to make sure that the number is not 1
    if number == 1:
        return True
    # We want to keep track of the numbers we have used
    used_numbers = []
    # We want to loop through the number
    while number not in used_numbers:
        # We want to add the number to the list of used numbers
        used_numbers.append(number)
        # We want to find the sum of the squares of the digits of the number
        number = _sum_squares(number)
        # We want to check if the number is one
        if number == 1:
            # We want to return True
            return True
    # We want to return False
    return False

# _sum_squares takes a non-negative integer and returns the sum of the squares of its digits.
def _sum_squares(number):
    if number < 0:
        raise ValueError
    else:
        number = str(number)
        sum = 0
        for i in number:
            sum += int(i) ** 2
        return sum


assert happy_numbers(10) == [1, 7, 10]
assert happy_numbers(50) == [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49]
assert happy_numbers(100) == [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 86, 91, 94, 97, 100]


