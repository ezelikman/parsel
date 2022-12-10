import argparse
from codex import CodeGen
from graph import get_graph, strongly_connected_components
import itertools
from fn import get_function_from_examples
import concurrent.futures
from tqdm import tqdm
import random
from consts import CONSTS

# When a function is called but not defined, we can try to
# infer its implementation from the other functions in the
# same SCC.
def fill_in_missing_fn(missing_fn_name, scc, defined_fns, implementation_set, implementation_attempt, codegen):
    usage_examples = set()
    using_fns = set()
    for fn_name, implementation in zip(scc, implementation_set):
        for line in implementation.splitlines():
            if missing_fn_name in line:
                usage_examples.add(line.strip())
                using_fns.add(fn_name)
    parent = defined_fns[list(using_fns)[0]]
    missing_fn_attempts = get_function_from_examples(missing_fn_name, usage_examples, parent, codegen)
    for missing_fn_attempt in missing_fn_attempts:
        try:
            impl_str = missing_fn_attempt.get_implementation_strs()[0]
            new_implementation_attempt = impl_str + "\n" + implementation_attempt
            exec(new_implementation_attempt, locals())
            defined_fns[missing_fn_name] = missing_fn_attempt
            # Let all functions using the missing function know about their new child
            missing_fn_attempt.parent = []
            for fn_name in using_fns:
                defined_fns[fn_name].add_child(missing_fn_attempt)
            for fn_name, implementation in zip(scc, implementation_set):
                fn = defined_fns[fn_name]
                if fn.fixed_implementation is None:
                    fn.fix_implementation(implementation)
            return new_implementation_attempt
        except:
            continue

def implement_set(implementation_set, dependencies_str, asserts_str, verbose=True, catch_name_exceptions=False):
    implementation_attempt = dependencies_str
    for fn_implementation in implementation_set:
        implementation_attempt += fn_implementation + "\n"
    for assert_str in asserts_str.splitlines():
        exec_implementation_attempt = implementation_attempt
        if verbose:
            assert_in = CONSTS["get_assert_in"](assert_str)
            exec_implementation_attempt += CONSTS["output_fn"].format(output_str=assert_in)
        exec_implementation_attempt += assert_str
        if verbose:
            print(exec_implementation_attempt)
        try:
            exec(exec_implementation_attempt, locals())
        except NameError as e:
            if catch_name_exceptions:
                return implementation_attempt + asserts_str, implementation_set, e
            else:
                raise e
        except Exception as e:
            if catch_name_exceptions:
                return None, implementation_set, e
            else:
                raise e
    implementation_attempt += asserts_str
    return implementation_attempt, implementation_set, None

def kill_remaining_futures(futures):
    for future in futures:
        if not future.done():
            future.result(timeout=0)

def multiprocess_fill(scc, dependencies_str, defined_fns, all_implementations, asserts_str, timeout, num_workers=32, max_attempts=1000, debug=False):
    if debug:
        num_workers = 1
        verbose = True
    else:
        verbose = False
    random.seed(42)
    all_implementation_sets = [list(set(impls)) for impls in all_implementations.values()]
    implementation_sets = list(itertools.product(*all_implementation_sets))
    n_to_try = min(max_attempts, len(implementation_sets))
    with tqdm(total=n_to_try) as pbar:
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            submitted = 0
            random.shuffle(implementation_sets)
            for implementation_set in implementation_sets[:n_to_try]:
                futures.append(executor.submit(
                    implement_set, implementation_set, dependencies_str, asserts_str, verbose))
                submitted += 1
                if submitted % num_workers == 0 or submitted == n_to_try:
                    for future in futures:
                        if debug:
                            breakpoint()
                        try:
                            result = future.result(timeout=timeout)
                            if result is not None:
                                implementation_attempt, implementation_set, _ = result
                                executor.shutdown(wait=False, cancel_futures=True)
                                pbar.close()
                                print("Successfully implemented", scc)
                                for fn_name, implementation in zip(scc, implementation_set):
                                    fn = defined_fns[fn_name]
                                    if fn.fixed_implementation is None:
                                        fn.fix_implementation(implementation)
                                return implementation_attempt
                            else:
                                pbar.update(1)
                        except KeyboardInterrupt:
                            kill_remaining_futures(futures)
                            raise KeyboardInterrupt
                        except:
                            pbar.update(1)
                            continue
                    futures = []
            executor.shutdown(wait=False, cancel_futures=True)
            print(f"Failed implementing {scc}")

def autofill(scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, remaining_attempts=10):
    all_implementation_sets = [list(set(impls)) for impls in all_implementations.values()]
    implementation_sets = list(itertools.product(*all_implementation_sets))
    random.shuffle(implementation_sets)
    for implementation_set in implementation_sets:
        if remaining_attempts > 0:
            implementation_attempt, implementation_set, e = implement_set(
                implementation_set, dependencies_str, asserts_str, catch_name_exceptions=True)
            if implementation_attempt is None:
                continue
            remaining_attempts -= 1
            missing_fn_name = e.args[0].split("'")[1]
            # Find lines that call the missing function
            new_implementation_attempt = fill_in_missing_fn(
                missing_fn_name, scc, defined_fns, implementation_set, implementation_attempt, codegen)
            if new_implementation_attempt is not None:
                return new_implementation_attempt

