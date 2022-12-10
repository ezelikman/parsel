# find_2nd_largest takes a list of numbers and returns the second largest number in the list.
def find_2nd_largest(arr):
    if len(arr) == 1:
        return None
    arr = filter_int(arr)
    if len(arr) == 0:
        return None
    if len(arr) == 1:
        return arr[0]
    arr = sort(arr)
    if is_diff(arr) == False:
        return None
    res = arr[len(arr) - 2]
    return res

# filter_int takes an array of integers and returns an array of integers.
def filter_int(arr):
    return list(filter(lambda x: type(x) == int, arr))

# sec_big takes two numbers and returns the smaller of the two.
def sec_big(a, b):
    if a > b:
        return b
    else:
        return a

# sort takes an array of numbers and returns a sorted array of numbers.
def sort(arr):
    return sorted(arr)

# is_diff takes an array of numbers and returns True if there are any two numbers in the array that are different, and False if all the numbers in the array are the same.
def is_diff(arr):
    for i in range(len(arr) - 1):
        if arr[i] != arr[i + 1]:
            return True
    return False


assert find_2nd_largest([1, 2, 3]) == 2
assert find_2nd_largest([1, 1, 1, 1, 1, 1, 1]) == None
assert find_2nd_largest([1, 'a', '2', 3, 3, 4, 5, 'b']) == 4
assert find_2nd_largest([1, 'a', '2', 3, 3, 3333333333333333333334, 544444444444444444444444444444, 'b']) == 3333333333333333333334




