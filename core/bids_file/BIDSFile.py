#!/usr/bin/env python3

from bids_path.core import BIDSFile
from bids_path.core.bids_file import (
    MRIFile, FMRIFile, EventsFile, BehFile, PhysioFile, SideCarFile
)

__all__ = (
    MRIFile, FMRIFile, EventsFile, BehFile,
    PhysioFile, SideCarFile, BIDSFile
)
