#!/usr/bin/env python3

from os import PathLike
from typing import Text, Union

from bids_path.core.BIDSFileAbstract import BIDSFileAbstract


class PhysioFile(BIDSFileAbstract):
    """
    Class for physiological data files.

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      self.is_physio_file(instance))
        return True if all(conditions) else False

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)
