from consts import CONSTS
import random

# Parsel representation of a function
class Function:
    def __init__(self, name, args, ret, desc, parent, asserts, prefix=''):
        self.name = name
        self.args = args
        self.ret = ret
        self.desc = desc
        if "default_prefix" in CONSTS:
            prefix = prefix + CONSTS["default_prefix"]
        self.prefix = prefix
        if parent is None:
            self.parents = []
        else:
            self.parents = [parent]
        self.asserts = asserts
        self.children = []
        self.implementations = []
        self.fixed_implementation = None

    # i.e. returns the function signature
    def header(self):
        return CONSTS["header_str"](self.name, self.args)

    # Constructs prompt for code generation
    def get_codex_input(self):
        base_str = ""
        base_str += self.prefix
        already_listed = [self.name]
        for child in self.children:
            if child.name in already_listed:
                continue
            already_listed.append(child.name)
            ret_str = (" -> " + ", ".join(child.ret)) if child.ret else ""
            if isinstance(CONSTS["desc_helper"], str):
                base_str += CONSTS["desc_helper"].format(desc=child.desc)
            else:
                base_str += CONSTS["desc_helper"](child.desc)
            base_str += CONSTS["sig_helper"].format(
                sig=f"{child.name}({', '.join(child.args)}){ret_str}")
            base_str += CONSTS["import"].format(name=child.name)
            base_str += f"\n"
        if self.desc:
            if isinstance(CONSTS["desc_helper"], str):
                base_str += CONSTS["desc_helper"].format(desc=self.desc)
            else:
                base_str += CONSTS["desc_helper"](self.desc)
        if self.ret and ', '.join(self.ret):
            base_str += CONSTS["ret_helper"].format(ret=', '.join(self.ret))
        other_children = [child for child in self.children if child.name != self.name]
        if other_children:
            base_str += CONSTS["use_helper"].format(
                uses=', '.join([child.name for child in other_children]))
        base_str += f"{self.header()}:\n"
        if self.asserts:
            for cur_assert in self.asserts:
                base_str += CONSTS["assert_helper"](cur_assert)
        return base_str

    # Constructs prompt for code generation
    def get_codex_test_input(self):
        base_str = self.get_codex_input()
        base_str += f"""  pass

# check the correctness of {self.name}
assert"""
        return base_str

    # Convert Parsel-style asserts to asserts in the target language
    def get_assert_str(self):
        assert_str = ""
        for cur_assert in self.asserts:
            assert_in, assert_out = CONSTS["assert_break"](cur_assert)
            if isinstance(CONSTS["assert_format"], str):
                assert_str += CONSTS["assert_format"].format(
                    name=self.name, assert_in=assert_in, assert_out=assert_out)
            else:
                assert_str += CONSTS["assert_format"](self.name, assert_in, assert_out)
        return assert_str
    
    # Get the string representation of all implementations of this function
    def get_implementation_strs(self):
        def join_str(strs):
            return "\n".join(strs)
        return [CONSTS["impl_helper"].format(
            header=self.header(),
            impls=join_str(impl),
            asserts=join_str([
                CONSTS["assert_helper"](cur_assert) for cur_assert in self.asserts]),
        ) for impl in self.implementations]

    # Call code model and optionally filter the results
    # Generate implementations for the function
    def implement(self, codex, num_completions=None):
        if 'max_tokens' in CONSTS:
            max_tokens = CONSTS['max_tokens']
        else:
            max_tokens = 500
        if num_completions is None:
            num_completions = CONSTS['num_completions']
        self.implementations = codex.generate(
            codex_in=self.get_codex_input(),
            num_completions=num_completions,
            max_tokens=max_tokens,
            temperature=0.6,
            stop=CONSTS["gen_stop"],
            indented=CONSTS['needs_indent'],
            indented_after_first_line=False,
            require=None,
            cache_key=None,
        )
        self.implementations = list(filter(CONSTS["impl_filter"], self.implementations))
        if "shuffle_implementations" in CONSTS and CONSTS["shuffle_implementations"]:
            random.shuffle(self.implementations)
        self.implementations = self.implementations[:CONSTS['num_completions_eval']]

    # Generate tests for this function
    def generate_tests(self, codex, num_completions=None):
        if num_completions is None:
            num_completions = CONSTS['num_completions']
        tests = codex.generate(
            codex_in=self.get_codex_test_input(),
            num_completions=num_completions * 5,
            max_tokens=100,
            temperature=0.6,
            stop="\n",
            indented=CONSTS['needs_indent'],
            indented_after_first_line=False,
            require=None,
            cache_key=None,
        )
        tests = set([test[0] for test in tests if test])
        self.asserts = tests
        return tests

    # Converts any parent names to references to the actual parent functions
    # Same for children
    # This is because sometimes we need to create references to functions before they are defined
    # Even when they are technically in scope
    # e.g. consider the following valid Parsel program 
    # """
    # a: description1
    #   b
    # b: description2
    # """
    def names_to_fns(self, defined_fns):
        for i, child_name in enumerate(self.children):
            if isinstance(child_name, str):
                self.children[i] = defined_fns[child_name]
                defined_fns[child_name].names_to_fns(defined_fns)
        for i, parent_name in enumerate(self.parents):
            if isinstance(parent_name, str):
                self.parents[i] = defined_fns[parent_name]
                defined_fns[parent_name].names_to_fns(defined_fns)

    # Describe what a function does using code model
    # This is for backtranslation / decompilation
    def describe(self, codex, names_to_avoid=None):
        if names_to_avoid is None:
            names_to_avoid = []
        body_str = f"{self.fixed_implementation}\n"
        body_str += CONSTS["explain_helper"].format(name=self.name)
        gen_desc = codex.generate(body_str, num_completions=1, temperature=0., indented=False)[0]
        new_desc = []
        first_line = True
        for line in gen_desc[:5]:
            line = line.lstrip("#").rstrip()
            if first_line:
                new_desc.append(self.name + line)
                if line.strip().endswith('.'):
                    break
                else:
                    first_line = False
                    continue
            if not line.strip():
                break
            if line.strip().endswith('.'):
                new_desc.append(line.strip())
                break
            new_desc.append(line.strip())
        self.desc = " ".join(new_desc)

    # If the function has no children, we generate children using codex
    def expand(self, codex):
        if self.children:
            return
        body_str = CONSTS["decompose_helper"].format(
            parsel_str=self.to_parsel_str(include_asserts=False).rstrip())
        completions = codex.generate(body_str, num_completions=3, temperature=0.01, indented=False, max_tokens=250, stop=["\n#\n"])
        for completion in completions:
            gen_fns = [gen_fn.split(
                CONSTS["decompose_example_prefix"], 1)[-1] for gen_fn in completion]
            if len(gen_fns) > 3:
                continue
            defined_fns = {self.name: self}
            for gen_fn in gen_fns:
                parse_to_fn(gen_fn, self, defined_fns)
            return defined_fns

    # Add a child to this function
    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)

    # Set the implementation of this function as fixed to a particular string
    def fix_implementation(self, impl_str):
        self.fixed_implementation = impl_str

    # We need to be careful about infinite recursion here
    # Get all functions that are descendants of this function
    def get_descendants(self, visited=None):
        if visited is None:
            visited = {self.name: self}
        for child in self.children:
            if child.name not in visited:
                visited[child.name] = child
                child.get_descendants(visited)
        return visited
    
    # Get all functions that are ancestors of this function
    def get_ancestors(self, visited=None):
        if visited is None:
            visited = {self.name: self}
        for parent in self.parents:
            if parent.name not in visited:
                visited[parent.name] = parent
                parent.get_ancestors(visited)
        return visited
    
    # Check if this function uses another function (even indirectly)
    def uses(self, fn_name):
        return fn_name in self.get_descendants()
    
    # Creates a copy of this function
    def copy(self):
        new_function = Function(
            name=self.name,
            args=self.args.copy(),
            ret=self.ret.copy(),
            desc=self.desc,
            parent=None,
            asserts=self.asserts.copy(),
        )
        new_function.children = self.children.copy()
        new_function.implementations = self.implementations.copy()
        new_function.fixed_implementation = self.fixed_implementation
        new_function.parents = self.parents.copy()
        return new_function

    # Identify functions that are defined by multiple children
    # and move the definition to self
    def rearrange(self, already_defined=None):
        if already_defined is None:
            already_defined = set()
        else:
            already_defined = already_defined.copy()

        # Note that we have defined self and its children
        already_defined.add(self.name)
        for child in self.children:
            already_defined.add(child.name)

        descendant_fns = self.get_descendants()
        # Find all functions that are defined in multiple children
        n_uses = {}
        for fn in descendant_fns.values():
            if fn.name not in already_defined:
                for child in self.children:
                    if child.uses(fn.name):
                        n_uses[fn.name] = n_uses.get(fn.name, 0) + 1
        # Move the definition of each function to self 
        # if it is defined in multiple children
        for fn_name, n in n_uses.items():
            if n > 1:
                fn = descendant_fns[fn_name]
                self.children.insert(0, fn)
                fn.parents.append(self)
                already_defined.add(fn.name)
        for child in self.children:
            # If the child has descendants that are not yet defined,
            # recurse on the child
            child_descendants_set = set(child.get_descendants().keys())
            if not child_descendants_set.issubset(already_defined):
                child.rearrange(already_defined)
    
    # Convert the function and its children to a Parsel string
    def to_parsel_str(self, already_defined=None, override_names=True, include_children=True, include_asserts=True):
        if already_defined is None:
            already_defined = {self.name}
        else:
            already_defined = already_defined.copy()
        outputs = self.ret
        desc = self.desc
        cur_str = f"{self.name}({', '.join(self.args)})"
        if outputs:
            if override_names:
                if len(outputs) == 1:
                    outputs = "res"
                else:
                    outputs = ", ".join(["res" + str(i) for i, _ in enumerate(outputs)])
            else:
                outputs = ", ".join(outputs)
            output_str = f' -> {outputs}'
        else:
            output_str = ""
        cur_str += output_str
        if desc:
            cur_str += ": " + desc
        cur_str += '\n'
        if include_asserts and self.asserts:
            cur_str += '\n'.join(self.asserts) + '\n'
        if not include_children:
            return cur_str

        to_def = []
        to_ref = []
        for child in self.children:
            if child.name not in already_defined:
                already_defined.add(child.name)
                to_def.append(child)
            else:
                to_ref.append(child)

        for child in to_def:
            cur_str += indent_str(child.to_parsel_str(already_defined))
        for child in to_ref:
            if child.name != self.name:
                cur_str += indent_str(child.name)
        return cur_str

    def __repr__(self):
        parent_names = [parent.name for parent in self.parents]
        child_name = [child.name for child in self.children]
        ret_str = f" -> {self.ret}" if self.ret else ""
        return f"Function({self.name}({self.args}){ret_str}); parents: {parent_names}; children: {child_name})"

