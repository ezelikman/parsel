# capture any string output from a function

# assert_format = """assert repr(str({name}({assert_in}))) == repr(str({assert_out})) or (repr(str_output(lambda: {name}({assert_in}).rstrip())) == repr(str({assert_out})))"""
assert_format = """assert compare_output({name}, {assert_in}, {assert_out})\n"""

exec_imports = (
    "import sys\nimport time\nimport itertools\nfrom itertools import accumulate, product, permutations, "
    "combinations\nimport collections\nfrom collections import Counter, OrderedDict, deque, defaultdict, "
    "ChainMap\nfrom functools import lru_cache\nimport math\nfrom math import sqrt, sin, cos, tan, ceil, "
    "fabs, floor, gcd, exp, log, log2\nimport fractions\nfrom typing import List, Tuple\nimport numpy as "
    "np\nimport random\nimport heapq\n"
)

exec_pre = exec_imports + """
import io, contextlib
def apps_preprocess(input_str):
    # if the input is a list, convert it to a string
    if isinstance(input_str, list):
        input_str = ' '.join([apps_preprocess(x) for x in input_str])
    return str(input_str)

def str_output(fn):
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        ret_val = fn()
        print_val = buf.getvalue()
        return print_val if print_val else ret_val

def compare_output(fn, assert_in, assert_out):
    try:
        assert repr(str_output(lambda: fn(assert_in)).rstrip()) == repr(str(assert_out))
        return True
    except:
        try:
            assert repr(str_output(lambda: fn(apps_preprocess(assert_in))).rstrip()) == repr(str(apps_preprocess(assert_out)))
            return True
        except:
            try:
                assert repr(str_output(lambda: fn(str(assert_in))).rstrip()) == repr(str(str(assert_out)))
                return True
            except:
                try:
                    assert repr(str_output(lambda: fn(assert_in)).rstrip()) == repr(str(assert_out))
                    return True
                except:
                    try:
                        assert repr(str_output(lambda: fn(assert_in)).rstrip()) == repr(str(apps_preprocess(assert_out)))
                        return True
                    except:
                        try:
                            assert abs(float(str_output(lambda: fn(assert_in)).strip()) - float(str(apps_preprocess(assert_out)).strip())) < 1e-6
                            return True
                        except:
                            return False

"""

def eval_fn(fn_str):
    import io, contextlib
    # "import sys\nimport time\nimport itertools\nfrom itertools import accumulate, product, permutations, "
    # "combinations\nimport collections\nfrom collections import Counter, OrderedDict, deque, defaultdict, "
    # "ChainMap\nfrom functools import lru_cache\nimport math\nfrom math import sqrt, sin, cos, tan, ceil, "
    # "fabs, floor, gcd, exp, log, log2\nimport fractions\nfrom typing import List, Tuple\nimport numpy as "
    # "np\nimport random\nimport heapq\nfrom heapq import *\n"
    import sys
    import time
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
    exec(exec_pre + fn_str, locals())
    

CONSTS = {
    "num_completions": 8,
    "text_model_name": "text-davinci-003",
    # "text_model_name": None,
    "num_text_completions": 8,
    "exec_pre": exec_pre,
    "needs_indent": True,
    "fn_init": "def ",
    "exclude_init": ["from ", "import "],
    "fn_end": "return",
    "gen_stop": ["\ndef"],
    "import": "from helpers import {name}\n",
    "header_str": lambda name, args: f"def {name}({', '.join(args)})",
    "sig_helper": "# Signature: {sig}\n",
    "desc_helper": "# Description: {desc}\n",
    "ret_helper": "# Returns: {ret}\n",
    "use_helper": "# Uses: {uses}\n",
    "impl_helper": "{header}:\n{impls}",
    "assert_helper": lambda _: "",
    "assert_check": lambda line: "->" in line and "(" not in line.split("->")[0],
    "assert_break": lambda cur_assert: (cur_assert.split("->")[0].strip(), cur_assert.split("->")[1].strip()),
    "assert_format": assert_format,
    "explain_helper":  "# Reviewer:\n"
                        "# Please explain the above function in one sentence with as much detail as possible.\n"
                        "# In your one-sentence description, specify the range and domain of your function precisely.\n"
                        "# Your description should be clear enough that someone could reimplement the function from it.\n"
                        "# Author:\n"
                        "# Sounds good, here's my one-sentence explanation of {name}:\n"
                        "# {name}",
    "decompose_helper": "# Let's decompose this function into two functions:\n"
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
    "get_assert_in": lambda assert_str: assert_str.split('==')[0].replace('assert', '').replace('.rstrip()', '').strip(),
    "exist_asserts": lambda assert_str: 'assert' in assert_str,
    "exec": eval_fn,
    "impl_filter": lambda _: True,
    "implicit_assert": False,
}