def attempt_implementations(scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, should_fill_in_missing=False, should_expand=False, remaining_attempts=5, timeout=1):
    print("Attempting to implement", scc)
    implementation_attempt = multiprocess_fill(
        scc, dependencies_str, defined_fns, all_implementations, asserts_str, timeout)
    if implementation_attempt is not None:
        return implementation_attempt

    if should_fill_in_missing:
        implementation_attempt = autofill(
            scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, remaining_attempts)
        if implementation_attempt is not None:
            print("Successfully implemented", scc, "with autofill")
            return implementation_attempt
    
    if should_expand:
        print("Attempting to expand", scc)
        new_scc = set()
        # Copy the old implementations
        new_implementations = all_implementations.copy()
        for fn_name in scc:
            fn = defined_fns[fn_name]
            if fn.fixed_implementation is None:
                new_fn_defs = fn.expand(codegen)
                for new_fn_name, new_fn in new_fn_defs.items():
                    new_fn.implement(codegen)
                    new_implementations[new_fn_name] = new_fn.get_implementation_strs()
            defined_fns.update(new_fn_defs)
            new_scc.update(new_fn_defs.keys())
        print("Expanded", scc, "to", new_scc)
        for fn_name in scc:
            fn = defined_fns[fn_name]

        return attempt_implementations(
            new_scc, dependencies_str, defined_fns, new_implementations, asserts_str, codegen, should_fill_in_missing=False, should_expand=False, remaining_attempts=remaining_attempts, timeout=timeout)
    raise RuntimeError(f"No implementation found for {scc}")

def eval_scc(scc, dependencies_str, defined_fns, codegen, allow_autofill=False, should_expand=False):
    # Evaluate all the combinations of possible
    # implementations of the functions in the SCC
    all_implementations = {}
    asserts_str = ""
    for fn_name in scc:
        fn = defined_fns[fn_name]
        all_implementations[fn_name] = fn.get_implementation_strs()
        asserts_str += fn.get_assert_str()
    return attempt_implementations(
        scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, should_fill_in_missing=allow_autofill, should_expand=should_expand)

def implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill=False, should_expand=False):
    if scc_idx in implemented_sccs:
        return
    dependencies_str = ""
    for edge in scc_edges[scc_idx]:
        dependencies_str += implement_scc(edge, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand)
    for fn_name in sccs[scc_idx]:
        fn = defined_fns[fn_name]
        fn.implement(codegen)
    dependencies_str += eval_scc(sccs[scc_idx], dependencies_str, defined_fns, codegen, allow_autofill, should_expand)
    implemented_sccs.append(scc_idx)
    return dependencies_str

def write_to_file(filename, defined_fns):
    fn_defs = ""
    for fn in defined_fns.values():
        fn_defs += CONSTS['full_fn_str'].format(
            desc=fn.desc, fn_impl=fn.fixed_implementation)
    asserts = "\n".join(fn.get_assert_str() for fn in defined_fns.values())
    assert CONSTS['exist_asserts'](asserts)
    contents = f"{fn_defs}\n{asserts}"
    with open(filename, "w") as f:
        print("Writing to " + str(filename))
        f.write(contents)
    print("Done writing to " + str(filename))

def parsel(codegen, source_file, target_file=None, allow_autofill=False, should_expand=False):
    assert source_file.split(".")[-1] == 'ss'
    if target_file is None:
        target_file = source_file.split(".")[0] + CONSTS['extension']
    # Load the program to be parsed
    with open(source_file, "r") as f:
        program = f.readlines()
    _, defined_fns = get_graph(program)
    sccs, scc_edges = strongly_connected_components(defined_fns)
    implemented_sccs = []
    for scc_idx, _ in enumerate(sccs):
        implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand)
    write_to_file(target_file, defined_fns)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source_file", help="The program to parse")
    argparser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    argparser.add_argument("-c", "--cache", help="Where to store the cache", default="cache.json")
    argparser.add_argument("-d", "--key", help="Codex API key file", default="keys/codex_key.txt")
    argparser.add_argument("-i", "--allow_imports", help="Allow imports", action="store_true")
    argparser.add_argument("-a", "--allow_autofill", help="Allow autofill", action="store_true")
    argparser.add_argument("-e", "--allow_expand", help="Allow autofill", action="store_true")
    args = argparser.parse_args()

    assert args.source_file.split(".")[-1] == 'ss'
    codegen = CodeGen(args.cache, args.key)

    parsel(codegen, args.source_file, allow_autofill=args.allow_autofill, should_expand=args.allow_expand)