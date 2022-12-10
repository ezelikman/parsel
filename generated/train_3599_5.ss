find_f1_eq_f2(n, k): find_f1_eq_f2 is a function that takes in two integers, n and k, and returns the smallest integer n_i such that f1(n_i,k) == f2(n_i,k).
542,5 -> 547
1750,6 -> 1799
14990,7 -> 14996
3456,4 -> 3462
30500,3 -> 30501
62550,5 -> 62557
568525,7 -> 568531
9567100,8 -> 9567115
  f2(n, k): f2 takes a positive integer n and a positive integer k, and returns the smallest positive integer n_i such that n_i is a multiple of n and the digits of n_i are a permutation of the digits 0, 1, ..., k-1.
  f1(n, k): f1 takes a positive integer n and a positive integer k, and returns the smallest positive integer n_i such that n_i is a multiple of n and all digits of n_i are less than k.
