import logging
from typing import Any, List, Optional
import requests
from dataclasses import dataclass
import time 


# TODO: move to async to handle more load
# TODO: move to pydantic to validate and load the struct
# TODO: implem dependency detection

def post(
    url:str , 
    headers=None,
    input: str = "json", 
    output="json", 
    data:dict=None, 
    session:Optional[requests.Session]=None
):
    res = (session or requests).post(
            url=url, 
            json=data if input == "json" else None, 
            data=data if input == "form" else None,
            headers=headers,
        )
    if output == "json":
        return res.json()
    else:
        return res.text

def get(
    url:str, 
    output="json", 
    headers=None,
    session: Optional[requests.Session]=None
):
    res = (session or requests).get(url, headers=headers)
    if output == "json":
        return res.json()
    else:
        return res.text

def contains(input: str, inside: str) -> bool:
    return inside in input

def pick(input: dict, key: str) -> Any:
    return input[key]

functions = {
    "post": post,
    "get": get,
    "pick": pick,
    "contains": contains,
}

@dataclass
class Result:
    elapsed: float
    success: bool
    name: str

    def to_json(self):
        return {
            "name": self.name,
            "elapsed": self.elapsed,
            "success": self.success,
        }

class Context:
    def __init__(self) -> None:
        self.data = {}

    def put(self, name, value):
        self.data[name] = value

    # handle nested values with "." notation parent.nested
    def get(self, name: str):
        return self.data[name]


class Recipe:
    pass

class Step:
    pass

def load_recipe(d: dict) -> Recipe:
    """Reads a dict and returns a valid Recipe"""
    return d

VARIABLE_TOKEN = "$"

class Executor:
    def __init__(self) -> None:
        self.context = Context()
        self.logger = logging.getLogger()

    def _prepare_args(self, args: dict, current=None) -> dict:
        res = current or {}
        # trouver ce qui est entre {{}} et remplacer comme un format
        # trouver ce qui est entre {} et mettre la variable à la place directement
        for k, v in args.items():
            if isinstance(v, str):
                if v.startswith(VARIABLE_TOKEN) and len(v) > 2:
                    res[k] = self.context.get(v[1:])
                else:
                    res[k] = v.format_map(self.context.data)
            elif isinstance(v, dict):
                res[k] = self._prepare_args(v)
            else:
                res[k] = v
        return res

    def _do_test(self, step) -> bool:
        test = step["test"]
        func = functions[test["function"]]
        args = self._prepare_args(test["with"])

        result = func(**args)

        return result

    def _configure(self, args: Optional[dict]) -> None:
        if args is not None:
            for k, v in args.items():
                self.context.put(k, v)


    def do_step(self, step) -> Result:
        start = time.time()
        func = functions[step["function"]]
        args = self._prepare_args(step["with"])
        self.logger.debug(f'{args}')
        result = func(**args)
        self.logger.debug(f'{step["name"]} did return {result}')

        if "returns" in step:
            self.context.put(step["returns"], result)

        test_passed = True
        if "test" in step:
            test_passed = self._do_test(step)
        end = time.time()
        return Result(
            name=step["name"],
            success=test_passed, 
            elapsed=end-start
        )

    def add_env(self, args: dict):
        self._configure(args)

    def execute_recipe(self, recipe: Recipe) -> List[Result]:
        results = []
        self._configure(recipe.get("env"))
        for step in recipe["steps"]:
            results.append(self.do_step(step))

        return results
