# count_pencils takes an integer and returns the pronunciation of "本" in the phrase "N 本".
def count_pencils(n):
    """
    count_pencils takes an integer and returns the pronunciation of "本" in the phrase "N 本".
    :param n: a positive integer not exceeding 999.
    :returns: the pronunciation of "本" in the phrase "N 本".
    """
    return count_pencils_helper(n)

# count_pencils_helper takes an integer and returns the pronunciation of "本" in the phrase "N 本".
def count_pencils_helper(n):
    # convert the integer n to a string
    n_str = str(n)
    # if the last character of n_str is a 2, 4, 5, 7, or 9
    if n_str[-1] in ['2', '4', '5', '7', '9']:
        return 'hon'
    # if the last character of n_str is a 0, 1, 6, or 8
    elif n_str[-1] in ['0', '1', '6', '8']:
        return 'pon'
    # if the last character of n_str is a 3
    elif n_str[-1] in ['3']:
        return 'bon'


assert repr(str(count_pencils('16'))) == repr('pon')
assert repr(str(count_pencils('2'))) == repr('hon')
assert repr(str(count_pencils('183'))) == repr('bon')
assert repr(str(count_pencils('999'))) == repr('hon')
assert repr(str(count_pencils('1'))) == repr('pon')
assert repr(str(count_pencils('440'))) == repr('pon')
assert repr(str(count_pencils('73'))) == repr('bon')
assert repr(str(count_pencils('24'))) == repr('hon')
assert repr(str(count_pencils('438'))) == repr('pon')
assert repr(str(count_pencils('575'))) == repr('hon')
assert repr(str(count_pencils('7'))) == repr('hon')
assert repr(str(count_pencils('3'))) == repr('bon')

