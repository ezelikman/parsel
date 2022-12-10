case_id(c_str): case_id takes a string and returns a string that is either "kebab", "snake", "camel", or "none" depending on whether the input string is in kebab case, snake case, camel case, or none of the above.
'hello-world' -> 'kebab'
'hello-to-the-world' -> 'kebab'
'hello_world' -> 'snake'
'hello_to_the_world' -> 'snake'
'helloWorld' -> 'camel'
'helloToTheWorld' -> 'camel'
'hello-World' -> 'none'
'hello-To-The-World' -> 'none'
'good-Night' -> 'none'
'he--llo' -> 'none'
'good-night' -> 'kebab'
'good_night' -> 'snake'
'goodNight' -> 'camel'
'hello_World' -> 'none'
'hello_To_The_World' -> 'none'
'he_lloWorld' -> 'none'
'he_lo-lo' -> 'none'
'he-llo--world' -> 'none'
'he-llo--World' -> 'none'
'hello_-World' -> 'none'
  is_snake(s): is_snake takes a string and returns True if the string is snake_case and False otherwise.
  is_kebab(s): is_kebab takes a string and returns True if the string is a kebab-case string, and False otherwise.
  is_camel(s): is_camel returns True if the string s is not lowercase, does not contain dashes, and does not contain underscores.
