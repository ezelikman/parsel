exec_imports = (
    "import sys\nimport time\nimport itertools\nfrom itertools import accumulate, product, permutations, "
    "combinations\nimport collections\nfrom collections import Counter, OrderedDict, deque, defaultdict, "
    "ChainMap\nfrom functools import lru_cache\nimport math\nfrom math import sqrt, sin, cos, tan, ceil, "
    "fabs, floor, gcd, exp, log, log2\nimport fractions\nfrom typing import List, Tuple\nimport numpy as "
    "np\nimport random\nimport heapq\n"
)

def eval_fn(fn_str):
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
    exec(exec_imports + fn_str, locals())

def prepend_hash(lines_str):
    return "\n".join(["#" + line for line in lines_str.split("\n")])

def find_str(line, target):
    # Find the first : not in parentheses
    paren_count = 0
    bracket_count = 0
    curly_count = 0
    in_string = None
    for i, c in enumerate(line):
        if c == "(":
            paren_count += 1
        elif c == ")":
            paren_count -= 1
        elif c == "[":
            bracket_count += 1
        elif c == "]":
            bracket_count -= 1
        elif c == "{":
            curly_count += 1
        elif c == "}":
            curly_count -= 1
        elif c == "\"" or c == "'":
            if in_string == c:
                in_string = None
            else:
                in_string = c
        elif c == target and paren_count == 0 and bracket_count == 0 and curly_count == 0 and in_string is None:
            return i
    return -1

def assert_check(line):
    line = line.strip()
    return find_str(line, ":") == -1 and "->" in line and (find_str(line, "-") == find_str(line, ">") - 1)

CONSTS = {
    "rate_limit_tokens_text": 16000,
    "num_completions": 16,
    "num_completions_eval": 8,
    "text_model_name": None,
    "num_text_completions": 8,
    "max_text_completions": 8,
    "exec_pre": exec_imports,
    'strict_mode': False,
    "needs_indent": True,
    "eval_mode": False,
    "fn_init": "def ",
    "exclude_init": ["from ", "import "],
    "fn_end": "return",
    "gen_stop": ["\ndef"],
    "default_prefix": "\"\"\"An action plan is a list of strings that describes a sequence of steps to accomplish a task, To be correctly parsed, an action plan must be syntactically correct and contain only allowed actions and recognizable simple objects. Allowed actions: 'close' <arg1>, 'cut' <arg1>, 'drink' <arg1>, 'drop' <arg1>, 'eat' <arg1>, 'find' <arg1>, 'grab' <arg1>, 'greet' <arg1>, 'lie on' <arg1>, 'look at' <arg1>, 'open' <arg1>, 'plug in' <arg1>, 'plug out' <arg1>, 'point at' <arg1>, 'pour' <arg1> 'into' <arg2>, 'pull' <arg1>, 'push' <arg1>, 'put' <arg1> 'on' <arg2>, 'put' <arg1> 'in' <arg2>, 'put back' <arg1>, 'take off' <arg1>, 'put on' <arg1>, 'read' <arg1>, 'release', 'rinse' <arg1>, 'run to'  <arg1>, 'scrub' <arg1>, 'sit on' <arg1>, 'sleep', 'squeeze' <arg1>, 'stand up', 'switch off' <arg1>, 'switch on' <arg1>, 'touch' <arg1>, 'turn to' <arg1>, 'type on' <arg1>, 'wake up', 'walk to' <arg1>, 'wash' <arg1>, 'watch' <arg1>, 'wipe' <arg1>. To satisfy the common-sense constraints, each action step in this action plan must not violate the set of its pre-conditions (e.g. the agent cannot grab milk from the fridge before opening it) and post-conditions (e.g. the state of the fridge changes from \“closed\” to \“open\” after the agent opens it).\"\"\"\n",
    "import": "from helpers import {name}\n",
    "header_str": lambda name, args: f"def {name}({', '.join(args)})",
    "sig_helper": "# Signature: {sig}\n",
    "desc_helper": lambda desc: prepend_hash(f" Description: {desc}") + "\n",
    "ret_helper": "# Returns: {ret}\n",
    "use_helper": "# Uses: {uses}\n",
    "impl_helper": "{header}:\n{impls}",
    "assert_helper": lambda _: "",
    "assert_check": assert_check,
    "assert_break": lambda cur_assert: (cur_assert.split("->")[0].strip(), cur_assert.split("->")[1].strip()),
    "assert_format": "from execute_virtual_home import test_script;assert test_script({name}({assert_in}))\n",
    "explain_helper":  "# Reviewer:\n"
                        "# Please explain the above function in one sentence with as much detail as possible.\n"
                        "# In your one-sentence description, specify the range and domain of your function precisely.\n"
                        "# Your description should be clear enough that someone could reimplement the function from it.\n"
                        "# Author:\n"
                        "# Sounds good, here's my one-sentence explanation of {name}:\n"
                        "# {name}",
    "decompose_helper": "# Let's decompose this function into at most three functions:\n"
                        "# Function to decompose:\n"
                        "# - {parsel_str}\n"
                        "# Necessary helper functions in the same format of 'fn_name(inputs): description':\n",
    "example_helper": "# {example}\n",
    "missing_gen_helper": "# Helper function for {parent_name}\n"
                    "# Usage examples:\n"
                    "# {examples_str}\n"
                    "# def {missing_fn_name}(",
    "decompose_example_prefix": " - ",
    'extension': '.py',
    "output_fn": "print({output_str})\n",
    "full_fn_str": "# {desc}\n{fn_impl}\n",
    "get_assert_in": lambda assert_str: assert_str.split('==')[0].replace('assert', '').strip(),
    "exist_asserts": lambda assert_str: 'assert' in assert_str,
    "exec": eval_fn,
    "impl_filter": lambda _: True,
    "implicit_assert": False,
}