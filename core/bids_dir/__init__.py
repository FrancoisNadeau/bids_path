
"""
Submodule for directories in a BIDS dataset.

"""

import os
from typing import List

from ..BIDSDirAbstract import BIDSDirAbstract
from ..bids_dir import (
    BIDSDir, Datatype, Derivatives, Session, Subject
)

__all__: List = [
    "BIDSDirAbstract", "BIDSDir", "Datatype",
    "Session", "Subject", "Derivatives"
]

__path__ = [os.path.join('..', '..', 'core', '__init__.py')]
