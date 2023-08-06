"""
Distributions illustrating three times of dependency among two variables.
"""

from .. import Distribution

__all__ = ['stacked', 'mixed']

_stacked_outcomes = []
_stacked_pmf = []
stacked = Distribution(_stacked_outcomes, _stacked_pmf)

_mixed_outcomes = []
_mixed_pmf = []
mixed = Distribution(_mixed_outcomes, _mixed_pmf)
