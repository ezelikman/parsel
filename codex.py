import json
import openai
import os
import time

class CodeGen():
    def __init__(self, cache="cache.json", key="keys/codex_key.txt"):
        self.cache_file = cache
        # Load the cache JSON file, if cache file exists. Else, cache is {}
        if os.path.exists(cache):
            with open(cache, "r") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

        # Load codex key from file
        with open(key, "r") as f:
            codex_key = f.read().strip()
        openai.organization, openai.api_key = codex_key.split(":")

    def generate(self,
        codex_in, num_completions=8, max_tokens=500, temperature=0.5, presence_penalty=0.0,
        stop=["\ndef"], indented=True, indented_after_first_line=False, require=None, cache_key=None,
        rate_limit_tokens=4000, verbose=False, logit_bias=None
    ):
        if verbose:
            print(codex_in)
            print("-----")
        assert isinstance(codex_in, str)
        cache_key_base = codex_in if cache_key is None else cache_key
        cache_key_list = (cache_key_base, max_tokens, temperature, stop, indented, indented_after_first_line, require)
        if presence_penalty != 0.0:
            cache_key_list = cache_key_list + (presence_penalty,)
        cache_key = str(cache_key_list)
        if cache_key in self.cache:
            if len(self.cache[cache_key]) < num_completions:
                num_completions -= len(self.cache[cache_key])
                results = self.cache[cache_key]
            else:
                return self.cache[cache_key]
        else:
            results = []

        print("Calling Codex!")
        total_tokens = num_completions * max_tokens
        completions_per_call = rate_limit_tokens // max_tokens
        while total_tokens > 0:
            num_completions = min(total_tokens // max_tokens, completions_per_call)
            print(num_completions, "completions", max_tokens, "tokens each")
            while True:
                try:
                    time.sleep(31)
                    if logit_bias is None:
                        completions = openai.Completion.create(
                            model="code-davinci-002",
                            prompt=codex_in,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            presence_penalty=presence_penalty,
                            stop=stop,
                            n=num_completions,
                        )['choices']
                    else:
                        completions = openai.Completion.create(
                            model="code-davinci-002",
                            prompt=codex_in,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            presence_penalty=presence_penalty,
                            stop=stop,
                            n=num_completions,
                            logit_bias=logit_bias
                        )['choices']
                    break
                except openai.error.RateLimitError:
                    print("Rate limit reached. Waiting before retrying...")
            for completion in completions:
                result = []
                for line_idx, line in enumerate(completion.text.split("\n")):
                    if (indented or (indented_after_first_line and line_idx > 0)) and line.lstrip() == line and line.strip() != "":
                        break
                    if require is not None and line.strip() != "" and require not in line:
                        break
                    result += [line]
                results.append(result)

            # Save updated cache
            self.cache[cache_key] = results
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f, indent=4)
            total_tokens -= num_completions * max_tokens
        return results