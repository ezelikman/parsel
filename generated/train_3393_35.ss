list_squared(m, n): list_squared(m, n) returns a list of lists of integers, where each sublist contains an integer and its sum of squared divisors, and the integers are in the range [m, n] (inclusive).
1,250 -> [[1, 1], [42, 2500], [246, 84100]]
42,250 -> [[42, 2500], [246, 84100]]
250,500 -> [[287, 84100]]
300,600 -> []
600,1500 -> [[728, 722500], [1434, 2856100]]
1500,1800 -> [[1673, 2856100]]
1800,2000 -> [[1880, 4884100]]
2000,2200 -> []
2200,5000 -> [[4264, 24304900]]
5000,10000 -> [[6237, 45024100], [9799, 96079204], [9855, 113635600]]
  divisors_list(num): divisors_list takes a number and returns a list of all the divisors of that number.
  sum_squares(nums): sum_squares takes a list of numbers and returns the sum of the squares of those numbers.
  isSquarable(num): isSquarable takes a number and returns True if the number is a perfect square, and False otherwise.
