import unittest
from .. import executor
from .. import utils
import yaml

data = """
name: check site alive
kind: test.availability

trigger:
  every: 5m

args: []

steps:
  - name: http ping
    function: http.ping_get
    with:
      url: https://google.com
"""

class ExecutorTests(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def _load_base_recipe(self):
        return utils.load_recipe(yaml.safe_load(data))

    def test_load_recipe(self):
        recipe = utils.load_recipe(yaml.safe_load(data))
        self.assertEqual(recipe.name, 'check site alive')
        self.assertEqual(recipe.kind, 'test.availability')
        self.assertEqual(recipe.args, [])

    def test_executor(self):
        recipe = self._load_base_recipe()
        e = executor.Executor()
        res = e.execute_recipe(recipe)
        self.assertTrue(res[0].success)
