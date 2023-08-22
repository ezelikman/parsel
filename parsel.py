import argparse
from codex import CodeGen
from graph import get_graph, strongly_connected_components, get_root
from parsify import add_fn_name_and_args
import itertools
from fn import get_function_from_examples, find_str
import concurrent.futures
from multiprocessing import get_context
from tqdm import tqdm
import random
import time
from consts import CONSTS, mode
import os
import ast
import traceback
import functools
import operator

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
            traceback.print_exc() 
            continue


# Join a set of function implementations to a string, along with
# the already-implemented dependencies of the functions
def to_implementation_str(implementation_set, dependencies_str):
    implementation_attempt = dependencies_str
    for fn_implementation in implementation_set:
        implementation_attempt += fn_implementation + "\n"
    return implementation_attempt


# Try to fill in the implementation of a set of functions in an SCC
def eval_implementation(implementation_set, dependencies_str, asserts_str, verbose=True, best_attempt=0):
    implementation_attempt = to_implementation_str(
        implementation_set, dependencies_str)
    asserts_passed = []
    failure = None
    attempted = 0
    # Try all of the asserts one at a time
    # This is perhaps less efficient for Python, but it
    # gives us a lot more information about what went wrong
    # and although not currently explicitly supported,
    # it may be necessary for other languages
    # where multiple constraints can't be applied at once
    for assert_str in asserts_str.splitlines():
        # We do still give up if we've already done better than this attempt
        if (len(asserts_str.splitlines()) - attempted < best_attempt) or (
                CONSTS['strict_mode'] and (len(asserts_passed) != attempted)):
            failure = Exception("Already beat this attempt")
            break

        # Construct the code to execute
        exec_implementation_attempt = implementation_attempt
        if verbose:
            assert_in = CONSTS["get_assert_in"](assert_str)
            exec_implementation_attempt += CONSTS["output_fn"].format(output_str=assert_in)

        # Add the assert to the code to execute
        exec_implementation_attempt += assert_str

        if verbose:
            print("--------")
            print(CONSTS["exec_pre"])
            print(exec_implementation_attempt)
        try:
            # Try to execute the code
            CONSTS['exec'](exec_implementation_attempt)
        except Exception as e:
            if failure is None:
                failure = e
            continue

        # If we get here, the assert passed
        asserts_passed += [assert_str]
        attempted += 1

    # If we get here, we've tried all of the asserts
    # If we failed, return the failure as the third return value
    if failure is not None:
        if isinstance(failure, NameError):
            return implementation_attempt + asserts_str, implementation_set, failure, asserts_passed
        else:
            return None, implementation_set, failure, asserts_passed

    # Otherwise, let's keep track of the asserts so that the final
    # Implementation has access to them
    implementation_attempt += asserts_str
    return implementation_attempt, implementation_set, None, asserts_passed


# Kill any futures that haven't finished yet
# I don't know why this is necessary, and it really feels like overkill
# but sometimes I can't seem to kill the subprocesses otherwise
def kill_remaining_futures(executor, futures):
    # Attempt 1
    try:
        executor.shutdown(wait=False, cancel_futures=True)
    except:
        pass

    # Attempt 2
    for future in futures:
        try:
            if not future.done():
                future.result(timeout=0)
        except:
            pass

    # Attempt 3
    try:
        for work_item in executor._pending_work_items.values():
            work_item.future.cancel()
    except:
        pass

    # Last resort. This kind of sucks because it means you can't run multiple compilers in parallel
    # Would love to find a better solution
    print("Killing subprocesses")
    os.system("pkill -f multiprocessing.spawn")


