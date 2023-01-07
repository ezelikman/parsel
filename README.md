In order to run this project, here are some example commands:
- `python parsel.py programs/problem_solving.ss` will run and transpile the program in the file `programs/problem_solving.ss`.
- `python parsel.py programs/collatz_recursion.ss` shows an example of a recursive function.
- To run `python parsel.py programs/and_commute.ss`, change the mode in `consts/__init__.py` to `lean` and (assuming you have Lean installed), it will generate a Lean file in the same directory as the input file.
- To run `game_of_life_inverse_expand.ss` you will need to use the `-e` flag to automatically expand / decompose it.
- To run `game_of_life_inverse_fill.ss` you will need to use the `-a` to autofill the program with functions that are called but not used.