def indent_str(s, n=2):
    indented_str = ""
    for line in s.splitlines():
        indented_str += ' ' * n + line + '\n'
    return indented_str

def get_function_from_examples(missing_fn_name, examples, parent, codex, include_rets=False):
    examples_str = "\n".join(CONSTS['example_helper'].format(
        example=example) for example in examples)
    generation_str = CONSTS['missing_gen_helper'].format(
        parent_name=parent.name,
        examples_str=examples_str,
        missing_fn_name=missing_fn_name)
    implementations = codex.generate(
        codex_in=generation_str,
        num_completions=CONSTS['num_completions'],
        max_tokens=250,
        temperature=0.2,
        indented_after_first_line=True,
        indented=False)
    sig_lines = [impl[0] for impl in implementations]
    implementations = [impl[1:] for impl in implementations]
    def strip_list(l):
        return [s.strip() for s in l]
    args = [strip_list(sig_line.split(")")[0].split(",")) for sig_line in sig_lines]
    rets = []
    def get_ret(impl):
        for line in impl:
            if CONSTS['fn_end'] in line:
                ret = line.split(CONSTS['fn_end'])[1].strip().split(",")
                ret = strip_list(ret)
                return ret
    if include_rets:
        rets = [get_ret(impl) for impl in implementations]
    else:
        rets = [[] for _ in implementations]
    missing_fns = [
        Function(missing_fn_name, arg, ret, "", parent, [])
        for arg, ret in zip(args, rets)
    ]

    for missing_fn, impl in zip(missing_fns, implementations):
        missing_fn.implementations = [impl]
        impl_str = missing_fn.get_implementation_strs()[0]
        missing_fn.fix_implementation(impl_str)
    return missing_fns

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

