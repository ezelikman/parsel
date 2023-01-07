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
        rate_limit_tokens=4000, verbose=False, logit_bias=None, model_name=None
    ):
        if model_name is None:
            model_name = "code-davinci-002"
        if verbose:
            print(codex_in)
            print("-----")
        assert isinstance(codex_in, str)
        cache_key_base = codex_in if cache_key is None else cache_key
        cache_key_list = (cache_key_base, max_tokens, temperature, stop, indented, indented_after_first_line, require)
        if presence_penalty != 0.0:
            cache_key_list = cache_key_list + (presence_penalty,)
        if model_name != "code-davinci-002":
            cache_key_list = cache_key_list + (model_name,)
        cache_key = str(cache_key_list)
        if cache_key in self.cache:
            if len(self.cache[cache_key]) < num_completions:
                num_completions -= len(self.cache[cache_key])
                results = self.cache[cache_key]
            else:
                return self.cache[cache_key][:num_completions]
        else:
            results = []

        if model_name != "code-davinci-002":
            print("WARNING, using davinci text model")

        print("Calling Codex!")
        total_tokens = num_completions * max_tokens
        completions_per_call = rate_limit_tokens // max_tokens
        while total_tokens > 0:
            num_completions = min(total_tokens // max_tokens, completions_per_call)
            print(num_completions, "completions", max_tokens, "tokens each")
            while True:
                try:
                    time.sleep(15)
                    if logit_bias is None:
                        completions = openai.Completion.create(
                            model=model_name,
                            prompt=codex_in,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            presence_penalty=presence_penalty,
                            stop=stop,
                            n=num_completions,
                        )['choices']
                    else:
                        completions = openai.Completion.create(
                            model=model_name,
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
                    time.sleep(16)
            for completion in completions:
                result = []
                for line_idx, line in enumerate(completion.text.split("\n")):
                    if (indented or (indented_after_first_line and line_idx > 0)) and line.lstrip() == line and line.strip() != "":
                        break
                    if require is not None and line.strip() != "" and require not in line:
                        break
                    result += [line]
                results.append(result)

            # Save updated cache - reopen in case multiple processes running
            # Save to a temp file first, then rename
            # Check if a temp file exists, and if so, wait for it to be deleted
            while os.path.exists(self.cache_file + ".tmp") or os.path.exists(self.cache_file + ".lock"):
                time.sleep(0.1)
            # create an empty file to indicate that we are writing to the cache
            with open(self.cache_file + ".lock", "w") as f:
                pass
            with open(self.cache_file, "r") as f:
                self.cache = json.load(f)
            self.cache[cache_key] = results
            with open(self.cache_file + ".tmp", "w") as f:
                json.dump(self.cache, f, indent=4)
            os.rename(self.cache_file + ".tmp", self.cache_file)
            os.remove(self.cache_file + ".lock")
            total_tokens -= num_completions * max_tokens
        return results