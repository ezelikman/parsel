CONSTS = {
    "fn_init": "def ",
    "exclude_init": ["from ", "import "],
    "fn_end": "return",
    "header_str": "def {name}({args})",
    "desc_helper": "# Description: {desc}\n",
    "ret_helper": "# Returns: {ret}\n",
    "use_helper": "# Uses: {uses}\n",
    "assert_format": "assert repr(str({name}({assert_in}))) == repr({assert_out})\n",
    "describe_helper":  "# Reviewer:\n"
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
}