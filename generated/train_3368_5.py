# circular_prime takes a number and returns True if it is a circular prime, and False otherwise.
def circular_prime(number):
    if is_prime(number) == False:
        return False
    else:
        for i in range(len(str(number))-1):
            number = rotate(str(number), 1)
            if is_prime(int(number)) == False:
                return False
        return True

# rotate takes a list and an integer and returns a new list with the last n elements of the original list moved to the front.
def rotate(l, n):
    return l[-n:] + l[:-n]

# is_prime returns True if n is a prime number, and False otherwise.
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


assert circular_prime(197) == True
assert circular_prime(179) == False
assert circular_prime(971) == True
assert circular_prime(222) == False
assert circular_prime(9377) == True
assert circular_prime(7) == True
assert circular_prime(213) == False
assert circular_prime(35) == False
assert circular_prime(1) == False


