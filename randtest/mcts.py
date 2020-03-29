"""
Module:
Collection of functions for various measures of central tendencies
"""

from types import GeneratorType


def arithmetic_mean(data: GeneratorType) -> float:
    """Arithmetic mean computed on generator object"""
    sum_data_pnts, num_data_pnts = 0, 0
    for item in data:
        sum_data_pnts += item
        num_data_pnts += 1
    return sum_data_pnts / num_data_pnts


def trimmed_mean(data: GeneratorType, trim_percent=.2) -> float:
    """Trimmed mean computed on generator object"""
    data_sorted = tuple(sorted(data))
    num_data_pnts = len(data_sorted)
    lowercut = int(num_data_pnts * trim_percent)
    uppercut = num_data_pnts - lowercut
    data_trimmed = data_sorted[lowercut:uppercut]
    return sum(data_trimmed) / len(data_trimmed)
