import json
import os
from codex import CodeGen
from parsel import get_graph, parsel_graph
import random

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
"""# -----Example Outline-----
# You must write your solution as a call outline.
# Each function to define should have its signature as "fn_name(inputs): description"
# If a function fn_x should call a function fn_y which has not yet been defined, list the definition of fn_y under fn_x (with an additional indent).
# If a function x should call a function y which has already been defined, include the name fn_y to reference it.
# There is no need to reference a function defined at the same level.
# Here is an example of this format applied to the Collatz conjecture:
# \"\"\"
# collatz_recursion(num, cur_list): Calls base_case if 1, otherwise call recursion_rule
#    base_case(num, cur_list): Returns the list with the number appended to it
#    recursion_rule(num, cur_list): Add num to list, recurse with num = 3n + 1 if odd or num = n / 2 if even
#        collatz_recursion
# \"\"\"
#
# And here is an example of the format applied to a function that takes a step of the game of life and then inverts the board:
# \"\"\"
# game_of_life_inversion_iteration(array_at_time_t): Takes a board and returns the next iteration of the game of life, but with all values flipped.
#    game_of_life_iteration(array_at_time_t): Takes a board with active and inactive cells as a list of lists and returns the next iteration of the game of life.
#    array_inversion(array): Invert a square array by flipping 0's and 1's
# \"\"\"
#
# -----Outline-----
\"\"\"
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
          cur_asserts += [f"{repr(input.rstrip())} -> {repr(output.rstrip())}"]
        # for input, output in zip(inputs, outputs):
        #   input = ','.join([repr(input_ex) for input_ex in input])
        #   output = ','.join([repr(output_ex) for output_ex in output])
        #   cur_asserts += [str(input) + ' -> ' + str(output)]
        save_file = os.path.join(
          "generated", f'eval_{mode}_{folder}.ss')
        question = prepend_hash(question) + "\n"
        attempt_solution = codegen.generate(
          codex_in=question + prompt,
          num_completions=1,
          temperature=0.1,
          indented=False,
          stop="\"\"\""
        )[0]
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
        try:
          root, defined_fns = get_graph(attempt_solution)
          if len(defined_fns) > 5:
            continue
          root.asserts = cur_asserts
          for fn in defined_fns.values():
            fn.prefix = question + "# -----Solution-----\n"
          parsel_graph(defined_fns, codegen)
          success_save_path = save_file.replace(".ss", ".success.ss")
          if not os.path.exists(success_save_path):
            with open(success_save_path, "w") as f:
              f.write("\n".join(attempt_solution))
        except KeyboardInterrupt:
          exit()
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