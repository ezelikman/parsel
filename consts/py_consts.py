from contextlib import redirect_stdout

vis = False

exec_imports = (
    "import sys\nimport time\nimport itertools\nfrom itertools import accumulate, product, permutations, "
    "combinations\nimport collections\nfrom collections import Counter, OrderedDict, deque, defaultdict, "
    "ChainMap\nfrom functools import lru_cache\nimport math\nfrom math import sqrt, sin, cos, tan, ceil, "
    "fabs, floor, gcd, exp, log, log2\nimport fractions\nfrom typing import List, Tuple\nimport numpy as "
    "np\nimport random\nimport heapq\n"
)

if vis:
    exec_imports += "import clip\nfrom PIL import Image\n"
    exec_imports += "import torch\nfrom torch import nn\nfrom torch.nn import functional as F\n"

def eval_fn(fn_str):
    if vis:
        import clip
        from PIL import Image
        import torch
        from torch import nn
        from torch.nn import functional as F
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
    f = io.StringIO()
    with redirect_stdout(f):
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

def assert_break(cur_assert):
    if "->" not in cur_assert:
        return cur_assert, None
    return (cur_assert.split("->")[0].strip(), cur_assert.split("->")[1].strip())

def assert_format(name, assert_in, assert_out):
    if assert_out is not None:
        return f"assert repr(str({name}({assert_in}))) == repr(str({assert_out})) or ({name}({assert_in}) == {assert_out})\n"
    return f"assert {assert_in}\n"

CONSTS = {
    "rate_limit_tokens_text": 16000,
    "num_completions": 64,
    "min_completions": 8,
    "num_completions_eval": 64,
    "text_model_name": None,
    "timeout": 0.5,
    "shuffle_always": True,
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
    "import": "from helpers import {name}\n",
    "header_str": lambda name, args: f"def {name}({', '.join(args)})",
    "sig_helper": "# Signature: {sig}\n",
    "desc_helper": lambda desc: prepend_hash(f" Description: {desc}") + "\n",
    "ret_helper": "# Returns: {ret}\n",
    "use_helper": "# Uses: {uses}\n",
    "impl_helper": "{header}:\n{impls}",
    "assert_helper": lambda _: "",
    "assert_check": assert_check,
    "assert_break": assert_break,
    "assert_format": assert_format,
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
