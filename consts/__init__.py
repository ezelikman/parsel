mode = 'py'
if mode == 'py':
    from .py_consts import CONSTS
if mode == 'apps':
    from .apps_consts import CONSTS
elif mode == 'lean':
    from .lean_consts import CONSTS

if 'num_completions_eval' not in CONSTS:
    CONSTS['num_completions_eval'] = CONSTS['num_completions']