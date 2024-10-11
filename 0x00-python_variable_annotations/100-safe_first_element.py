#!/usr/bin/env python3
"""Type-annotated function"""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Function that augments the correct duck-typed annotations"""
    if lst:
        return lst[0]
    return None
