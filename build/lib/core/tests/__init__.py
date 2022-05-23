
"""
BIDSPath module speed and error tests.

References:
    TimeCheck:
    <https://www.geeksforgeeks.org/class-as-decorator-in-python/>
    ErrorCheck:
    <https://www.geeksforgeeks.org/class-as-decorator-in-python/>
"""

from .ErrorCheck import ErrorCheck
from .TimeCheck import TimeCheck

__all__ = ["ErrorCheck", "TimeCheck"]