# Wrap up the results of a function implementation attempt
def collect_result(scc, dependencies_str, defined_fns, asserts_str, pbar, executor, futures, best_attempt):
    implementation_set = best_attempt[1]
    asserts_passed = best_attempt[2]
    error = best_attempt[3]
    print("Asserts passed:", len(asserts_passed))
    for assert_passed in asserts_passed:
        print("    ", assert_passed)
    if error is not None and not generate_tests:
        if len(asserts_passed) > best_attempt[0]:
            best_attempt = (
                len(asserts_passed), implementation_set, asserts_passed)
        raise error
    try:
        kill_remaining_futures(executor, futures)
    except:
        pass
    try:
        pbar.close()
    except:
        pass
    print("Successfully implemented", scc)
    if generate_tests:
        # Clear out the asserts in the SCC
        for fn_name in scc:
            fn = defined_fns[fn_name]
            fn.asserts = []
        # Write the passed asserts to the root
        new_fns = {dict_key: dict_value for dict_key, dict_value in defined_fns.items() if dict_key in scc}
        root = get_root(new_fns)
        defined_fns[root].asserts = [assert_passed.replace("assert", "", 1).strip() for assert_passed in asserts_passed]

    if CONSTS['eval_mode']:
        with open(CONSTS['eval_filename'], "a+") as f:
            f.write(f", {len(asserts_str.splitlines())} / {len(asserts_str.splitlines())}")
    for fn_name, implementation in zip(scc, implementation_set):
        fn = defined_fns[fn_name]
        if fn.fixed_implementation is None:
            fn.fix_implementation(implementation)
    implementation_attempt = to_implementation_str(implementation_set, dependencies_str) + "\n" + "\n".join(asserts_passed)
    return implementation_attempt, best_attempt


# This is a helper function to keep track of the best attempts
def update_best_attempt(scc, all_attempts, implementation_set, asserts_passed, error):
    asserts_passed_hash = hash(tuple(sorted(asserts_passed)))
    all_found = {fn: [] for fn in scc}
    for fn in scc:
        for assert_passed in asserts_passed:
            if fn in assert_passed:
                if generate_tests:
                    assert_passed = CONSTS['simplify_assert'](assert_passed)
                assert_target = assert_passed.split("==")[-1].strip()
                comma_idx = find_str(assert_target, ",")
                if comma_idx != -1:
                    assert_target = assert_target[:comma_idx].strip()
                all_found[fn] += [assert_target]
    if generate_tests:
        # If we're generating tests, we need to make sure that we've found at least two different values for each function
        # Modified!: Since there may be fewer tests, delete the check of each function passing >= 2 different tests.
        # found_successful_generation = (len(all_found) == len(scc))
        found_successful_generation = True
    else:
        # If we're not generating tests and we get here, we've found a successful implementation
        found_successful_generation = True
    min_found = min(len(found) for found in all_found.values())
    if min_found == 0:
        # if exist 0, get the second min if exists.
        found_nonzero = [found for found in all_found.values() if len(found) != 0]
        if found_nonzero:
            min_found = min(len(found) for found in found_nonzero)
    if found_successful_generation:
        #print("found_successful_generation")
        if generate_tests:
            score = min_found
            if asserts_passed_hash in all_attempts:
                # Inspired by the CodeT approach, we evaluate based on the product of |implementations| and |asserts|
                # We do this for the least-tested function in the SCC
                score += all_attempts[asserts_passed_hash][0]
                implementation_set = all_attempts[asserts_passed_hash][1]
                asserts_passed = all_attempts[asserts_passed_hash][2]
                error = all_attempts[asserts_passed_hash][3]
        else:
            score = len(asserts_passed)
        all_attempts[asserts_passed_hash] = (
            score,
            implementation_set,
            asserts_passed,
            error
        )


