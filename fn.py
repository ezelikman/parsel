from consts import CONSTS

class Function:
    def __init__(self, name, args, ret, desc, parent, asserts):
        self.name = name
        self.args = args
        self.ret = ret
        self.desc = desc
        if parent is None:
            self.parents = []
        else:
            self.parents = [parent]
        self.asserts = asserts
        self.children = []
        self.implementations = []
        self.fixed_implementation = None

    def header(self):
        return CONSTS["header_str"].format(name=self.name, args=', '.join(self.args))

    def get_codex_input(self):
        base_str = ""
        for child in self.children:
            ret_str = (" -> " + ", ".join(child.ret))# if child.ret else ""
            base_str += f"from helpers import {child.name}\n"
            base_str += f"# Description: {child.desc}\n"
            base_str += f"# Signature: {child.name}({', '.join(child.args)}){ret_str}\n"
            base_str += f"\n"
        if self.desc:
            base_str += CONSTS["desc_helper"].format(desc=self.desc)
        if self.ret and ', '.join(self.ret):
            base_str += CONSTS["ret_helper"].format(ret=', '.join(self.ret))
        if self.children:
            base_str += CONSTS["use_helper"].format(
                uses=', '.join([child.name for child in self.children]))
        base_str += f"{self.header()}:\n"
        return base_str

    def get_assert_str(self):
        assert_str = ""
        for cur_assert in self.asserts:
            assert_in, assert_out = cur_assert.split("->")
            assert_in = assert_in.strip()
            assert_out = assert_out.strip()
            assert_str += CONSTS["assert_format"].format(
                name=self.name, assert_in=assert_in, assert_out=assert_out)
        return assert_str
    
    def get_implementation_strs(self):
        def join_str(strs):
            return "\n".join(strs)
        return [f"{self.header()}:\n{join_str(impl)}" for impl in self.implementations]

    def implement(self, codex):
        self.implementations = codex.generate(
            codex_in=self.get_codex_input(),
            num_completions=8,
            max_tokens=500,
            # num_completions=16,
            # max_tokens=250,
            temperature=0.5,
            stop=["\ndef"],
            indented=True,
            indented_after_first_line=False,
            require=None,
            cache_key=None,
        )
    
    def names_to_fns(self, defined_fns):
        for i, child_name in enumerate(self.children):
            if isinstance(child_name, str):
                self.children[i] = defined_fns[child_name]
                defined_fns[child_name].names_to_fns(defined_fns)
        for i, parent_name in enumerate(self.parents):
            if isinstance(parent_name, str):
                self.parents[i] = defined_fns[parent_name]
                defined_fns[parent_name].names_to_fns(defined_fns)

    def describe(self, codex, names_to_avoid=None):
        if names_to_avoid is None:
            names_to_avoid = []
        body_str = f"{self.fixed_implementation}\n"
        body_str += CONSTS["describe_helper"].format(name=self.name)
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
        gen_fns = codex.generate(body_str, num_completions=1, temperature=0., indented=False, max_tokens=250, stop=["\n#\n"])[0]
        gen_fns = [gen_fn.split(
            CONSTS["decompose_example_prefix"], 1)[-1] for gen_fn in gen_fns]
        defined_fns = {self.name: self}
        for gen_fn in gen_fns:
            parse_to_fn(gen_fn, self, defined_fns)
        return defined_fns

    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)

    def fix_implementation(self, impl_str):
        self.fixed_implementation = impl_str

    # We need to be careful about infinite recursion here
    def get_descendants(self, visited=None):
        if visited is None:
            visited = {self.name: self}
        for child in self.children:
            if child.name not in visited:
                visited[child.name] = child
                child.get_descendants(visited)
        return visited
    
    def uses(self, fn_name):
        return fn_name in self.get_descendants()
    
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
        num_completions=16,
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

def parse_line(line):
    # Parse a function definition
    if ":" not in line:
        return line, None, None, None
    fn_sig, desc = line.split(":", 1)
    desc = desc.strip()
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

def parse_to_fn(line, parent, defined_fns, scope=None):
    if scope is None:
        scope = defined_fns
    fn_name, fn_args, fn_ret, desc = parse_line(line.strip())
    if fn_name in scope:
        if fn_args is not None:
            raise RuntimeError(f"Function {fn_name} already defined")
        new_fn = defined_fns[fn_name]
        if parent is not None:
            new_fn.parents.append(parent)
            parent.children.append(new_fn)
        return defined_fns[fn_name]
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
            return new_fn
        else:
            raise RuntimeError(f"Function {fn_name} not defined")