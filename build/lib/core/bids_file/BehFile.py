
from os import PathLike
from typing import Text, Union

from ..BIDSFileAbstract import BIDSFileAbstract


class BehFile(BIDSFileAbstract):
    """
    Class representing a behavioural task in a BIDS dataset.

    Derived from ``EventsFile``.
    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      self.is_beh_file(instance))
        return True if all(conditions) else False

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)
