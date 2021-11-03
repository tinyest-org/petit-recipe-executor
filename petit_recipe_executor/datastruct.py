from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

VARIABLE_TOKEN = "$"

FunctionParams = Dict[str, Any]


class Test(BaseModel):
    function: str
    with_: FunctionParams

    class Config:
        fields = {
            'with_': 'with'
        }

class Step(BaseModel):
    name: str
    function: str
    with_: FunctionParams
    returns: Optional[str]
    tests: Optional[List[Test]]


    class Config:
        # rename field with to with_
        fields = {
            'with_': 'with'
        }


class Recipe(BaseModel):
    name: str
    kind: str
    # should create class for later
    trigger: dict
    steps: List[Step]
    args: List[str] = []
    env: Dict[str, Any] = {}

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

