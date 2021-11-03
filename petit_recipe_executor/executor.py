import logging
import time
from typing import List, Optional

from .base_functions import functions
from .context import Context
from .datastruct import VARIABLE_TOKEN, Recipe, Result, Step, Test

# TODO: move to async to handle more load
# TODO: implem dependency detection


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

    def _do_test(self, step: Step, test: Test) -> bool:
        result = False
        try :
            func = functions[test.function]
            args = self._prepare_args(test.with_)
            result = func(**args)
        except:
            # TODO: log
            pass
        return result

    def __configure(self, args: Optional[dict]) -> None:
        if args is not None:
            for k, v in args.items():
                self.context.put(k, v)

    def do_step(self, step: Step) -> Result:
        start = time.time()
        func = functions[step.function]
        args = self._prepare_args(step.with_)
        self.logger.debug(f'{args}')
        result = func(**args)
        self.logger.debug(f'{step.name} did return {result}')

        if step.returns is not None:
            self.context.put(step.returns, result)

        test_passed = True
        if step.tests is not None:
            for test in step.tests:
                test_passed = self._do_test(step, test)
        
        end = time.time()
        return Result(
            name=step.name,
            success=test_passed,
            elapsed=end-start
        )

    def add_env(self, args: dict):
        self.__configure(args)

    def bind_args(self, args: dict):
        self.__configure(args)

    def execute_recipe(self, recipe: Recipe) -> List[Result]:
        results = []
        self.__configure(recipe.env)
        for step in recipe.steps:
            results.append(self.do_step(step))

        return results