def parse_line(line):
    # Parse a function definition
    colon_idx = find_str(line, ":")
    if colon_idx == -1:
        return line, None, None, None
    fn_sig, desc = line[:colon_idx], line[colon_idx + 1:]
    desc = desc.strip()
    if len(fn_sig.split("(", 1)) == 1:
        raise ValueError(f"Invalid function signature: {fn_sig}")
    fn_name, fn_args = fn_sig.split("(", 1)
    if "->" in fn_args:
        fn_args, fn_ret = fn_args.split("->", 1)
        fn_args, fn_ret = fn_args.strip(), fn_ret.strip()
        fn_ret = fn_ret.split(",")
        fn_ret = [ret.strip() for ret in fn_ret]
    else:
        fn_ret = []
    assert fn_args.endswith(")")
    fn_args = fn_args[:-1].split(",")

    fn_args = [arg.strip() for arg in fn_args]
    return fn_name, fn_args, fn_ret, desc

def parse_to_fn(line, parent, defined_fns, scope=None, loose_ref=False, loose_def=False):
    if scope is None:
        scope = defined_fns
    fn_name, fn_args, fn_ret, desc = parse_line(line.strip())
    # print(f"Parsing {fn_name}({fn_args}) -> {fn_ret}")
    # print("Line:", line)
    if fn_name in scope:
        if fn_args is not None:
            failure_output = print if loose_ref else RuntimeError
            failure_output(f"Warning: Function {fn_name} already defined")
            new_fn = defined_fns[fn_name]
            if parent is not None:
                if parent not in new_fn.parents:
                    new_fn.parents.append(parent)
                if new_fn not in parent.children:
                    parent.children.append(new_fn)
            return new_fn
        new_fn = defined_fns[fn_name]
        if parent is not None:
            new_fn.parents.append(parent)
            parent.children.append(new_fn)
        return new_fn
    else:
        if fn_args is not None:
            new_fn = Function(
                name=fn_name,
                args=fn_args,
                ret=fn_ret,
                desc=desc,
                parent=parent,
                asserts=[],
            )
            if parent is not None:
                parent.children.append(new_fn)
                defined_fns[fn_name] = new_fn
                new_fn.prefix = parent.prefix
            return new_fn
        else:
            failure_output = print if loose_def else RuntimeError
            failure_output(f"Function {fn_name} not defined; skipped")
