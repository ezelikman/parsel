# am_i_wilson takes a positive integer n and returns True if n is prime and (n-1)! + 1 is divisible by n^2, and False otherwise.
def am_i_wilson(n):
    return is_prime(n) and (fac(n-1) + 1) % n**2 == 0

# fac is a function that takes a positive integer n and returns the product of all integers from 1 to n.
def fac(n):
    if n == 0:
        return 1
    return n * fac(n-1)
# is_prime takes a positive integer n and returns True if n is prime and False otherwise.
def is_prime(n):
    if n == 2:
        return True
    elif n < 2 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True


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


