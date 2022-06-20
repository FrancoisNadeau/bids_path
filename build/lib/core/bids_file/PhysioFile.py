"""
Class for physiological json_docs files.

"""

import os
from typing import Text, Union

from ...core.BIDSFileAbstract import BIDSFileAbstract

__path__ = [os.path.join('..', '__init__.py')]


class PhysioFile(BIDSFileAbstract):
    """
    Class for physiological json_docs files.

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      self.is_physio_file(instance))
        return True if all(conditions) else False

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
