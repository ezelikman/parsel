import argparse
from codex import CodeGen
from graph import get_graph, strongly_connected_components, get_root
import itertools
from fn import get_function_from_examples
import concurrent.futures
from multiprocessing import get_context
from tqdm import tqdm
import random
import time
from consts import CONSTS
import multiprocessing
import subprocess
import os

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
            CONSTS['exec'](new_implementation_attempt)
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

# Try to fill in the implementation of a set of functions in an SCC
def eval_implementation(implementation_set, dependencies_str, asserts_str, verbose=True, catch_name_exceptions=False, best_attempt=0):
    implementation_attempt = dependencies_str
    for fn_implementation in implementation_set:
        implementation_attempt += fn_implementation + "\n"
    asserts_passed = []
    failure = None
    attempted = 0
    for assert_str in asserts_str.splitlines():
        n_remaining = len(asserts_str.splitlines()) - attempted
        n_remaining_to_best_beat = best_attempt - len(asserts_passed)
        if (len(asserts_str.splitlines()) - attempted < best_attempt) or (CONSTS['strict_mode'] and (len(asserts_passed) != attempted)):
            failure = Exception("Already beat this attempt")
            break
        exec_implementation_attempt = implementation_attempt
        if verbose:
            assert_in = CONSTS["get_assert_in"](assert_str)
            exec_implementation_attempt += CONSTS["output_fn"].format(output_str=assert_in)
        exec_implementation_attempt += assert_str
        if verbose:
            print("--------")
            print(CONSTS["exec_pre"])
            print(exec_implementation_attempt)
        try:
            CONSTS['exec'](exec_implementation_attempt)
        except Exception as e:
            if failure is None:
                failure = e
            continue
        asserts_passed += [assert_str]
        attempted += 1
    if failure is not None:
        if isinstance(failure, NameError):
            return implementation_attempt + asserts_str, implementation_set, failure, asserts_passed
        else:
            return None, implementation_set, failure, asserts_passed
    implementation_attempt += asserts_str
    return implementation_attempt, implementation_set, None, asserts_passed

# Kill any futures that haven't finished yet
def kill_remaining_futures(futures):
    for future in futures:
        if not future.done():
            future.result(timeout=0)