# Process the result of a single implementation attempt
def eval_result(scc, defined_fns, asserts_str, implementation_set_keys, all_attempts, pbar, executor, futures, result):
    implementation_attempt, implementation_set, error, asserts_passed = result

    # If we got an error, check if we have a new best attempt
    if error is not None:
        update_best_attempt(scc, all_attempts, implementation_set, asserts_passed, error)
        raise error

    kill_remaining_futures(executor, futures)
    pbar.close()

    # We succeeded, so we can return the implementation
    print("Successfully implemented", scc)
    if CONSTS['eval_mode']:
        # We manually edit a csv file to store the results
        # Right now evaluation on datasets isn't the main focus, so this is fine
        # There's almost certainly a more elegant way to do this
        with open(CONSTS['eval_filename'], "a+") as f:
            f.write(f", {len(asserts_str.splitlines())} / {len(asserts_str.splitlines())}")

    # Since we found a working solution, we can consider the implementation fixed
    for fn_name, implementation in zip(implementation_set_keys, implementation_set):
        fn = defined_fns[fn_name]
        if fn.fixed_implementation is None:
            fn.fix_implementation(implementation)
    return implementation_set,implementation_attempt


# If we fail to implement an SCC, we need to kill all the remaining futures and clean up
def handle_failure(scc, asserts_str, pbar, executor, futures, best_attempt):
    kill_remaining_futures(executor, futures)
    pbar.close()
    print(f"Failed implementing {scc}, best attempt: {best_attempt[0]} / {len(asserts_str.splitlines())}")
            # open "performance.csv" and write the score in the current line
    if CONSTS['eval_mode']:
        with open(CONSTS['eval_filename'], "a+") as f:
            f.write(f", {best_attempt[0]} / {len(asserts_str.splitlines())}")


# Use multiprocessing to try to fill in the implementation of an SCC
# This function could definitely use some refactoring
# Maybe in the future Parsel will do that for me
def multiprocess_fill(scc, dependencies_str, defined_fns, all_implementations, asserts_str, timeout, num_workers=None, min_attempts=500, max_attempts=100000, min_time=60, max_time=240, debug=False, seed=42):
    if num_workers is None:
        num_workers = 8 
        #cpu_count = os.cpu_count()
        #num_workers = cpu_count if cpu_count is not None else 1
    if 'max_attempts' in CONSTS:
        max_attempts = CONSTS['max_attempts']
    if debug and debug != "best":
        num_workers = 1
        verbose = True
    else:
        verbose = False
    all_implementations = dict(sorted(all_implementations.items()))
    implementation_set_keys = all_implementations.keys()
    all_implementation_sets = [list(set(impls)) for impls in all_implementations.values()]
    # We save memory by only storing the index of the implementation in all_implementation_sets
    implementation_set_dims = [len(s) for s in all_implementation_sets]
    num_implementation_sets = functools.reduce(operator.mul, implementation_set_dims, 1)

    # We can't try more than the number of implementations we have
    n_to_try = min(max_attempts, num_implementation_sets)

    def product_to_tensor_idx(prod, dims, idx):
        ans = []
        for dim in dims:
            prod //= dim
            ans.append(idx // prod)
            idx %= prod
        return ans

    def sample_product(arrs, n, k):
        indices = random.sample(range(n), k)
        dims = [len(arr) for arr in arrs]
        prod = functools.reduce(operator.mul, dims, 1)
        return [
            product_to_tensor_idx(prod, dims, idx)
            for idx in indices
        ]

    random.seed(seed)
    implementation_sets = sample_product(all_implementation_sets, num_implementation_sets, n_to_try)
    all_attempts = {}
    start_time = time.time()

    # We use a ProcessPoolExecutor to parallelize the work
    # This helps us handle variance in the runtime of each implementation
    # As well as broadly make better use of compute
    pbar = tqdm(total=n_to_try)
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers, mp_context=get_context('spawn')) as executor:

        futures = []
        # Loop over as many implementation sets as we can
        for i, implementation_set_indices in enumerate(implementation_sets):
            # We need to convert the implementation set indices to the actual implementation_set
            implementation_set = [all_implementation_sets[i][impl_id] for i, impl_id in enumerate(implementation_set_indices)]
            try:
                futures.append(executor.submit(eval_implementation, implementation_set, dependencies_str, asserts_str, verbose))
            except:
                pbar.update(1)
            if not (i == len(implementation_sets) - 1 or (i + 1) % num_workers == 0):
                continue
            # Check if the future has succeeded
            for future in futures:
                try:
                    result = future.result(timeout=1)
                    if result is not None:
                        implementation_set, implementation_attempt = eval_result(scc, defined_fns, asserts_str, implementation_set_keys, all_attempts, pbar, executor, futures, result)
                        return implementation_attempt
                    else:
                        pbar.update(1)
                except KeyboardInterrupt:
                    kill_remaining_futures(executor, futures)
                    raise KeyboardInterrupt
                except:
                    pbar.update(1)
            futures = []
            if (time.time() - start_time) >= max_time:
                print("timeout!")
                break

        # When we have exhausted all the implementation sets, we can try reattempting the best attempt
        # If we are debugging, even in 'best' mode, we want to stop at this point
        if len(all_attempts) == 0:
            kill_remaining_futures(executor, futures)
            raise Exception("No implementations found")
        best_attempt = max(all_attempts.values())
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

        # This is pretty similar to eval_result, so could probably be refactored
        try:
            implementation_attempt, best_attempt = collect_result(
                scc, dependencies_str, defined_fns, asserts_str, pbar, executor, futures, best_attempt)
            return implementation_attempt
        except Exception as e:
            print("Error:", e)
        
        # Note that the repetitiveness of kill_remaining_futures is intentional
        # If we do it outside the loop, we have the unfortunate situation where
        # sometimes we get stuck in the executor context, and the futures never get cancelled.
        # I have no idea why this happens, but this is a workaround
        handle_failure(scc, asserts_str, pbar, executor, futures, best_attempt)


