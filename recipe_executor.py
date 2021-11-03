import logging
from typing import Any, List, Optional
import requests
from dataclasses import dataclass
import time 
import yaml


def post(url:str="", json:dict=None, session:Optional[requests.Session]=None):
    return (session or requests).post(url=url, json=json)

def bearer_get(url:str="", bearer:str="", session: Optional[requests.Session]=None):
    return (session or requests).get(url, headers={"authorization": f"Bearer {bearer}"})

def contains(input: str, inside: str) -> bool:
    return inside in input

def pick(input: dict, key: str) -> Any:
    return input[key]

functions = {
    "post": post,
    "bearerGet": bearer_get,
    "pick": pick,
    "contains": contains,
}

@dataclass
class Result:
    elapsed: float
    success: bool

class Context:
    def __init__(self) -> None:
        self.data = {}

    def put(self, name, value):
        self.data[name] = value

    def get(self, name: str):
        return self.data[name]

class Executor:
    def __init__(self) -> None:
        self.context = Context()
        self.logger = logging.getLogger()

    def _prepare_args(self, args: dict) -> dict:
        res=  {}
        # trouver ce qui est entre {{}} et remplacer comme un format
        # trouver ce qui est entre {} et mettre la variable à la place directement
        for k, v in args.items():
            if isinstance(v, str):
                if v.startswith('#') and len(v) > 2:
                    res[k] = self.context.get(v[1:-1])
                else:
                    res[k] = v.format_map(self.context.data)
            else:
                res[k] = v

        return res

    def _do_test(self, step) -> bool:
        test = step["test"]
        func = test["function"]
        args = self._prepare_args(test["with"])

        result = func(**args)

        return result

    def configure(self, args) -> None:
        for k, v in args.items():
            self.context.put(k, v)


    def do_step(self, step) -> Result:
        start = time.time()
        func = functions[step["function"]]
        args = self._prepare_args(step["with"])

        result = func(**args)
        self.logger.debug(f'{step["name"]} did return {result}')

        if  "returns" in step:
            self.context.put(step["returns"], result)

        test_passed = True
        if "test" in step:
            test_passed = self._do_test(step)
        end = time.time()
        return Result(success=test_passed, elapsed=end-start)


    def do_recipe(self, recipe) -> List[Result]:
        results = []
        self.configure(recipe["args"])
        for step in recipe["steps"]:
            self.do_step(step)
        
        return results
