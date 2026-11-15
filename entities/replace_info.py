from __future__ import annotations
from typing import Callable, TypedDict
from entities.living.goods.base_good import BaseGood


# defiles the keys and type hints them for a dict
class ReplaceInfo(TypedDict):
    """The keys of a replacement entry: the good to replace with and its cost."""
    replace: Callable[..., BaseGood]
    cost: int
