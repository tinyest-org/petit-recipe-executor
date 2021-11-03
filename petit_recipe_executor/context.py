from typing import Any


class Context:
    def __init__(self) -> None:
        self.data = {}

    def put(self, name: str, value: Any):
        self.data[name] = value

    # handle nested values with "." notation parent.nested
    def get(self, name: str):
        return self.data[name]
