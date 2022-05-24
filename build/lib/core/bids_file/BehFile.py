
import os
from typing import Text, Union

from ..BIDSFileAbstract import BIDSFileAbstract

__path__ = [os.path.join('..', '__init__.py')]


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

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
