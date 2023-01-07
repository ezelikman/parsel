import json
import os
from codex import CodeGen
from backtranslate import backtranslate

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

def max_function_lines(solution):
  max_lines = 0
  cur_lines = 0
  in_function = False
  for line in solution.split('\n'):
    if len(line) == 0: continue
    if line.startswith('def '):
      in_function = True
      cur_lines = 1
      max_lines = max(max_lines, cur_lines)
    elif len(line) == len(line.lstrip()):
      in_function = False
      cur_lines = 0
    elif line.startswith('from ') or line.startswith('import '):
      in_function = False
      cur_lines = 0
    elif in_function:
      cur_lines += 1
      max_lines = max(max_lines, cur_lines)
  return max_lines

def function_lines(solution):
  all_lines = [0]
  in_function = False
  for line in solution.split('\n'):
    if len(line) == 0: continue
    if line.startswith('def '):
      in_function = True
      all_lines.append(1)
    elif len(line) == len(line.lstrip()):
      in_function = False
      all_lines.append(0)
    elif line.startswith('from ') or line.startswith('import '):
      in_function = False
      all_lines.append(0)
    elif in_function:
      all_lines[-1] += 1
  return all_lines

def has_globals(solution):
  for line in solution.split('\n'):
    if len(line) == len(line.lstrip()) and len(line) > 0:
      if '=' in line:
        return True
  return False

def num_defs(solution):
  return sum(1 for line in solution.split('\n') if line.startswith('def '))

def num_classes(solution):
  return sum(1 for line in solution.split('\n') if line.startswith('class '))

def num_yields(solution):
  return sum(1 for line in solution.split('\n') if line.strip().startswith('yield '))

def num_imports(solution):
  return sum(1 for line in solution.split('\n') if line.startswith('import ') or line.startswith('from '))

def main():
  modes = ['train']
  for mode in modes:
    apps_mode = os.path.join('APPS', mode)
    for folder in sorted(os.listdir(apps_mode)):
      # Check if there's a starer_code.py file
      if os.path.exists(os.path.join(apps_mode, folder, 'starter_code.py')):
        with open(os.path.join(apps_mode, folder, 'starter_code.py')) as f:
          starter = f.read()
      else:
        continue
      # if int(folder) <= 3837:
      #   continue
      # Load metadata.json
      # with open(os.path.join(apps_mode, folder, 'metadata.json')) as f:
      #   metadata = json.load(f)
      #   # Check if difficulty is competition
      #   if metadata['difficulty'] != 'competition':
      #     continue
      if os.path.isdir(os.path.join(apps_mode, folder)):
        with open(os.path.join(apps_mode, folder, 'solutions.json')) as f:
          solutions = json.load(f)
          for solution_idx, solution in enumerate(solutions):
            if num_defs(solution) > 2 and not has_globals(solution) and "input()" not in solution:
              max_len = max_function_lines(solution)
              if max_len >= 5 and max_len <= 15:
                if num_classes(solution) == 0 and num_imports(solution) == 0:
                  if sorted(function_lines(solution))[-2] >= 5:
                    if num_yields(solution) == 0:
                      with open(os.path.join(apps_mode, folder, 'input_output.json')) as f:
                        input_output = json.load(f)
                        if len(input_output['inputs']) == 0:
                          continue
                        inputs = input_output['inputs']
                        outputs = input_output['outputs']
                        cur_asserts = []
                        for input, output in zip(inputs, outputs):
                          input = ','.join([repr(input_ex) for input_ex in input])
                          output = ','.join([repr(output_ex) for output_ex in output])
                          cur_asserts += [str(input) + ' -> ' + str(output)]
                      save_file = os.path.join(
                        "generated", f'{mode}_{folder}_{solution_idx}.ss')
                      root = starter.split('(')[0].split(' ')[1]
                      backtranslate(solution, root, cur_asserts, save_file, codegen)

if __name__ == '__main__':
  codegen = CodeGen("cache.json", "keys/codex_key.txt")
  main()