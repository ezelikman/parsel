# am_i_wilson(n) returns True if n is a prime number between 2 and 563, inclusive, and False otherwise.
def am_i_wilson(n):
    if is_prime(n) and 2 <= n and n <= 563:
        return (factorial(n-1) + 1) % (n**2) == 0
    else:
        return False

# is_prime takes a positive integer n and returns True if n is prime and False otherwise.
def is_prime(n):
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


# factorial(n) returns the product of all integers from 1 to n, inclusive.
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


assert am_i_wilson(0) == False
assert am_i_wilson(1) == False
assert am_i_wilson(5) == True
assert am_i_wilson(8) == False
assert am_i_wilson(9) == False
assert am_i_wilson(11) == False
assert am_i_wilson(13) == True
assert am_i_wilson(101) == False
assert am_i_wilson(563) == True
assert am_i_wilson(569) == False


