#!/usr/bin/env python3
"""Type-annotated function"""
from typing import TypeVar, Any, Union, Mapping
T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default: Union[T, None]
                     = None) -> Union[Any, T]:
    """Function that returns values from added params"""
    if key in dict:
        return dct[key]
    else:
        return default
