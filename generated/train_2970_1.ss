prod_int_part(n): prod_int_part(n) returns a list of two elements, the first element is the number of partitions of n into a product of two integers, the second element is the longest partition of n into a product of two integers.
18 -> [3, [2, 3, 3]]
60 -> [10, [2, 2, 3, 5]]
54 -> [6, [2, 3, 3, 3]]
37 -> [0, []]
61 -> [0, []]
  addPart(n, s): addPart takes a number n and a set of tuples s, and returns a new set of tuples that is the same as s, except that each tuple in s has been extended by adding n to it.
  lastPart(newpart, n): lastPart takes a set of partitions of n and returns a set of partitions of n that are also partitions of n-1.
    is_mult(l, num): is_mult takes a list of numbers and a number and returns True if the product of the numbers in the list is equal to the number, and False otherwise.
    allmult
  allmult(n): allmult(n) returns a set of all unique pairs of integers (a, b) such that 2 <= a <= b <= n/2 and a*b == n.
