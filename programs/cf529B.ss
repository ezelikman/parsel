main(input_string): Parses the input str to L and returns the minimum area of L. You should only call parse_input and minimum_area which have been implemented. You shouln't redefine them.
"3\n10 1\n20 2\n30 3" -> 180
"3\n3 1\n2 2\n4 3" -> 21
    parse_input(input_string): Takes the input line and first splits on newline. Ignores the first line, and parses each of the remaining lines as a list of two numbers, which give a list L of lists. Returns L.
    "3\n10 1\n20 2\n30 3" -> [[10, 1], [20, 2], [30, 3]]
        parse_line(l): Splits l on space, converts each element to int, and returns the result of converting the result to a list.
        "10 1" -> [10, 1]
    enumerate_subsets_at_most_k(L, k): Returns all subsets of L with sizes ranging from 0 to k, inclusive.
    [1, 2, 3], 2 -> [[], [1], [2], [3], [1, 2], [1, 3], [2, 3]]
        enumerate_subsets(L, k): recusively enumerates the subsets of size k of the list L. Base cases: if k = 0, returns a list containing the empty list. If k > len(L), returns the empty list. Otherwise, first construct the subsets that contain the first element, then those that do not, and return their concatenation.
        [1, 2, 3], 2 -> [[1, 2], [1, 3], [2, 3]]
    minimum_area(whs): First, calls enumerate_subsets_at_most_k passing integer list range from 0 to whs length and half the length of whs rounded down. Returns the minimum result of calling compute_area on the list given by apply_inversions with whs and of the subset.
    [[10, 1], [20, 2], [30, 3]] -> 180
    [[3, 1], [2, 2], [4, 3]] -> 21
        enumerate_subsets_at_most_k
        compute_area(whs): takes a list of pairs (width, height). Computes the sum of the widths and the maximum of the heights. Returns the product of those two numbers.
        [[1, 2], [3, 5]] -> 20
        [[10, 1], [20, 2], [30, 3]] -> 180
        apply_inversions(whs, subset): Takes a list of pairs of form [w, h] and a subset of indices to invert. Returns a list where the elements of whs whose index is in the subset are inverted to [h, w], and the others appear as given.
        [[1, 2], [3, 5]], [1] -> [[1, 2], [5, 3]]
        [[1, 2], [3, 5]], [] -> [[1, 2], [3, 5]]

