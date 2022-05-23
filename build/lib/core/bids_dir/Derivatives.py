
from os import PathLike
from typing import Union, Text

from ...constants.fMRIPrepEntities import FMRIPrepEntities
from ...core.bids_dir.Subject import Subject


class Derivatives(Subject):
    """
    Class to access a participant's derived data.

    The participant (subject) level is chosen to
    better integrate FMRIPrep derivatives, as the
    pipeline preprocesses raw data at this level.
    """
    __slots__ = 'd_entities'

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)
        object.__setattr__(self, 'd_entities', FMRIPrepEntities)
