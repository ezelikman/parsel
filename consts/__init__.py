mode = 'py'
if mode == 'py':
    from .py_consts import CONSTS
elif mode == 'lean':
    from .lean_consts import CONSTS
elif mode == 'vh':
    from .vh_consts import CONSTS

def assert_mode(target_mode):
    if mode == target_mode:
        return
    # if the mode is not the target mode,
    # ask the user if he wants to change the mode
    print(f'The current mode is {mode}, but the target mode is {target_mode}.')
    choice = input('Do you want to change the mode? [y/N]')
    if choice == 'y':
        # edit the file
        with open(__file__, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('mode ') or line.startswith('mode='):
                lines[i] = f"mode = '{target_mode}'\n"
                break
        with open(__file__, 'w') as f:
            f.writelines(lines)
        raise RuntimeError(f'Mode changed to {target_mode}. Please restart the program.')
    else:
        raise RuntimeError(f'Incorrect mode.')