from __future__ import annotations
from typing import Callable, TypedDict
from entities.living.goods.base_good import BaseGood


# defiles the keys and type hints them for a dict
class ReplaceInfo(TypedDict):  # total=false allows a dict with only 1 key
    replace: Callable[..., BaseGood]
    cost: int