# Fill in functions which are called by the generated code but not defined
def autofill(scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, remaining_attempts=10):
    all_implementation_sets = [list(set(impls)) for impls in all_implementations.values()]
    implementation_sets = list(itertools.product(*all_implementation_sets))
    random.shuffle(implementation_sets)
    for implementation_set in implementation_sets:
        if remaining_attempts > 0:
            implementation_attempt, implementation_set, e, _ = eval_implementation(
                implementation_set, dependencies_str, asserts_str)
            if implementation_attempt is None:
                continue
            remaining_attempts -= 1
            missing_fn_name = e.args[0].split("'")[1]
            # Find lines that call the missing function
            new_implementation_attempt = fill_in_missing_fn(
                missing_fn_name, scc, defined_fns, implementation_set, implementation_attempt, codegen)
            if new_implementation_attempt is not None:
                return new_implementation_attempt


# If we're in VirtualHome mode, we keep track of different kinds
# of recursion depth to avoid infinite loops
if mode == 'vh':
    force_expand_counter = 0
    max_expand_counter = 2


def attempt_implementations(scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, should_fill_in_missing=False, should_expand=False, remaining_attempts=5, timeout=0.5, debug=False, seed=42, backtrack=False):
    if 'timeout' in CONSTS:
        timeout = CONSTS['timeout']
    print("Attempting to implement", scc)
    if mode == 'vh':
        # One alternative would be to make this all into a class, but for now we don't use this except in VH mode
        global force_expand_counter, max_expand_counter
    else:
        force_expand_counter = 1
        max_expand_counter = 1
    if force_expand_counter:
        implementation_attempt = multiprocess_fill(
            scc, dependencies_str, defined_fns, all_implementations, asserts_str, timeout, debug=debug, seed=seed)
        if implementation_attempt is not None:
            return implementation_attempt
    else:
        force_expand_counter -= 1


    if should_fill_in_missing:
        implementation_attempt = autofill(
            scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, remaining_attempts)
        if implementation_attempt is not None:
            print("Successfully implemented", scc, "with autofill")
            return implementation_attempt
    
    if should_expand and max_expand_counter > 0:
        max_expand_counter -= 1
        print("Attempting to expand", scc)
        new_scc = set()
        # Copy the old implementations
        new_implementations = all_implementations.copy()
        for fn_name in scc:
            fn = defined_fns[fn_name]
            if fn.fixed_implementation is None:
                new_fn_defs = fn.expand(codegen)
                if new_fn_defs is None:
                    continue
                for new_fn_name, new_fn in new_fn_defs.items():
                    new_fn.implement(codegen)
                    new_implementations[new_fn_name] = new_fn.get_implementation_strs()
                defined_fns.update(new_fn_defs)
                new_scc.update(new_fn_defs.keys())
        print("Expanded", scc, "to", new_scc)

        return attempt_implementations(
            new_scc, dependencies_str, defined_fns, new_implementations, asserts_str, codegen, should_fill_in_missing=False, should_expand=False, remaining_attempts=remaining_attempts, timeout=timeout, debug=debug, seed=seed, backtrack=backtrack)
    raise RuntimeError(f"No implementation found for {scc}")


