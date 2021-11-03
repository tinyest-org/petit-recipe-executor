import json
import logging
import sys

import yaml

from petit_monitor import Executor, load_recipe

# logging.basicConfig(level=logging.DEBUG)


filename = sys.argv[1]

with open(filename, 'r') as f :
    content = yaml.safe_load(f.read())

recipe = load_recipe(content)

e = Executor()

args = {
    "username": "<>",
    "password": "<>",
    "pageToLoad": 36,
    "wordToFind": "Formation",
}

e.add_env(args)

result = e.execute_recipe(recipe)


print(result)

with open('res.json', 'w') as f:
    json.dump([r.to_json() for r in result], f, indent=2)
