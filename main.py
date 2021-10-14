import json
import yaml
import logging
from recipe_executor import Executor
import sys

logging.basicConfig(level=logging.DEBUG)


filename = sys.argv[1]

with open(filename, 'r') as f :
    content = yaml.safe_load(f.read())

e = Executor()

args = {
    "username": "<>",
    "password":"<>",
    "pageToLoad": 36,
    "wordToFind": "Formation"
}

e.add_env(args)

result = e.execute_recipe(content)


print(result)

with open('res.json', 'w') as f:
    json.dump([r.to_json() for r in result], f, indent=2)