# Evaluate all the combinations of possible
# implementations of the functions in the SCC
def eval_scc(scc, dependencies_str, defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False, seed=42, backtrack=False):
    all_implementations = {}
    asserts_str = ""
    for fn_name in scc:
        fn = defined_fns[fn_name]
        all_implementations[fn_name] = fn.get_implementation_strs()
        asserts_str += fn.get_assert_str()
    return attempt_implementations(
        scc, dependencies_str, defined_fns, all_implementations, asserts_str, codegen, should_fill_in_missing=allow_autofill, should_expand=should_expand, debug=debug, seed=seed, backtrack=backtrack)


# Clear the implementations of all the functions in the SCC
def clear_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False):
    for edge in scc_edges[scc_idx]:
        clear_scc(edge, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug)
    for fn_name in sccs[scc_idx]:
        fn = defined_fns[fn_name]
        fn.fixed_implementation = None


# Implement the SCC and return the string
def implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False, sample_only=False, seed=42, backtrack=False, num_completions=1):
    print("Implementing SCC", scc_idx, sccs[scc_idx])
    if scc_idx in implemented_sccs:
        return implemented_sccs[scc_idx]
    dependencies_str = ""
    for edge in scc_edges[scc_idx]:
        dependencies_str += implement_scc(edge, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug, num_completions=num_completions)

    error = None
    # We exponentially increase the number of completions until we reach the max, "num_completions"
    print(f"Total: {num_completions} completions!")
    try:
        for fn_name in sccs[scc_idx]:
            fn = defined_fns[fn_name]
            fn.implement(codegen, num_completions=num_completions)
            if generate_tests:
                fn.generate_tests(codegen, num_completions=num_completions)

        # We support a "sample only" mode, where we don't actually
        # implement the SCC, but just try to run inference.
        # This let's us parallelize inference and implementation.
        if not sample_only:
            new_str = dependencies_str + eval_scc(
                sccs[scc_idx], dependencies_str, defined_fns, codegen, allow_autofill, should_expand, debug, seed=seed, backtrack=False)
        else:
            new_str = dependencies_str
        implemented_sccs[scc_idx] = new_str
        return new_str
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except Exception as e:
        error = e
        print("Error", e)
    if backtrack:
        # Backtracking allows us to try new implementations
        # of the dependencies if we fail to implement the SCC
        print("Backtracking due to error", error)
        clear_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug)
        for implemented_scc in list(implemented_sccs.keys()):
            del implemented_sccs[implemented_scc]
        new_str = implement_scc(
            scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug, seed=seed + 1, backtrack=True, num_completions=num_completions)
        implemented_sccs[scc_idx] = new_str
        return new_str
    raise error


# Convert a function to its string representation
# Including all its children
# Note that this assumes that functions need to be defined
# Before they are used, which is true for some languages
# But not all. To my knowledge, no standard language
# Requires the reverse, that functions must be defined
# After they are used.
def fns_to_str(fn, written):
    if fn.name in written:
        return ""
    written.add(fn.name)
    total_str = ""
    for child in fn.children:
        total_str += fns_to_str(child, written)
    return total_str + CONSTS['full_fn_str'].format(
        desc=fn.desc, fn_impl=fn.fixed_implementation)


