#!/usr/bin/env python3

from os import PathLike
from typing import List, Union, Text

from bids_path.core.bids_file.BehFile import BehFile
from bids_path.core.bids_file.EventsFile import EventsFile
from bids_path.core.bids_file.FMRIFile import FMRIFile
from bids_path.core.bids_file.MRIFIle import MRIFile
from bids_path.core.bids_file.PhysioFile import PhysioFile
from bids_path.core.bids_file.SidecarFile import SideCarFile
from bids_path.core.BIDSFileAbstract import BIDSFileAbstract


class BIDSFile(BIDSFileAbstract):
    """
    Metaclass for files in a BIDS dataset.

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __new__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__new__(*args, **kwargs)

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)


__all__: List = [
    "BehFile", "EventsFile", "FMRIFile", "MRIFile", "PhysioFile",
    "SideCarFile", "BIDSFileAbstract", "BIDSFile"
]
