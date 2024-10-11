#!/usr/bin/env python3
"""Type-annotated function"""
from typing import Sequence, Iterable, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Function that returns list of sequence and int"""
    return [(i, len(i)) for i in lst]