# Figure out which function is the root of the graph
# And then write a file with all the functions,
# Generated from the graph
def write_to_file(filename, defined_fns):
    fn_defs = ""
    root = get_root(defined_fns)
    fn_defs = fns_to_str(defined_fns[root], set())
    asserts = "\n".join(fn.get_assert_str() for fn in defined_fns.values())
    if generate_tests:
        # Remove duplicate asserts but keep the order
        asserts_dict = {}
        for assert_fn in asserts.split("\n"):
            if assert_fn.strip() == "":
                continue
            asserts_dict[assert_fn] = True
        asserts = "\n".join(list(asserts_dict.keys()))
    # Modified!: Remove exist_asserts check to allow codegen when all tests failed.
    # assert CONSTS['exist_asserts'](asserts)
    exec_pre = CONSTS['exec_pre']
    contents = f"{exec_pre}{fn_defs}\n{asserts}"
    with open(filename, "w") as f:
        print("Writing to " + str(filename))
        f.write(contents)
    print("Done writing to " + str(filename))


# The key function of the program, which takes a function graph
# Decomposes them to their strongly connected components
# And then implements each SCC in turn
def parsel_graph(defined_fns, codegen, allow_autofill=False, should_expand=False, debug=False, sample_only=False, num_completions=1):
    sccs, scc_edges = strongly_connected_components(defined_fns)#, consider_asserts=not generate_tests)
    implemented_sccs = {}
    for scc_idx, _ in enumerate(sccs):
        implement_scc(scc_idx, sccs, implemented_sccs, scc_edges, defined_fns, codegen, allow_autofill, should_expand, debug, sample_only, num_completions=num_completions)
    return defined_fns


# Used to parse a Parsel file to a target language
def parsel(codegen, source_file, target_file=None, allow_autofill=False, should_expand=False, debug=False, add_name_and_args=False, num_completions=1):
    assert source_file.split(".")[-1] == 'ss'
    if target_file is None:
        target_file = source_file.split(".")[0] + CONSTS['extension']
    # Load the program to be parsed
    with open(source_file, "r") as f:
        program = f.readlines()

    # Extract out the header, if it exists
    if "#*#*#\n" in program:
        header = program[:program.index("#*#*#\n")]
        program = program[program.index("#*#*#\n") + 1:]
    else:
        header = []

    if add_name_and_args:
        if "\\" in program[0]:
            print("Warning: multiline function descriptions are not fully supported with add_name_and_args")
        program = add_fn_name_and_args(program, codegen)

    # Parse the program into a graph of functions
    # And add the header to each function
    _, defined_fns = get_graph(program)
    for fn in defined_fns.values():
        fn.prefix = "\n".join(header)

    # Compile the graph into a target language
    defined_fns = parsel_graph(defined_fns, codegen, allow_autofill, should_expand, debug, num_completions=num_completions)

    # Write the compiled program to a file
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
    argparser.add_argument("-g", "--generate_tests", help="Generate tests", action="store_true")
    argparser.add_argument("-n", "--add_name_and_args", help="Add name and args", action="store_true")
    argparser.add_argument("-t", "--num_completions", help="Set trying times of each functions", type=int, default=1)
    argparser.add_argument("-s", "--save_path", help="Target code save path", type=str, default=None)
    args = argparser.parse_args()

    assert args.source_file.split(".")[-1] == 'ss'
    codegen = CodeGen(args.cache)
    if args.best:
        debug = 'best'
    else:
        debug = args.debug
    generate_tests = args.generate_tests
    parsel(codegen, args.source_file, target_file=args.save_path, allow_autofill=args.allow_autofill, should_expand=args.allow_expand, debug=debug, add_name_and_args=args.add_name_and_args, num_completions=args.num_completions)
else:
    generate_tests = False 
