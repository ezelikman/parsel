import json
import os
from codex import CodeGen
from parsel import get_graph, parsel_graph, write_to_file
import random
import openai
import argparse
from consts import CONSTS
from vm_prompts import prompt, solution_start, prefix_prefix, prefix_suffix, translation_prompt, direct_prompt

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
  direct = True
  for mode in modes:
    apps_mode = os.path.join('langauge-planner', mode)
    folders = [ s.split(".")[1].strip() for s in open("language-planner/eval_list.txt").readlines()]
    # random.shuffle(folders)
    for folder, question in enumerate(folders):
      try:
        if problem != -1 and int(folder) != problem:
          continue
      except:
        continue

      cur_asserts = ["-> executable"]
      save_file = os.path.join("vh_generated", f'eval_{mode}_{folder}.ss')
      question = question + "\n"
      cur_prompt = direct_prompt if direct else prompt
      print(prefix_prefix + question + cur_prompt)
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
          print(parsel_solution)
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
              fn.prefix = "\"\"\"An action plan is a list of strings that describes a sequence of steps to accomplish a task, To be correctly parsed, an action plan must be syntactically correct and contain only allowed actions and recognizable simple objects. Allowed actions: 'close' <arg1>, 'cut' <arg1>, 'drink' <arg1>, 'drop' <arg1>, 'eat' <arg1>, 'find' <arg1>, 'grab' <arg1>, 'greet' <arg1>, 'lie on' <arg1>, 'look at' <arg1>, 'open' <arg1>, 'plug in' <arg1>, 'plug out' <arg1>, 'point at' <arg1>, 'pour' <arg1> 'into' <arg2>, 'pull' <arg1>, 'push' <arg1>, 'put' <arg1> 'on' <arg2>, 'put' <arg1> 'in' <arg2>, 'put back' <arg1>, 'take off' <arg1>, 'put on' <arg1>, 'read' <arg1>, 'release', 'rinse' <arg1>, 'run to'  <arg1>, 'scrub' <arg1>, 'sit on' <arg1>, 'sleep', 'squeeze' <arg1>, 'stand up', 'switch off' <arg1>, 'switch on' <arg1>, 'touch' <arg1>, 'turn to' <arg1>, 'type on' <arg1>, 'wake up', 'walk to' <arg1>, 'wash' <arg1>, 'watch' <arg1>, 'wipe' <arg1>. To satisfy the common-sense constraints, each action step in this action plan must not violate the set of its pre-conditions (e.g. the agent cannot grab milk from the fridge before opening it) and post-conditions (e.g. the state of the fridge changes from \“closed\” to \“open\” after the agent opens it).\"\"\"\n"
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
            # plan_save_path = save_file.replace(".ss", ".txt")
            # if not os.path.exists(plan_save_path):
            #   print("save plan_save_path ", plan_save_path)
            #   script = open(python_save_path).read() + f"open(\"{plan_save_path}\", \"w\").write(\"\\n\".join(task_plan()))"
            #   import pdb;pdb.set_trace()
            #   exec(script, locals())
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
  assert mode == "py"

  codegen = CodeGen(args.cache, args.key)
  if args.debug:
    debug = "all"
  if args.best:
    debug = "best"
  main(args.problem, debug=debug, sample_only=args.sample_only)