# Use multiprocessing to try to fill in the implementation of an SCC
def multiprocess_fill(scc, dependencies_str, defined_fns, all_implementations, asserts_str, timeout, num_workers=30, min_attempts=500, max_attempts=100000, min_time=60, max_time=120, debug=False, seed=42):
    if debug and debug != "best":
        num_workers = 1
        verbose = True
    else:
        verbose = False
    random.seed(seed)
    print(seed)
    all_implementation_sets = [list(set(impls)) for impls in all_implementations.values()]
    # We save memory by only storing the index of the implementation in all_implementation_sets
    implementation_sets = list(itertools.product(*[list(range(len(impls))) for impls in all_implementation_sets]))
    n_to_try = min(max_attempts, len(implementation_sets))
    best_attempt = (0, None)
    start_time = time.time()
    with tqdm(total=n_to_try) as pbar:
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers, mp_context=get_context('spawn')) as executor:
            futures = []
            submitted = 0
            random.shuffle(implementation_sets)
            for implementation_set_indices in implementation_sets[:n_to_try]:
                # We need to convert the implementation set indices to the actual implementation_set
                implementation_set = [all_implementation_sets[i][impl_id] for i, impl_id in enumerate(implementation_set_indices)]
                if (not (time.time() - start_time > min_time and submitted > min_attempts)) and ((time.time() - start_time) < max_time):
                    futures.append(executor.submit(
                        eval_implementation, implementation_set, dependencies_str, asserts_str, verbose, best_attempt[0]))
                    submitted += 1
                if submitted % num_workers == 0 or submitted == n_to_try:
                    for future in futures:
                        if debug and debug != "best":
                            breakpoint()
                        try:
                            result = future.result(timeout=timeout)
                            if result is not None:
                                implementation_attempt, implementation_set, error, asserts_passed = result
                                if error is not None:
                                    if len(asserts_passed) > best_attempt[0]:
                                        best_attempt = (len(asserts_passed), implementation_set)
                                    raise error
                                executor.shutdown(wait=False, cancel_futures=True)
                                os.system("pkill -f multiprocessing.spawn")
                                pbar.close()
                                print("Successfully implemented", scc)
                                if CONSTS['eval_mode']:
                                    with open(CONSTS['eval_filename'], "a+") as f:
                                        f.write(f", {len(asserts_str.splitlines())} / {len(asserts_str.splitlines())}")
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
            if debug:
                print(CONSTS['exec_pre'])
                print(best_attempt[0])
                print(dependencies_str)
                if best_attempt[1] is not None:
                    print("\n".join(best_attempt[1]))
                else:
                    # Print the most recent attempt
                    print("\n".join(implementation_set))
                    pass
                print(asserts_str)
                breakpoint()
            reattempt = executor.submit(
                eval_implementation, best_attempt[1], dependencies_str, asserts_str, verbose)
            try:
                print("Reattempting", scc)
                result = reattempt.result(timeout=5)
                if result is not None:
                    implementation_attempt, implementation_set, error, asserts_passed = result
                    print("Reattempted", scc)
                    print("Original attempt:", best_attempt[0])
                    print("Asserts passed:", len(asserts_passed))
                    for assert_passed in asserts_passed:
                        print("    ", assert_passed)
                    if error is not None:
                        if len(asserts_passed) > best_attempt[0]:
                            best_attempt = (len(asserts_passed), implementation_set)
                        raise error
                    executor.shutdown(wait=False, cancel_futures=True)
                    pbar.close()
                    print("Successfully implemented", scc)
                    if CONSTS['eval_mode']:
                        with open(CONSTS['eval_filename'], "a+") as f:
                            f.write(f", {len(asserts_str.splitlines())} / {len(asserts_str.splitlines())}")
                    for fn_name, implementation in zip(scc, implementation_set):
                        fn = defined_fns[fn_name]
                        if fn.fixed_implementation is None:
                            fn.fix_implementation(implementation)
                    return implementation_attempt
            except Exception as e:
                print("Reattempt error:", e)
            os.system("pkill -f multiprocessing.spawn")
            executor.shutdown(wait=False, cancel_futures=True)
            while multiprocessing.active_children():
                try:
                    os.system(f"kill -9 {multiprocessing.active_children()[0].pid}")
                except:
                    pass
            print(f"Failed implementing {scc}, best attempt: {best_attempt[0]} / {len(asserts_str.splitlines())}")
            # open "performance.csv" and write the score in the current line
            if CONSTS['eval_mode']:
                with open(CONSTS['eval_filename'], "a+") as f:
                    f.write(f", {best_attempt[0]} / {len(asserts_str.splitlines())}")
            for work_item in executor._pending_work_items.values():
                work_item.future.cancel()

def autofill(scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, remaining_attempts=10):
    all_implementation_sets = [list(set(impls)) for impls in all_implementations.values()]
    implementation_sets = list(itertools.product(*all_implementation_sets))
    random.shuffle(implementation_sets)
    for implementation_set in implementation_sets:
        if remaining_attempts > 0:
            implementation_attempt, implementation_set, e, _ = eval_implementation(
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

def attempt_implementations(scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, should_fill_in_missing=False, should_expand=False, remaining_attempts=5, timeout=0.1, debug=False, seed=42):
    print("Attempting to implement", scc)
    implementation_attempt = multiprocess_fill(
        scc, dependencies_str, defined_fns, all_implementations, asserts_str, timeout, debug=debug, seed=seed)
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
            new_scc, dependencies_str, defined_fns, new_implementations, asserts_str, codegen, should_fill_in_missing=False, should_expand=False, remaining_attempts=remaining_attempts, timeout=timeout, debug=debug, seed=seed)
    raise RuntimeError(f"No implementation found for {scc}")

def eval_scc(scc, dependencies_str, defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False, seed=42):
    # Evaluate all the combinations of possible
    # implementations of the functions in the SCC
    all_implementations = {}
    asserts_str = ""
    for fn_name in scc:
        fn = defined_fns[fn_name]
        all_implementations[fn_name] = fn.get_implementation_strs()
        asserts_str += fn.get_assert_str()
    return attempt_implementations(
        scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, should_fill_in_missing=allow_autofill, should_expand=should_expand, debug=debug, seed=seed)

def clear_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False):
    for edge in scc_edges[scc_idx]:
        clear_scc(edge, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug)
    for fn_name in sccs[scc_idx]:
        fn = defined_fns[fn_name]
        fn.fixed_implementation = None

def implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False, sample_only=False, seed=42, backtrack=False):
    print("Implementing SCC", scc_idx, sccs[scc_idx])
    if scc_idx in implemented_sccs:
        return implemented_sccs[scc_idx]
    dependencies_str = ""
    for edge in scc_edges[scc_idx]:
        dependencies_str += implement_scc(edge, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug, seed=seed)
    for fn_name in sccs[scc_idx]:
        fn = defined_fns[fn_name]
        fn.implement(codegen)
    if not sample_only:
        if not backtrack:
            new_str = dependencies_str + eval_scc(sccs[scc_idx], dependencies_str, defined_fns, codegen, allow_autofill, should_expand, debug)
        else:
            try:
                new_str = dependencies_str + eval_scc(sccs[scc_idx], dependencies_str, defined_fns, codegen, allow_autofill, should_expand, debug, seed=seed, backtrack=False)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print("Backtracking due to error", e)
                clear_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug)
                for implemented_scc in list(implemented_sccs.keys()):
                    del implemented_sccs[implemented_scc]
                new_str = implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug, seed=seed + 1, backtrack=True)
    else:
        new_str = dependencies_str
    implemented_sccs[scc_idx] = new_str
    return new_str

def fns_to_str(fn, written):
    if fn.name in written:
        return ""
    written.add(fn.name)
    total_str = ""
    for child in fn.children:
        total_str += fns_to_str(child, written)
    return total_str + CONSTS['full_fn_str'].format(
        desc=fn.desc, fn_impl=fn.fixed_implementation)

def write_to_file(filename, defined_fns):
    fn_defs = ""
    root = get_root(defined_fns)
    fn_defs = fns_to_str(defined_fns[root], set())
    asserts = "\n".join(fn.get_assert_str() for fn in defined_fns.values())
    assert CONSTS['exist_asserts'](asserts)
    exec_pre = CONSTS['exec_pre']
    contents = f"{exec_pre}{fn_defs}\n{asserts}"
    with open(filename, "w") as f:
        print("Writing to " + str(filename))
        f.write(contents)
    print("Done writing to " + str(filename))

def parsel_graph(defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False, sample_only=False):
    sccs, scc_edges = strongly_connected_components(defined_fns)
    implemented_sccs = {}
    for scc_idx, _ in enumerate(sccs):
        implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug, sample_only)
    return defined_fns

def parsel(codegen, source_file, target_file=None, allow_autofill=False, should_expand=False, debug=False):
    assert source_file.split(".")[-1] == 'ss'
    if target_file is None:
        target_file = source_file.split(".")[0] + CONSTS['extension']
    # Load the program to be parsed
    with open(source_file, "r") as f:
        program = f.readlines()
    if "#*#*#\n" in program:
        header = program[:program.index("#*#*#\n")]
        program = program[program.index("#*#*#\n") + 1:]
    else:
        header = []
    _, defined_fns = get_graph(program)
    for fn in defined_fns.values():
        fn.prefix = "\n".join(header)

    defined_fns = parsel_graph(defined_fns, codegen, allow_autofill, should_expand, debug)
    write_to_file(target_file, defined_fns)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source_file", help="The program to parse")
    argparser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    argparser.add_argument("-c", "--cache", help="Where to store the cache", default="cache.json")
    argparser.add_argument("-k", "--key", help="Codex API key file", default="keys/codex_key.txt")
    argparser.add_argument("-i", "--allow_imports", help="Allow imports", action="store_true")
    argparser.add_argument("-a", "--allow_autofill", help="Allow autofill", action="store_true")
    argparser.add_argument("-e", "--allow_expand", help="Allow autofill", action="store_true")
    argparser.add_argument("-d", "--debug", help="Debug", action="store_true")
    argparser.add_argument("-b", "--best", help="Best", action="store_true")
    args = argparser.parse_args()

    assert args.source_file.split(".")[-1] == 'ss'
    codegen = CodeGen(args.cache, args.key)
    from consts import mode
    assert mode != "apps"
    if args.best:
        debug = 'best'
    else:
        debug = args.debug
    parsel(codegen, args.source_file, allow_autofill=args.allow_autofill, should_expand=args.allow_expand, debug=debug)