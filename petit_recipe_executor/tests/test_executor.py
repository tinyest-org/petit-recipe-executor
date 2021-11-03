import unittest

import yaml

from .. import executor, utils

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


http_lib_data = """
name: check site alive
kind: test.availability

trigger:
  every: 5m

args: []

steps:

  - name: test post
    function: http.post
    with:
      url: https://example.com
      output: text
    


#   - name: test put
#     function: http.put
#     with:
#       url: https://example.com
#       output: text
  
  - name: test patch
    function: http.patch
    with:
      url: https://example.com
      output: response
    returns: res

  - name: pick resp
    function: pick
    with:
      input: $res
      key: status_code
    returns: status_code
    tests:
      - function: not_equal
        with:
          a: $status_code
          b: 200
      - function: equal
        with:
          a: $status_code
          b: 405

#   - name: test delete
#     function: http.delete
#     with:
#       url: https://example.com
#       output: text
    """

class ExecutorTests(unittest.TestCase):
    def setUp(self):
        self.recipe = self._load_base_recipe()
        return super().setUp()

    def _load_base_recipe(self):
        return utils.load_recipe(yaml.safe_load(data))

    def test_load_recipe(self):
        recipe = utils.load_recipe(yaml.safe_load(data))
        self.assertEqual(recipe.name, 'check site alive')
        self.assertEqual(recipe.kind, 'test.availability')
        self.assertEqual(recipe.args, [])
        self.assertDictContainsSubset(recipe.steps[0].with_, {"url": "https://google.com"})

    def test_basic_recipe_executor(self):
        e = executor.Executor()
        res = e.execute_recipe(self.recipe)
        self.assertTrue(res[0].success)

    def test_http_functions(self):
        recipe = utils.load_recipe(yaml.safe_load(http_lib_data))
        e = executor.Executor()
        res = e.execute_recipe(recipe)
        print(res)
        self.assertTrue(res[0].success)
        # here as we requested
        # self.assertFalse(res[1].success)
        self.assertTrue(res[2].success)
