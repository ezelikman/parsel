# case_id takes a string and returns a string that is either "kebab", "snake", "camel", or "none" depending on whether the input string is in kebab case, snake case, camel case, or none of the above.
def case_id(c_str):
    if is_snake(c_str) == True:
        return "snake"
    elif is_kebab(c_str) == True:
        return "kebab"
    elif is_camel(c_str) == True:
        return "camel"
    else:
        return "none"

# is_snake takes a string and returns True if the string is snake_case and False otherwise.
def is_snake(s):
    if s[0].isalpha() and s[0].islower() and len(s) > 1:
        for char in s:
            if char.isalpha():
                if char.isupper():
                    return False
            elif char == '_':
                pass
            else:
                return False
        return True
    else:
        return False

# is_kebab takes a string and returns True if the string is a kebab-case string, and False otherwise.
def is_kebab(s):
    # if s is empty, False
    if s == '':
        return False
    # if s is not a string, False
    if type(s) != str:
        return False
    # if s is not lowercase, False
    if s != s.lower():
        return False
    # if s contains anything other than a-z or -, False
    for c in s:
        if not (c.isalpha() or c == '-'):
            return False
    # if s contains a - at the beginning or end, False
    if s[0] == '-' or s[-1] == '-':
        return False
    # if s contains more than one - in a row, False
    for i in range(len(s)-1):
        if s[i] == '-' and s[i+1] == '-':
            return False
    # otherwise, True
    return True


# is_camel returns True if the string s is not lowercase, does not contain dashes, and does not contain underscores.
def is_camel(s):
    return s != s.lower() and s.find('_') == -1 and s.find('-') == -1


assert case_id('hello-world') == 'kebab'
assert case_id('hello-to-the-world') == 'kebab'
assert case_id('hello_world') == 'snake'
assert case_id('hello_to_the_world') == 'snake'
assert case_id('helloWorld') == 'camel'
assert case_id('helloToTheWorld') == 'camel'
assert case_id('hello-World') == 'none'
assert case_id('hello-To-The-World') == 'none'
assert case_id('good-Night') == 'none'
assert case_id('he--llo') == 'none'
assert case_id('good-night') == 'kebab'
assert case_id('good_night') == 'snake'
assert case_id('goodNight') == 'camel'
assert case_id('hello_World') == 'none'
assert case_id('hello_To_The_World') == 'none'
assert case_id('he_lloWorld') == 'none'
assert case_id('he_lo-lo') == 'none'
assert case_id('he-llo--world') == 'none'
assert case_id('he-llo--World') == 'none'
assert case_id('hello_-World') == 'none'



