import json
import os
from codex import CodeGen
from parsel import get_graph, parsel_graph, write_to_file
import random
import openai

# Check if APPS folder exists
if not os.path.exists("APPS"):
  # Confirm download using input
  print("APPS folder not found. Should we download it? (y/n)")
  if input() != "y":
    exit()
  # Download APPS
  os.system("wget https://people.eecs.berkeley.edu/~hendrycks/APPS.tar.gz")
  os.system("tar -xvf APPS.tar.gz")
  os.system("rm APPS.tar.gz")

# For each line, add "# " to the beginning, avoiding trailing whitespace
def prepend_hash(string):
  new_str = "# " + string.replace("\n", "\n# ")
  return new_str.replace("\n# \n", "\n#\n")

prompt = (
"""-----Parsel Format-----
You must write your solution in Parsel.
Each function to define should have its signature as "fn_name(inputs): description"
If a function fn_x should call a function fn_y which has not yet been defined, list the definition of fn_y under fn_x (with an additional indent).
If a function x should call a function y which has already been defined, include the name fn_y to reference it.
There is no need to reference a function defined at the same level.
Here is an example of this format applied to the Collatz conjecture:
\"\"\"
collatz_recursion(num, cur_list): Calls base_case if 1, otherwise call recursion_rule
   base_case(num, cur_list): Returns the list with the number appended to it
   recursion_rule(num, cur_list): Add num to list, recurse with num = 3n + 1 if odd or num = n / 2 if even
       collatz_recursion
\"\"\"

And here is an example of the format applied to a function that takes a step of the game of life and then inverts the board:
\"\"\"
game_of_life_inversion_iteration(array_at_time_t): Takes a board and returns the next iteration of the game of life, but with all values flipped.
   game_of_life_iteration(array_at_time_t): Takes a board with active and inactive cells as a list of lists and returns the next iteration of the game of life.
   array_inversion(array): Invert a square array by flipping 0's and 1's
\"\"\"

And here is an example of the format applied to a function that finds the longest palindrome within a string:
\"\"\"
longest_palindrome(s) -> c1: longest_palindrome takes a string and returns the longest palindrome in the string.
  is_palindrome(s) -> c2: is_palindrome returns True if the string is a palindrome, and False otherwise.
  check(li, ri, s) -> c3: check takes in a string, s, and two indices, li and ri, and returns the longest palindrome that starts at li and ends at ri
    is_palindrome
\"\"\"

Here is another example that identifies all integers between m and n such that their divisors squared are a square:
\"\"\"
list_squared(m, n): list_squared(m, n) returns a list of lists of integers, where each sublist contains an integer and its sum of squared divisors, and the integers are in the range [m, n] (inclusive).
  divisors_list(num): divisors_list takes a number and returns a list of all the divisors of that number.
  sum_squares(nums): sum_squares takes a list of numbers and returns the sum of the squares of those numbers.
  isSquarable(num): isSquarable takes a number and returns True if the number is a perfect square, and False otherwise.
\"\"\"

Here is an example that identifies if a prime is a circular prime:
\"\"\"
circular_prime(number): circular_prime takes a number and returns True if it is a circular prime, and False otherwise.
  rotate(l, n): rotate takes a list and an integer and returns a new list with the last n elements of the original list moved to the front.
  is_prime(n): is_prime returns True if n is a prime number, and False otherwise.
\"\"\"

-----Solution-----
Use Standard Parsel format

ANSWER in Parsel:
\"\"\"
"""
)

prefix_prefix = "QUESTION:\n"

prefix_suffix = (
"""
Use Standard Input format

ANSWER in Python code:
"""
)

def main():
  modes = ['test']
  for mode in modes:
    apps_mode = os.path.join('APPS', mode)
    folders = sorted(os.listdir(apps_mode))
    random.shuffle(folders)
    for folder in folders:
      if os.path.isdir(os.path.join(apps_mode, folder)):
        with open(os.path.join(apps_mode, folder, 'question.txt')) as f:
          question = f.read()
        with open(os.path.join(apps_mode, folder, 'input_output.json')) as f:
          input_output = json.load(f)
        if len(input_output['inputs']) == 0:
          continue
        inputs = input_output['inputs']
        outputs = input_output['outputs']
        cur_asserts = []
        for input, output in zip(inputs, outputs):
          try:
            cur_asserts += [f"{repr(input.rstrip())} -> {repr(output.rstrip())}"]
          except:
            cur_asserts += [f"{repr(input)} -> {repr(output)}"]
        # for input, output in zip(inputs, outputs):
        #   input = ','.join([repr(input_ex) for input_ex in input])
        #   output = ','.join([repr(output_ex) for output_ex in output])
        #   cur_asserts += [str(input) + ' -> ' + str(output)]
        save_file = os.path.join(
          "generated", f'eval_{mode}_{folder}.ss')
        question = question + "\n"
        attempt_solutions = codegen.generate(
          codex_in=prefix_prefix + question + prompt,
          num_completions=1,
          temperature=0.2,
          indented=False,
          stop="\"\"\"",
          logit_bias={"4299": -100}
        )
        print("PROBLEM: ", folder)
        for attempt_solution in attempt_solutions:
          if any(line.startswith("# ") for line in attempt_solution):
            continue
          if len("".join(attempt_solution).strip()) == 0:
            continue
          try:
            # Remove blank lines
            attempt_solution = [line for line in attempt_solution if line.strip() != ""]
            new_solution = [attempt_solution[0]]
            for line in attempt_solution[1:]:
              if line.lstrip() != line:
                new_solution.append(line)
              else:
                break
            attempt_solution = new_solution
            print("\n".join(attempt_solution))
            root, defined_fns = get_graph(attempt_solution)
            if len(defined_fns) > 5:
              continue
            root.asserts = cur_asserts
            for fn in defined_fns.values():
              fn.prefix = prefix_prefix + question + prefix_suffix
            parsel_graph(defined_fns, codegen, debug=False)
            success_save_path = save_file.replace(".ss", ".success.ss")
            if not os.path.exists(success_save_path):
              with open(success_save_path, "w") as f:
                f.write("\n".join(attempt_solution))
            python_save_path = save_file.replace(".ss", ".py")
            if not os.path.exists(python_save_path):
              write_to_file(python_save_path, defined_fns)
          except KeyboardInterrupt:
            exit()
          except openai.error.Timeout:
            continue
          except:
            # Write to file
            failed_save_path = save_file.replace(".ss", ".failed.ss")
            if not os.path.exists(failed_save_path):
              with open(failed_save_path, "w") as f:
                f.write("\n".join(attempt_solution))
            continue

if __name__ == '__main__':
  codegen = CodeGen("cache.json", "keys/codex_key.txt")
  main()