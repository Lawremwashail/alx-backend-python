#!/usr/bin/env python3
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Function that returns sum of mixed list of integers and float"""

    num_list: float = 0.0
    for i in mxd_lst:
        num_list += i

    return num_list
