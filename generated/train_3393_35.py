# list_squared(m, n) returns a list of lists of integers, where each sublist contains an integer and its sum of squared divisors, and the integers are in the range [m, n] (inclusive).
def list_squared(m, n):
    result = []
    for num in range(m, n + 1):
        divisors = divisors_list(num)
        sum_of_squares = sum_squares(divisors)
        if isSquarable(sum_of_squares):
            result.append([num, sum_of_squares])
    return result
# divisors_list takes a number and returns a list of all the divisors of that number.
def divisors_list(num):
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(i)
    return divisors


# sum_squares takes a list of numbers and returns the sum of the squares of those numbers.
def sum_squares(nums):
    sum = 0
    for i in range(len(nums)):
        sum += nums[i]**2
    return sum

# isSquarable takes a number and returns True if the number is a perfect square, and False otherwise.
def isSquarable(num):
    root = num ** (1/2)
    if root % 1 == 0:
        return True
    else:
        return False


assert list_squared(1,250) == [[1, 1], [42, 2500], [246, 84100]]
assert list_squared(42,250) == [[42, 2500], [246, 84100]]
assert list_squared(250,500) == [[287, 84100]]
assert list_squared(300,600) == []
assert list_squared(600,1500) == [[728, 722500], [1434, 2856100]]
assert list_squared(1500,1800) == [[1673, 2856100]]
assert list_squared(1800,2000) == [[1880, 4884100]]
assert list_squared(2000,2200) == []
assert list_squared(2200,5000) == [[4264, 24304900]]
assert list_squared(5000,10000) == [[6237, 45024100], [9799, 96079204], [9855, 113635600]]



