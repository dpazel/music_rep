"""

File: utility.py

Purpose: Various code in support of the code base.

"""
from timemodel.position import Position
from timemodel.duration import Duration
from timemodel.offset import Offset


def convert_to_numeric(value):
    if isinstance(value, Position):
        return value.position
    elif isinstance(value, Duration):
        return value.duration
    elif isinstance(value, Offset):
        return value.offset
    else:
        return value
