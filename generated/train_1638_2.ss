longest_palindrome(s): longest_palindrome takes a string s and returns the longest palindrome in s.
'babad' -> 'bab'
'madam' -> 'madam'
'dde' -> 'dd'
'ababbab' -> 'babbab'
'abababa' -> 'abababa'
'banana' -> 'anana'
'abba' -> 'abba'
'cbbd' -> 'bb'
'zz' -> 'zz'
'dddd' -> 'dddd'
'' -> ''
'abcdefghijklmnopqrstuvwxyz' -> 'a'
'ttaaftffftfaafatf' -> 'aaftffftfaa'
'bbaaacc' -> 'aaa'
'm' -> 'm'
  is_palindrome(s): is_palindrome returns True if the string s is the same forwards and backwards, and False otherwise.
  check(li, ri, s): check takes a string s, a left index li, and a right index ri, and returns the longest palindrome that starts at or before li and ends at or after ri.
    is_palindrome
