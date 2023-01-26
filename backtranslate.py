from parsel import parsel
from parsify import to_parsel
from consts import CONSTS
import os

def backtranslate(solution, root, asserts, save_file, codegen):
  defined_fns = to_parsel(solution)
  defined_fns[root].names_to_fns(defined_fns)
  tree_str = defined_fns[root].to_parsel_str()
  if len(tree_str.strip().split('\n')) > 1:
    for fn in defined_fns:
      defined_fns[fn].describe(codegen, names_to_avoid=list(defined_fns.keys()))
    # Load input_output.json
    defined_fns[root].asserts += asserts
    defined_fns[root].rearrange()
    parsel_str = defined_fns[root].to_parsel_str()
    # Write to file
    if not os.path.exists(save_file.replace(".ss", CONSTS["extension"])):
      with open(save_file, 'w') as f:
        f.write(parsel_str)
      print(f"Writing: {save_file}")
      print(solution)
      try:
        parsel(codegen, save_file)
      except KeyboardInterrupt:
        raise KeyboardInterrupt
      except:
        pass