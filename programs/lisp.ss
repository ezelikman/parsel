An env is a dictionary of {'var':val} pairs, with a link to its outer environment in env['_outer'].
A procedure is a lambda expression, with parms, body, and env which calls eval_exp on the body.
#*#*#
evaluate_program(program): Initialize a standard environment. Parse and evaluate a list of expressions, returning the final result.
['(define square (lambda (r) (* r r)))', '(square 3)'] -> 9
  get_env(parms, args, env=None): Return a new env inside env with parms mapped to their corresponding args, and env as the new env's outer env.
  [], [] -> {'_outer': None}
  ['a'], [1] -> {'a': 1, '_outer': None}
  standard_env(includes=['math','ops','simple_math']): An environment with some Scheme standard procedures. Start with an environment and update it with standard functions.
  [] -> {'_outer': None}
    get_math(): Get a dictionary mapping math library function names to their functions.
    get_ops(): Get a dictionary mapping operator symbols to their functions: +, -, *, /, >, <, >=, <=, =.
    get_simple_math(): Get a dictionary mapping 'abs', 'min', 'max', 'not', 'round' to their functions.
    apply_fn_dict_key(fn_dict_generator, key, args_list): Return the value of fn_dict_generator()[key](*args_list) in standard_env.
    get_math, 'sqrt', [4] -> 2.0
    get_ops, '+', [1, 2] -> 3
    get_simple_math, 'abs', [-1] -> 1
      get_math
      get_ops
      get_simple_math
  parse_and_update(expression, env): Parse an expression, return the result.
  "(+ 1 (* 2 3))", {'+': (lambda x, y: x + y), '*': (lambda x, y: x * y), '_outer': None} -> 7
    eval_exp(x, env): Evaluate an expression in an environment and return the result. Check if x is a list, a string, or neither, and call the corresponding function.
    1, {'_outer': None} -> 1
      find(env, var): Find the value of var in the innermost env where var appears.
      {'a':4, '_outer':None}, 'a' -> 4
      {'_outer':{'a':4, '_outer':None}}, 'a' -> 4
      {'a':3, '_outer':{'a':4, '_outer':None}}, 'a' -> 3
      string_case(x, env): Return find(env, x).
      'a', {'a':4, '_outer':None} -> 4
        find
      list_case(x, env): Handle the function specified by the first value of x. Handle the first value of x being quote, if, define, set!, lambda, or otherwise. Return the result.
      ['quote', 'a'], {'_outer': None} -> 'a'
      ['if', True, 1, 2], {'_outer': None} -> 1
      ['define', 'a', 1], {'_outer': None} -> None
        get_procedure(parms, body, env): Return a procedure which evaluates body in a new environment with parms bound to the args passed to the procedure (in the same order as parms).
          eval_procedure(parms, body, env, args): Gets a procedure and returns the result of evaluating proc(*args) in env. Should not be called directly.
          ['r'], ['*', 'pi', ['*', 'r', 'r']], {'*': (lambda x, y: x * y), 'pi': 3, '_outer': None}, [1] -> 3
            get_procedure
            get_env
            eval_exp
        otherwise_case(x, env): Get the procedure by evaluating the first value of x. Then, evaluate the arguments and apply the procedure to them. Return the result.
        ['+', 1, 2], {'+': (lambda x, y: x + y), '_outer': None} -> 3
          eval_exp
        eval_exp
      not_list_case(x, env): Return x
      1, {} -> 1
    parse(program): Read a Scheme expression from a string.
    '(1 + (2 * 3))' -> [1, '+', [2, '*', 3]]
      tokenize(s): Convert a string into a list of tokens, including parens.
      "1 + 2" -> ['1', '+', '2']
      "1 + (2 * 3)" -> ['1', '+', '(', '2', '*', '3', ')']
      read_from_tokens(tokens): Translate tokens to their corresponding atoms, using parentheses for nesting lists.
      ['(', '1', '+', '(', '2', '*', '3', ')', ')'] -> [1, '+', [2, '*', 3]]
        atom(token): Numbers become numbers; every other token is a string.
        "1" -> 1
        "a" -> "a"
        "1.2" -> 1.2
    nested_list_to_str(exp): Convert a nested list into a string with nesting represented by parentheses.
    1 -> "1"
    [1, '+', [2, '*', 3]] -> "(1 + (2 * 3))"
