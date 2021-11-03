from __future__ import annotations
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Any, List, Dict, Optional

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
    test: Optional[Test]


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
    args: List[str]
    steps: List[Step]
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

