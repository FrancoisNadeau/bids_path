"""
Class to access a participant's derived data.

"""

import os
from typing import Union, Text

from ...fMRIPrepEntities import FMRIPrepEntities
from ...core.bids_dir.Subject import Subject

__path__ = [os.path.join('..', '__init__.py')]


class Derivatives(Subject):
    """
    Class to access a participant's derived data.

    The participant (subject) level is chosen to
    better integrate FMRIPrep derivatives, as the
    pipeline preprocesses raw data at this level.
    """
    __slots__, __fspath__ = 'd_entities', Subject.__fspath__
    def __type__(self): return type(self)

    def __get_entities__(self):
        return super().__get_entities__()

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
        object.__setattr__(self, 'd_entities', FMRIPrepEntities)
