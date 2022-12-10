"""Used to convert an existing program in text to a parsable format."""

from fn import Function
from consts import CONSTS

def get_defs(solution):
  defined_functions = []
  for line in solution.split('\n'):
    if line.startswith(CONSTS["fn_init"]):
      defined_functions.append(line.split('(')[0].split(' ')[1])
  return defined_functions

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
