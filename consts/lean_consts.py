import tempfile
import subprocess
import os

def lean_exec(code):
    # Create a temporary file to store the code
    assert "begin" in code
    assert "sorry" not in code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lean', delete=False) as f:
        f.write(code)
        f.flush()
        # Execute the code
        try:
            subprocess.run(['lean', f.name], check=True)
        except subprocess.CalledProcessError:
            print("Error executing code: ", code)
            raise
        finally:
            os.remove(f.name)

CONSTS = {
    "rate_limit_tokens_text": 16000,
    "exec_pre": "",
    "needs_indent": False,
    "fn_init": "def ",
    "exclude_init": ["from ", "import "],
    "fn_end": "return",
    "gen_stop": ["\nlemma", "\ntheorem", "\nexample", "\nimport"],
    "import": "import {name} helpers\n",
    "header_str": lambda name, arg_list: f"lemma {name}{' '.join(f'({arg})' for arg in arg_list if arg.strip())}",
    "sig_helper": "-- Signature: {sig}\n",
    "desc_helper": "-- Description: {desc}\n",
    "ret_helper": "-- Returns: {ret}\n",
    "use_helper": "-- Applies: {uses}\n",
    "impl_helper": "{header}:\n{asserts}\n{impls}",
    "assert_helper": lambda assertion: "  {assertion} :=".format(
        assertion=assertion.replace('show', '').strip()),
    "assert_check": lambda line: line.strip().startswith('show'),
    "assert_break": lambda cur_assert: (cur_assert, None),
    "assert_format": "-- {assert_in}\n",
    "explain_helper":  "-- Reviewer:\n"
                        "-- Please explain the above function in one sentence with as much detail as possible.\n"
                        "-- In your one-sentence description, specify the range and domain of your function precisely.\n"
                        "-- Your description should be clear enough that someone could reimplement the function from it.\n"
                        "-- Author:\n"
                        "-- Sounds good, here's my one-sentence explanation of {name}:\n"
                        "-- {name}",
    "decompose_helper": "-- Let's decompose this lemma into two lemmas:\n"
                        "-- Lemma to decompose:\n"
                        "-- - {parsel_str}\n"
                        "-- Sublemmas in the same format of 'lamma_name(hypotheses): description':\n",
    "example_helper": "-- {example}\n",
    "missing_gen_helper": "-- Helper function for {parent_name}\n"
                    "-- Usage examples:\n"
                    "-- {examples_str}\n"
                    "-- def {missing_fn_name}(",
    "decompose_example_prefix": " - ",
    'extension': '.lean',
    "output_fn": "-- ({output_str})\n",
    "full_fn_str": "-- {desc}\n{fn_impl}\n",
    "get_assert_in": lambda assert_str: assert_str.split('==')[0].replace('assert', '').strip(),
    "exist_asserts": lambda _: True,
    "exec": lean_exec,
    "impl_filter": lambda impl: "begin" in impl and "sorry" not in impl,
    "implicit_assert": True,
}