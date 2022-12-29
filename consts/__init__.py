mode = 'apps'
if mode == 'py':
    from .py_consts import CONSTS
if mode == 'apps':
    from .apps_consts import CONSTS
elif mode == 'lean':
    from .lean_consts import CONSTS