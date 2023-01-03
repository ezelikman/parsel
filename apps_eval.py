import json
import os
from codex import CodeGen
from parsel import get_graph, parsel_graph, write_to_file
import random
import openai
import argparse
from consts import CONSTS
from apps_eval_prompts import prompt, solution_start, prefix_prefix, prefix_suffix, translation_prompt, direct_prompt

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

def consider_more_solutions(translated_solutions, translation_attempt_idx, question, parsel_solution):
  # if translation_attempt_idx == len(translated_solutions) - 1:
  #   print("Failed to translate. Trying more solutions...")
  #   translated_solutions = codegen.generate(
  #     codex_in=prefix_prefix + question + parsel_solution,
  #     num_completions=2 * CONSTS['num_completions_eval'],
  #     temperature=0.2,
  #     presence_penalty=0.1,
  #     indented=False,
  #     stop="\"\"\"",
  #     logit_bias={"4299": -100}
  #   )
  return translated_solutions

def main(problem, debug=False, sample_only=False):
  modes = ['test']
  direct = False
  for mode in modes:
    apps_mode = os.path.join('APPS', mode)
    folders = sorted(os.listdir(apps_mode))
    # random.shuffle(folders)
    for folder in folders:
      try:
        if problem != -1 and int(folder) != problem:
          continue
      except:
        continue
      if os.path.isdir(os.path.join(apps_mode, folder)):
        with open(os.path.join(apps_mode, folder, 'question.txt')) as f:
          question = f.read()
        # check if os.path.join(apps_mode, folder, 'input_output.json') exists
        if not os.path.exists(os.path.join(apps_mode, folder, 'input_output.json')):
          continue
        with open(os.path.join(apps_mode, folder, 'input_output.json')) as f:
          input_output = json.load(f)
        if len(input_output['inputs']) == 0:
          continue
        # # load the solutions
        # with open(os.path.join(apps_mode, folder, 'solutions.json')) as f:
        #   solutions = json.load(f)
        # load metadata
        with open(os.path.join(apps_mode, folder, 'metadata.json')) as f:
          metadata = json.load(f)
          if metadata['difficulty'] != 'competition':
            continue
        print("PROBLEM: ", folder)
        # open performance.csv and write the problem number
        if not sample_only:
          if os.path.exists(f"performance_{CONSTS['num_completions_eval']}.csv"):
            # first check if the problem number is already at the start of some line in the file
            with open(f"performance_{CONSTS['num_completions_eval']}.csv", "r") as f:
              for line in f.readlines():
                if line.startswith(folder): #and (len(line.split(",")) == CONSTS['max_text_completions'] + 1):
                  exit()

          with open(f"performance_{CONSTS['num_completions_eval']}.csv", "a+") as f:
            f.write("\n" + folder)

        inputs = input_output['inputs']
        outputs = input_output['outputs']
        cur_asserts = []
        for cur_input, output in zip(inputs, outputs):
          try:
            cur_asserts += [f"{repr(cur_input.rstrip())} -> {repr(output.rstrip())}"]
          except:
            cur_asserts += [f"{repr(cur_input)} -> {repr(output)}"]
        # for input, output in zip(inputs, outputs):
        #   input = ','.join([repr(input_ex) for input_ex in input])
        #   output = ','.join([repr(output_ex) for output_ex in output])
        #   cur_asserts += [str(input) + ' -> ' + str(output)]
        save_file = os.path.join(
          "generated", f'eval_{mode}_{folder}.ss')
        question = question + "\n"
        cur_prompt = direct_prompt if direct else prompt
        # Check if confirmation.txt exists at the root
        if not os.path.exists("confirmation.txt"):
          print("WARNING: confirmation.txt not found. Should we continue? (y/n)")
          if input() != "y":
            exit()
          else:
            with open("confirmation.txt", "w") as f:
              f.write("Confirmed")
        sketch_solutions = codegen.generate(
          model_name=CONSTS['text_model_name'],
          rate_limit_tokens=CONSTS['rate_limit_tokens_text'],
          codex_in=prefix_prefix + question + cur_prompt,
          num_completions=CONSTS['num_text_completions'],
          temperature=0.6,
          indented=False,
          stop="\"\"\"",
          logit_bias={"4299": -100}
        )
        n_valid_translations = 0
        for sketch_solution in sketch_solutions:
          if n_valid_translations >= CONSTS['max_text_completions']:
            break
          if direct:
            parsel_solution = sketch_solution
            translated_solutions = [parsel_solution]
          else:
            print(solution_start + "\n".join(sketch_solution).lstrip())
            parsel_solution = translation_prompt.format(
              solution_start=solution_start,
              solution_text="\n".join(sketch_solution).lstrip(),
            )
            translated_solutions = codegen.generate(
              codex_in=prefix_prefix + question + parsel_solution,
              num_completions=CONSTS['num_translation_attempts'],
              temperature=0.2,
              presence_penalty=0.1,
              indented=False,
              stop="\"\"\"",
              logit_bias={"4299": -100}
            )
          valid_translation = False
          translation_attempt_idx = -1
          while translation_attempt_idx < len(translated_solutions) - 1:
            translation_attempt_idx += 1
            attempt_solution = translated_solutions[translation_attempt_idx]
            if valid_translation:
              break
            if any(line.startswith("# ") for line in attempt_solution):
              translated_solutions = consider_more_solutions(translated_solutions, translation_attempt_idx, question, parsel_solution)
              continue
            if len("".join(attempt_solution).strip()) == 0:
              translated_solutions = consider_more_solutions(translated_solutions, translation_attempt_idx, question, parsel_solution)
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
              root, defined_fns = get_graph(attempt_solution)
              if len(defined_fns) > 7:
                translated_solutions = consider_more_solutions(translated_solutions, translation_attempt_idx, question, parsel_solution)
                continue
              else:
                print(f"Attempt number {translation_attempt_idx}")
                print("\n".join(attempt_solution))
                print(f"Implementing {len(defined_fns)} functions")
                valid_translation = True
                n_valid_translations += 1
              root.asserts = cur_asserts
              for fn in defined_fns.values():
                fn.prefix = prefix_prefix + question + prefix_suffix
              parsel_graph(defined_fns, codegen, debug=debug, sample_only=sample_only)
              if sample_only:
                continue
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
  argparser = argparse.ArgumentParser()
  argparser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  argparser.add_argument("-c", "--cache", help="Where to store the cache", default="cache.json")
  argparser.add_argument("-k", "--key", help="Codex API key file", default="keys/codex_key.txt")
  argparser.add_argument("-i", "--allow_imports", help="Allow imports", action="store_true")
  argparser.add_argument("-a", "--allow_autofill", help="Allow autofill", action="store_true")
  argparser.add_argument("-e", "--allow_expand", help="Allow autofill", action="store_true")
  argparser.add_argument("-d", "--debug", help="Debug", action="store_true")
  argparser.add_argument("-b", "--best", help="Best", action="store_true")
  argparser.add_argument("-p", "--problem", help="Problem number", default=2016, type=int)
  argparser.add_argument("-s", "--sample_only", help="Sample only, do not evaluate", action="store_true")

  args = argparser.parse_args()
  debug = args.debug
  from consts import mode
  assert mode == "apps"

  codegen = CodeGen(args.cache, args.key)
  if args.debug:
    debug = "all"
  if args.best:
    debug = "best"
  main(args.problem, debug=debug, sample_only=args.sample_only)