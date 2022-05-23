
from os import PathLike
from typing import Union, Text

from .core.BIDSPathAbstract import BIDSPathAbstract
from .core.bids_file.BIDSFile import BIDSFile
from .core.bids_dir.BIDSDir import BIDSDir


class BIDSPath(BIDSPathAbstract):
    __slots__ = ()
    def __type__(self): return type(self)

    def __new__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__new__(*args, **kwargs)

    @classmethod
    def __prepare__(cls, src: Union[Text, PathLike]):
        _mapper = (
            (cls.isfile(src), BIDSFile),
            (cls.isdir(src), BIDSDir)
        )
        _cls = next(filter(lambda item: bool(item[0]), _mapper))
        keywords = super().__get_entities__(src)._asdict()
        subclass = _cls[1](src)
        subclass.__set_from_dict__(keywords)
        return subclass

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)
