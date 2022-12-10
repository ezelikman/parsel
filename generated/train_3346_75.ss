gap(g, m, n): gap(g, m, n) returns the first pair of prime numbers in the range [m, n] that have a difference of g.
2,3,10 -> [3, 5]
3,3,10 -> None
2,100,110 -> [101, 103]
4,100,110 -> [103, 107]
6,100,110 -> None
8,300,400 -> [359, 367]
10,300,400 -> [337, 347]
4,30000,100000 -> [30109, 30113]
6,30000,100000 -> [30091, 30097]
8,30000,100000 -> [30161, 30169]
11,30000,100000 -> None
2,10000000,11000000 -> [10000139, 10000141]
  get_next_prime_number(start, end): get_next_prime_number takes a start and end number and returns the next prime number in that range.
    check_prime_number(n): check_prime_number(n) returns True if n is a prime number, and False otherwise.
