gap(g, m, n): gap takes in three integers, g, m, and n, and returns a list of two integers, [i, i + g], where i is the smallest prime number in the range [m, n] such that i + g is also prime, and there are no prime numbers in the range [i + 1, i + g - 1].
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
  allprimes(start, end): allprimes(start,end) returns a list of all prime numbers between start and end, inclusive.
    prime
  prime(a): prime(a) returns True if a is a prime number, and False otherwise.
