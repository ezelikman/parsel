'''
Codex was deprecated by openai, so change the model to gpt3.5.
'''
import json
import openai
import os
import time
from consts import CONSTS
import random

class CodeGen():
    def __init__(self, cache="cache.json"):
        self.cache_file = cache
        self.exponential_backoff = 1
        self.messages = []
        # Load the cache JSON file, if cache file exists. Else, cache is {}
        if os.path.exists(cache):
            while os.path.exists(self.cache_file + ".tmp") or os.path.exists(self.cache_file + ".lock"):
                time.sleep(0.1)
            with open(cache, "r") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def generate(self,
        codex_in, num_completions=8, max_tokens=500, temperature=0.5, presence_penalty=0.0,
        stop=["\ndef"], indented=True, indented_after_first_line=False, require=None, cache_key=None,
        rate_limit_tokens=4000, verbose=False, logit_bias={}, model_name=None, is_test=False
    ):
        if model_name is None:
            model_name = "gpt-3.5-turbo-0301"
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
                cur_implementations = self.cache[cache_key].copy()
                if "shuffle_implementations" in CONSTS and CONSTS["shuffle_implementations"]:
                    random.shuffle(cur_implementations)
                return cur_implementations[:num_completions]
        else:
            results = []

        print(f"Using {model_name} model!")

        # raise Exception("Codex is not available")
        total_tokens = num_completions * max_tokens
        completions_per_call = rate_limit_tokens // max_tokens
        while total_tokens > 0:
            #num_completions = min(total_tokens // max_tokens, completions_per_call)
            print(f"Actually need: {num_completions} completions!")
            while True:
                try:
                    # time.sleep(8)
                    if not is_test:
                        print(codex_in)
                        messages = [{"role" : "system", "content" : "You are an expert of the Python programming language."}, {"role": "user", "content": "Please return a python function meets the following requirements. The function implementations should consist with the type innotations in function headers if exist. You should return return only the pure code. Omit explanations or any additional text. Ensure that your code can be directly compiled and run without errors.\n" + codex_in}]
                        completions = openai.ChatCompletion.create(
                            model=model_name,
                            messages=messages,
                            temperature=temperature,
                            presence_penalty=presence_penalty,
                            max_tokens=max_tokens,
                            n=num_completions,
                            logit_bias=logit_bias
                        )['choices']
                    else:
                        print(codex_in)
                        messages = [{"role" : "system", "content" : "You are an expert of the Python programming language."}, {"role": "user", "content": codex_in}]
                        completions = openai.ChatCompletion.create(
                            model=model_name,
                            messages=messages,
                            temperature=temperature,
                            presence_penalty=presence_penalty,
                            max_tokens=max_tokens,
                            n=num_completions,
                            logit_bias=logit_bias
                        )['choices']
                    self.exponential_backoff = 1
                    break
                except openai.error.RateLimitError:
                    print("Rate limit reached. Waiting before retrying...")
                    time.sleep(16 * self.exponential_backoff)
                    self.exponential_backoff *= 2
            for completion in completions:
                result = []
                response = completion["message"]["content"]
                if '```' in response:
                    response = response.split('```')[1]
                    if response[:6] == "python":
                        response = response[6:]
                for line_idx, line in enumerate(response.split("\n")): 
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
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r") as f:
                    self.cache = json.load(f)
            self.cache[cache_key] = results
            with open(self.cache_file + ".tmp", "w") as f:
                json.dump(self.cache, f)
            os.rename(self.cache_file + ".tmp", self.cache_file)
            os.remove(self.cache_file + ".lock")
            total_tokens -= num_completions * max_tokens
        return results
