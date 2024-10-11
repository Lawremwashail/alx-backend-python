#!/usr/bin/env python3
"""Type-annotated function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Function that returns multiple of multiplier by float"""
    return lambda a: a * multiplier
