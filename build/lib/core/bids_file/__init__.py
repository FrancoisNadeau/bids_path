"""
Submodule for files in a BIDS dataset.

"""

import os
from typing import List

from ..BIDSFileAbstract import BIDSFileAbstract
from ..bids_file import (
    BehFile, BIDSFile, ChangesFile, EventsFile, FMRIFile,
    GitAttributesFile, LicenseFile, MRIFile, PhysioFile,
    ReadMeFile, SideCarFile
)

__all__: List = [
    "BehFile", "BIDSFile", "ChangesFile", "EventsFile",
    "GitAttributesFile", "FMRIFile", "LicenseFile", "MRIFile",
    "PhysioFile", "ReadMeFile", "SideCarFile", "BIDSFileAbstract"
]

__path__ = [os.path.join('..', '..', 'core', '__init__.py')]
