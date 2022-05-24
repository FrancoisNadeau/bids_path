
"""
BIDSPath module speed and error tests.

References:
    TimeCheck:
    https://www.geeksforgeeks.org/class-as-decorator-in-python/
    ErrorCheck:
    https://www.geeksforgeeks.org/class-as-decorator-in-python/
"""

import os
from .ErrorCheck import ErrorCheck
from .TimeCheck import TimeCheck

__all__ = ["ErrorCheck", "TimeCheck"]

__path__ = [os.path.join('..', '..', 'core', '__init__.py')]
