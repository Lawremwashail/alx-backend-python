#!/usr/bin/env python3
"""Type-annotated function"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Function that returns a tuple of a str and float """
    a = v ** 2
    return (k, a)
