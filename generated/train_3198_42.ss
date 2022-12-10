check_exam(arr1, arr2): check_exam takes two lists of equal length and returns the sum of the elements of the first list, where the elements of the second list are either 0, 1, 2, or 3, and the elements of the first list are subtracted by 1 if the corresponding element of the second list is 1, 2, or 3.
['a', 'a', 'b', 'b'],['a', 'c', 'b', 'd'] -> 6
['a', 'a', 'c', 'b'],['a', 'a', 'b', ''] -> 7
['a', 'a', 'b', 'c'],['a', 'a', 'b', 'c'] -> 16
['b', 'c', 'b', 'a'],['', 'a', 'a', 'c'] -> 0
  check0(arr1, arr2): check0 takes two arrays of strings and returns +4 if the first string in the first array is the same as the first string in the second array, 0 if the first string in the second array is empty, and -1 otherwise.
  minus(arr1, arr2): minus takes two arrays of strings and returns the number of strings in the first array that are not in the second array.
  check3(arr1, arr2): check3 takes two arrays of length 4 as input and returns +4 if the fourth element of both arrays is the same, 0 if the fourth element of the second array is empty, and -1 otherwise.
  check2(arr1, arr2): check2 takes two arrays as input and returns +4 if the third element of the first array is equal to the third element of the second array, 0 if the third element of the second array is empty, and -1 otherwise.
  check1(arr1, arr2): check1 takes two arrays as input, and returns +4 if the second element of the first array is equal to the second element of the second array, and returns -1 if the second element of the second array is not empty, and returns 0 otherwise.
