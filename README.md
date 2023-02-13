In order to run this project, here are some example commands:
- `python parsel.py programs/problem_solving.ss` will run and transpile the program in the file `programs/problem_solving.ss`.
- `python parsel.py programs/collatz_recursion.ss` shows an example of a recursive function.
- `python parsel.py programs/problem_solving_no_tests.ss -g` shows how you can use automatic test generation to write programs without tests.
- `python parsel.py programs/game_of_life_inverse_no_args.ss -n` shows how you can use natural language to write programs without argument names.
- `python parsel.py programs/problem_solving_no_args_no_tests.ss -g -n` shows how you can use automatic test generation to write programs without tests or argument names, i.e. in entirely natural language.
- To run `python parsel.py programs/and_commute.ss`, change the mode in `consts/__init__.py` to `lean` and (assuming you have Lean installed), it will generate a Lean file in the same directory as the input file.
- To run `game_of_life_inverse_expand.ss` you will need to use the `-e` flag to automatically expand / decompose it.
- To run `game_of_life_inverse_fill.ss` you will need to use the `-a` to autofill the program with functions that are called but not used.

In general, to configure Parsel for a new target programming, you'll need to create a new file in `consts/` and add it to `consts/__init__.py`. In addition, to use the OpenAI models, you'll need to create a `keys/codex_key.txt` file in the format `organization_id:api_key`.

If you find this repo or the paper useful in your research, please feel free to cite [our paper](https://arxiv.org/abs/2212.10561):
```
@misc{zelikman2022parsel,
  url = {https://arxiv.org/abs/2212.10561},
  author = {Zelikman, Eric and Huang, Qian and Poesia, Gabriel and Goodman, Noah D and Haber, Nick},
  keywords = {Computation and Language (cs.CL); Artificial Intelligence (cs.AI); Machine Learning (cs.LG)},
  title = {Parsel 🐍: A (De-)compositional Framework for Algorithmic Reasoning with Language Models},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
