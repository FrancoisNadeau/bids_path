

import os
from typing import Union, Text

from ..BIDSDirAbstract import BIDSDirAbstract

__path__ = [os.path.join('..', '__init__.py')]


class Dataset(BIDSDirAbstract):
    __slots__ = ()

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
