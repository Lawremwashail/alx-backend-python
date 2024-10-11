#!/usr/bin/env python3
"""Type-annotated function"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Function that  returns the sum of input_list"""

    num_list: float = 0.0
    for i in input_list:
        num_list += i

    return num_list
