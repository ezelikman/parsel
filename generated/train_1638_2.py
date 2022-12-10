# longest_palindrome takes a string s and returns the longest palindrome in s.
def longest_palindrome(s):
    if len(s) <= 1:
        return s
    else:
        longest = s[0]
        for i in range(len(s)):
            for j in range(len(s)):
                if is_palindrome(check(i, j, s)) and len(check(i, j, s)) > len(longest):
                    longest = check(i, j, s)
        return longest

# is_palindrome returns True if the string s is the same forwards and backwards, and False otherwise.
def is_palindrome(s):
    if len(s) <= 1:
        return True
    else:
        return s[0] == s[-1] and is_palindrome(s[1:-1])

# check takes a string s, a left index li, and a right index ri, and returns the longest palindrome that starts at or before li and ends at or after ri.
def check(li, ri, s):
    while li >= 0 and ri < len(s) and s[li] == s[ri]:
        li -= 1
        ri += 1
    return s[li+1:ri]


assert longest_palindrome('babad') == 'bab'
assert longest_palindrome('madam') == 'madam'
assert longest_palindrome('dde') == 'dd'
assert longest_palindrome('ababbab') == 'babbab'
assert longest_palindrome('abababa') == 'abababa'
assert longest_palindrome('banana') == 'anana'
assert longest_palindrome('abba') == 'abba'
assert longest_palindrome('cbbd') == 'bb'
assert longest_palindrome('zz') == 'zz'
assert longest_palindrome('dddd') == 'dddd'
assert longest_palindrome('') == ''
assert longest_palindrome('abcdefghijklmnopqrstuvwxyz') == 'a'
assert longest_palindrome('ttaaftffftfaafatf') == 'aaftffftfaa'
assert longest_palindrome('bbaaacc') == 'aaa'
assert longest_palindrome('m') == 'm'


