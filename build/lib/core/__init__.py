"""
Package containing the ``bidspathlib`` abstract base classes.

"""

import os.path

from ..core.bids_file import *
from ..core.bids_dir import (
    BIDSDirAbstract, BIDSDir, Dataset, Datatype,
    Session, Subject, Derivatives
)
from ..core.BIDSDirAbstract import BIDSDirAbstract
from ..core.BIDSFileAbstract import BIDSFileAbstract
from ..core.BIDSPathAbstract import BIDSPathAbstract
from ..core.bids_dir import (
    BIDSDir, Datatype, Dataset, Session, Subject
)
from .bids_dir.Derivatives import Derivatives
from ..core.bids_file import (
    BIDSFile, BehFile, ChangesFile, EventsFile, FMRIFile,
    GitAttributesFile, LicenseFile, MRIFile,
    PhysioFile, ReadMeFile, SideCarFile
)

__all__ = [
    # core
    "BIDSDirAbstract", "BIDSFileAbstract", "BIDSPathAbstract",
    # BIDSFile
    "BIDSFile", "BehFile", "ChangesFile", "EventsFile", "FMRIFile",
    "GitAttributesFile", "LicenseFile", "MRIFile", "PhysioFile",
    "ReadMeFile", "SideCarFile",
    # BIDSDir
    "BIDSDirAbstract", "BIDSDir", "Dataset", "Datatype",
    "Session", "Subject", "Derivatives"
]

__path__ = [os.path.join('..', '..', '__init__.py')]
