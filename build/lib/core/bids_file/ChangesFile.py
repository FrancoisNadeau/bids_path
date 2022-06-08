"""
Class representing a CHANGES file in a BIDS dataset.

"""

import os
from pprint import pprint
from typing import Text, Union

from ..BIDSFileAbstract import BIDSFileAbstract

__path__ = [os.path.join('../..', '__init__.py')]


class ChangesFile(BIDSFileAbstract):
    """
    Class representing a CHANGES file in a BIDS dataset.

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      os.path.basename(instance) == 'CHANGES')
        return all(conditions)

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)

    def view(self):
        _contents = self.path.read_text().strip()
        pprint(_contents)
