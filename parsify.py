"""Used to convert an existing program in text to a parsable format."""

from fn import Function
from consts import CONSTS

# Used for backtranslation / decompilation
# Get the names of all the functions defined in the solution
def get_defs(solution):
  defined_functions = []
  for line in solution.split('\n'):
    if line.startswith(CONSTS["fn_init"]):
      defined_functions.append(line.split('(')[0].split(' ')[1])
  return defined_functions

# Used for backtranslation / decompilation
# Heuristically get the names of the inputs and outputs of each function
# Ideally, this should be done by parsing the AST instead
def get_fns(solution, defs, get_rets=False):
  fns = {fn: {
    'name': fn,
    'args': [],
    'ret': [],
    'parent': set(),
    'children': set(),
    'implementations': [],
  } for fn in defs}
  cur_fn = None
  for line in solution.split('\n'):
    if len(line) == 0: continue
    if line.startswith(CONSTS["fn_init"]):
      cur_fn = line.split('(')[0].split(' ')[1]
      # Get inputs
      inputs = line.split('(')[1].split(')')[0].split(',')
      fns[cur_fn]['args'] = [inp.strip() for inp in inputs]
      for fn in defs:
        if fn + "(" in line.split(':', 1)[1]:
          fns[fn]['parent'].add(cur_fn)
          fns[cur_fn]['children'].add(fn)
      fns[cur_fn]['implementations'] = [line]
    elif any(line.startswith(exclude) for exclude in CONSTS["exclude_init"]):
      cur_fn = None
    elif len(line) == len(line.lstrip()):
      cur_fn = None
    elif cur_fn is not None:
      fns[cur_fn]['implementations'].append(line)
      if CONSTS['fn_end'] in line and get_rets:
        # Calculate the number of commas in the line which are not in parentheses or brackets
        num_commas = 0
        in_paren = 0
        in_bracket = 0
        for char in line:
          if char == '(':
            in_paren += 1
          elif char == ')':
            in_paren -= 1
          elif char == '[':
            in_bracket += 1
          elif char == ']':
            in_bracket -= 1
          elif char == ',' and in_paren == 0 and in_bracket == 0:
            num_commas += 1
        rets = list(range(num_commas + 1))
        if not rets:
          fns[cur_fn]['ret'] = []
        elif len(rets) == 1:
          fns[cur_fn]['ret'] = ["res"]
        else:
          fns[cur_fn]['ret'] = ["res" + str(i) for i in range(len(rets))]
        
      for fn in defs:
        if fn + "(" in line:
          fns[fn]['parent'].add(cur_fn)
          fns[cur_fn]['children'].add(fn)

  fn_objs = {}
  for fn_name, fn_dict in fns.items():
    # Add empty asserts list
    fn_dict['asserts'] = []
    fn_objs[fn_name] = Function(
      name=fn_dict['name'],
      args=fn_dict['args'],
      ret=fn_dict['ret'],
      desc='',
      parent=None,
      asserts=[]
    )
    # Convert parents and children to a list
    fn_objs[fn_name].parents = list(fn_dict['parent'])
    fn_objs[fn_name].children = list(fn_dict['children'])
    # Convert implementation to a string
    fn_objs[fn_name].implementations = [fn_dict['implementations']]
    # Set fixed_implementations to the value of implementations
    fn_objs[fn_name].fixed_implementation = '\n'.join(fn_dict['implementations'])
  return fn_objs

def to_parsel(solution):
  defined_functions = get_defs(solution)
  basic_graph = get_fns(solution, defined_functions)
  return basic_graph

def add_fn_name_and_args(parsel_text, codegen, max_tokens=500):
  parsel_lines = [line.rstrip() for line in parsel_text if line.strip() != ""]
  is_assert_lines = [CONSTS['assert_check'](line) for line in parsel_lines]
  assert_lines = [line for line, is_assert in zip(parsel_lines, is_assert_lines) if is_assert]
  parsel_lines = [parsel_line for parsel_line, assert_line in zip(parsel_lines, is_assert_lines) if not assert_line]
  parsel_text = '\n'.join(parsel_lines)
  prompt = CONSTS["add_name_and_args"](parsel_text)
  added_args = codegen.generate(
    codex_in=prompt,
    num_completions=8,
    max_tokens=max_tokens,
    temperature=0.2,
    stop=["\n\n"],
    indented=False,
    indented_after_first_line=True,
    require=None,
    cache_key=None,
  )
  for added_arg in added_args:
    # get the non-empty lines
    added_arg = [line.strip() for line in added_arg if line.strip() != ""]
    print("Added args:", added_arg)
    # zip the lines together
    new_parsel = []
    if len(added_arg) != len(parsel_lines):
      continue
    for name_and_args, line in zip(added_arg, parsel_lines):
      indentation = len(line) - len(line.lstrip())
      new_parsel.append(" " * indentation + name_and_args + ": " + line.strip())
    final_parsel = []
    for is_assert in is_assert_lines:
      if is_assert:
        final_parsel.append(assert_lines.pop(0))
      else:
        final_parsel.append(new_parsel.pop(0))
    return final_parsel