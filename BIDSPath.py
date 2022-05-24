
"""
Main metaclass factory and preferred instantiation method.

"""

import os
from typing import List, Union, Text

from .core.BIDSPathAbstract import BIDSPathAbstract
from .core.bids_file.BIDSFile import BIDSFile
from .core.bids_dir.BIDSDir import BIDSDir
from .constants.BIDSPathConstants import ENTITY_STRINGS

__path__ = [os.path.join('..', '__init__.py')]


class BIDSPath(BIDSPathAbstract):
    """
    Main metaclass factory and preferred instantiation method.

    """

    __slots__, __fspath__ = (), BIDSPathAbstract.__fspath__
    def __type__(self): return type(self)

    def __new__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__new__(*args, **kwargs)

    def __get_entities__(self):
        return super().__get_entities__()

    @classmethod
    def __prepare__(cls, src: Union[Text, os.PathLike]):
        _mapper = (
            (cls.isfile(src), BIDSFile),
            (cls.isdir(src), BIDSDir)
        )
        _cls = next(filter(lambda item: bool(item[0]), _mapper))
        keywords = dict(zip(ENTITY_STRINGS,
                            super().__get_entities__(src)))
        subclass = _cls[1](src)
        subclass.__set_from_dict__(keywords)
        return subclass

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)


__all__: List = ["BIDSPath"]
