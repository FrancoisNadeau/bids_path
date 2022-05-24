"""
Package containing the ``bidspathlib`` abstract base classes.

"""

import os.path

from ..core.BIDSDirAbstract import BIDSDirAbstract
from ..core.BIDSFileAbstract import BIDSFileAbstract
from ..core.BIDSPathAbstract import BIDSPathAbstract
from ..core.bids_dir import (
    BIDSDir, Datatype, Session, Subject, Derivatives
)
from ..core.bids_file import (
    BIDSFile, BehFile, EventsFile, FMRIFile, MRIFile,
    PhysioFile, SideCarFile
)

__all__ = [
    # core
    "BIDSDirAbstract", "BIDSFileAbstract", "BIDSPathAbstract",
    "bids_dir", "bids_file",
    # BIDSFile
    "BIDSFile", "BehFile", "EventsFile", "FMRIFile", "MRIFile",
    "PhysioFile", "SideCarFile",
    # BIDSDir
    "BIDSDir", "Datatype", "Session", "Subject", "Derivatives"
]

__path__ = [os.path.join('..', '__init__.py')]
