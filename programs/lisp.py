import io, contextlib
import sys
import time
import resource
import itertools
from itertools import accumulate, product, permutations, combinations
import collections
from collections import Counter, OrderedDict, deque, defaultdict, ChainMap
from functools import lru_cache
import math
from math import sqrt, sin, cos, tan, ceil, fabs, floor, gcd, exp, log, log2
import fractions
from typing import List, Tuple
import numpy as np
import random
import heapq

# Return a new env inside env with parms mapped to their corresponding args, and env as the new env's outer env.
def get_env(parms, args, env=None):
    new_env = {'_outer':env}
    for (parm, arg) in zip(parms, args):
        new_env[parm] = arg
    return new_env

# Get a dictionary mapping math library function names to their functions.
def get_math():
    d = {}
    for name in dir(math):
        if name[:2] != '__':
            d[name] = getattr(math, name)
    return d

# Get a dictionary mapping operator symbols to their functions: +, -, *, /, >, <, >=, <=, =.
def get_ops():
    return {
        "+" : (lambda x,y: x+y),
        "-" : (lambda x,y: x-y),
        "*" : (lambda x,y: x*y),
        "/" : (lambda x,y: x/y),
        ">" : (lambda x,y: x>y),
        "<" : (lambda x,y: x<y),
        ">=": (lambda x,y: x>=y),
        "<=": (lambda x,y: x<=y),
        "=": (lambda x,y: x==y)
    }
# Get a dictionary mapping 'abs', 'min', 'max', 'not', 'round' to their functions.
def get_simple_math():
    return {'abs':abs, 'min':min, 'max':max, 'not':lambda x: not x, 'round':round}

# Return the value of fn_dict_generator()[key](*args_list) in standard_env.
def apply_fn_dict_key(fn_dict_generator, key, args_list):
    fn_dict = fn_dict_generator()
    return fn_dict[key](*args_list)

# An environment with some Scheme standard procedures. Start with an environment and update it with standard functions.
def standard_env(includes=['math', 'ops', 'simple_math']):
    env = {'_outer': None}
    if 'math' in includes:
        env.update(get_math())
    if 'ops' in includes:
        env.update(get_ops())
    if 'simple_math' in includes:
        env.update(get_simple_math())
    return env

# Find the value of var in the innermost env where var appears.
def find(env, var):
    if var in env:
        return env[var]
    else:
        return find(env['_outer'], var)

# Return find(env, x).
def string_case(x, env):
    return find(env, x)

# Gets a procedure and returns the result of evaluating proc(*args) in env. Should not be called directly.
def eval_procedure(parms, body, env, args):
    proc = get_procedure(parms, body, env)
    new_env = get_env(parms, args, env)
    return eval_exp(body, new_env)

# Return a procedure which evaluates body in a new environment with parms bound to the args passed to the procedure (in the same order as parms).
def get_procedure(parms, body, env):
    return lambda *args: eval_procedure(parms, body, env, args)
 

# Get the procedure by evaluating the first value of x. Then, evaluate the arguments and apply the procedure to them. Return the result.
def otherwise_case(x, env):
    p = eval_exp(x[0], env)
    args = [eval_exp(arg, env) for arg in x[1:]]
    return p(*args)

# Handle the function specified by the first value of x. Handle the first value of x being quote, if, define, set!, lambda, or otherwise. Return the result.
def list_case(x, env):
    if x[0] == 'quote':
        return x[1]
    elif x[0] == 'if':
        if eval_exp(x[1], env):
            return eval_exp(x[2], env)
        elif len(x) == 4:
            return eval_exp(x[3], env)
    elif x[0] == 'define':
        env[x[1]] = eval_exp(x[2], env)
    elif x[0] == 'set!':
        env.find(x[1])[x[1]] = eval_exp(x[2], env)
    elif x[0] == 'lambda':
        return get_procedure(x[1], x[2], env)
    else:
        proc = eval_exp(x[0], env)
        args = [ eval_exp(arg, env) for arg in x[1:] ]
        return proc(*args)

# Return x
def not_list_case(x, env):
    if isinstance(x, list):
        return None
    return x

# Evaluate an expression in an environment and return the result. Check if x is a list, a string, or neither, and call the corresponding function.
def eval_exp(x, env):
    if isinstance(x, list):
        return list_case(x, env)
    elif isinstance(x, str):
        return string_case(x, env)
    else:
        return not_list_case(x, env)
# Convert a string into a list of tokens, including parens.
def tokenize(s):
    "Convert a string into a list of tokens, including parens."
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

# Numbers become numbers; every other token is a string.
def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return token
# Translate tokens to their corresponding atoms, using parentheses for nesting lists.
def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)
    
# Read a Scheme expression from a string.
def parse(program):
    return read_from_tokens(tokenize(program))

# Convert a nested list into a string with nesting represented by parentheses.
def nested_list_to_str(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(nested_list_to_str, exp)) + ')'
    else:
        return str(exp)
# Parse an expression, return the result.
def parse_and_update(expression, env):
    exp = parse(expression)
    result = eval_exp(exp, env)
    return nested_list_to_str(result)

# Initialize a standard environment. Parse and evaluate a list of expressions, returning the final result.
def evaluate_program(program):
    env = standard_env()
    last = None
    for expression in program:
        last = parse_and_update(expression, env)
    return last


