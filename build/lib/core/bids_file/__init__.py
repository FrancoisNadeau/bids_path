
import os
from typing import List

from ..BIDSFileAbstract import BIDSFileAbstract
from ..bids_file import (
    BehFile, BIDSFile, EventsFile, FMRIFile, MRIFile,
    PhysioFile, SideCarFile
)

__all__: List = [
    "BehFile", "BIDSFile", "EventsFile", "FMRIFile",
    "MRIFile", "PhysioFile", "SideCarFile", "BIDSFileAbstract"
]

__path__ = [os.path.join('..', '..', 'core', '__init__.py')]
