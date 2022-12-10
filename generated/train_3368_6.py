# circular_prime(n) returns True if n is a circular prime, and False otherwise.
def circular_prime(n):
    # Check if n is a prime number.
    if not is_prime(n):
        return False
    else:
        # Get the length of n.
        length = len(str(n))
        # Get the first digit of n.
        first_digit = str(n)[0]
        # Get the number of rotations.
        rotations = length
        # Rotate n.
        while rotations > 0:
            # Get the new number.
            n = circul_num(n, length)
            # Check if n is a prime number.
            if not is_prime(n):
                return False
            # Decrement the number of rotations.
            rotations -= 1
        return True
# is_prime takes a number n and returns True if n is prime and False if n is not prime.
def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    for i in range(3, int(n**0.5)+1, 2):   # only odd numbers
        if n % i == 0:
            return False
    return True

# circul_num takes an integer n and an integer l, and returns the integer that results from moving the first digit of n to the end of n, and then padding the result with zeros until it has length l.
def circul_num(n, l):
    n = str(n)
    digit = n[0]
    n = n[1:] + digit
    n = n.ljust(l, "0")
    return int(n)



assert circular_prime(197) == True
assert circular_prime(179) == False
assert circular_prime(971) == True
assert circular_prime(222) == False
assert circular_prime(9377) == True
assert circular_prime(7) == True
assert circular_prime(213) == False
assert circular_prime(35) == False
assert circular_prime(1) == False