assert repr(str(evaluate_program(['(define square (lambda (r) (* r r)))', '(square 3)']))) == repr(str(9)) or (evaluate_program(['(define square (lambda (r) (* r r)))', '(square 3)']) == 9)

assert repr(str(get_env([], []))) == repr(str({'_outer': None})) or (get_env([], []) == {'_outer': None})
assert repr(str(get_env(['a'], [1]))) == repr(str({'a': 1, '_outer': None})) or (get_env(['a'], [1]) == {'a': 1, '_outer': None})

assert repr(str(standard_env([]))) == repr(str({'_outer': None})) or (standard_env([]) == {'_outer': None})

assert repr(str(parse_and_update("(+ 1 (* 2 3))", {'+': (lambda x, y: x + y), '*': (lambda x, y: x * y), '_outer': None}))) == repr(str(7)) or (parse_and_update("(+ 1 (* 2 3))", {'+': (lambda x, y: x + y), '*': (lambda x, y: x * y), '_outer': None}) == 7)




assert repr(str(apply_fn_dict_key(get_math, 'sqrt', [4]))) == repr(str(2.0)) or (apply_fn_dict_key(get_math, 'sqrt', [4]) == 2.0)
assert repr(str(apply_fn_dict_key(get_ops, '+', [1, 2]))) == repr(str(3)) or (apply_fn_dict_key(get_ops, '+', [1, 2]) == 3)
assert repr(str(apply_fn_dict_key(get_simple_math, 'abs', [-1]))) == repr(str(1)) or (apply_fn_dict_key(get_simple_math, 'abs', [-1]) == 1)

assert repr(str(eval_exp(1, {'_outer': None}))) == repr(str(1)) or (eval_exp(1, {'_outer': None}) == 1)

assert repr(str(parse('(1 + (2 * 3))'))) == repr(str([1, '+', [2, '*', 3]])) or (parse('(1 + (2 * 3))') == [1, '+', [2, '*', 3]])

assert repr(str(nested_list_to_str(1))) == repr(str("1")) or (nested_list_to_str(1) == "1")
assert repr(str(nested_list_to_str([1, '+', [2, '*', 3]]))) == repr(str("(1 + (2 * 3))")) or (nested_list_to_str([1, '+', [2, '*', 3]]) == "(1 + (2 * 3))")

assert repr(str(find({'a':4, '_outer':None}, 'a'))) == repr(str(4)) or (find({'a':4, '_outer':None}, 'a') == 4)
assert repr(str(find({'_outer':{'a':4, '_outer':None}}, 'a'))) == repr(str(4)) or (find({'_outer':{'a':4, '_outer':None}}, 'a') == 4)
assert repr(str(find({'a':3, '_outer':{'a':4, '_outer':None}}, 'a'))) == repr(str(3)) or (find({'a':3, '_outer':{'a':4, '_outer':None}}, 'a') == 3)

assert repr(str(string_case('a', {'a':4, '_outer':None}))) == repr(str(4)) or (string_case('a', {'a':4, '_outer':None}) == 4)

assert repr(str(list_case(['quote', 'a'], {'_outer': None}))) == repr(str('a')) or (list_case(['quote', 'a'], {'_outer': None}) == 'a')
assert repr(str(list_case(['if', True, 1, 2], {'_outer': None}))) == repr(str(1)) or (list_case(['if', True, 1, 2], {'_outer': None}) == 1)
assert repr(str(list_case(['define', 'a', 1], {'_outer': None}))) == repr(str(None)) or (list_case(['define', 'a', 1], {'_outer': None}) == None)

assert repr(str(not_list_case(1, {}))) == repr(str(1)) or (not_list_case(1, {}) == 1)


assert repr(str(otherwise_case(['+', 1, 2], {'+': (lambda x, y: x + y), '_outer': None}))) == repr(str(3)) or (otherwise_case(['+', 1, 2], {'+': (lambda x, y: x + y), '_outer': None}) == 3)

assert repr(str(eval_procedure(['r'], ['*', 'pi', ['*', 'r', 'r']], {'*': (lambda x, y: x * y), 'pi': 3, '_outer': None}, [1]))) == repr(str(3)) or (eval_procedure(['r'], ['*', 'pi', ['*', 'r', 'r']], {'*': (lambda x, y: x * y), 'pi': 3, '_outer': None}, [1]) == 3)

assert repr(str(tokenize("1 + 2"))) == repr(str(['1', '+', '2'])) or (tokenize("1 + 2") == ['1', '+', '2'])
assert repr(str(tokenize("1 + (2 * 3)"))) == repr(str(['1', '+', '(', '2', '*', '3', ')'])) or (tokenize("1 + (2 * 3)") == ['1', '+', '(', '2', '*', '3', ')'])

assert repr(str(read_from_tokens(['(', '1', '+', '(', '2', '*', '3', ')', ')']))) == repr(str([1, '+', [2, '*', 3]])) or (read_from_tokens(['(', '1', '+', '(', '2', '*', '3', ')', ')']) == [1, '+', [2, '*', 3]])

assert repr(str(atom("1"))) == repr(str(1)) or (atom("1") == 1)
assert repr(str(atom("a"))) == repr(str("a")) or (atom("a") == "a")
assert repr(str(atom("1.2"))) == repr(str(1.2)) or (atom("1.2") == 1.2)
