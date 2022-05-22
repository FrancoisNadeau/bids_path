#!/usr/bin/env python3

from os import PathLike
from typing import Iterator, List, Text, Union

from bids_path.functions.general_methods import docstring_parameter
from bids_path.core.BIDSDirAbstract import BIDSDirAbstract
from bids_path.core.bids_dir.Datatype import Datatype
from bids_path.core.bids_dir.Session import Session
from bids_path.core.bids_dir.Subject import Subject


class BIDSDir(BIDSDirAbstract):
    """
    Metaclass for directories in a BIDS Dataset.

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __new__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__new__(*args, **kwargs)

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)

    @docstring_parameter(BIDSDirAbstract.glob.__doc__)
    def glob(self, pattern: Text) -> Iterator[Union[Text, PathLike]]:
        """{0}\n"""
        _cls = self.__bases__[0].__subclasses__()[1]
        yield from map(_cls, self.__bases__[0].glob(pattern))

    @docstring_parameter(BIDSDirAbstract.iterdir.__doc__)
    def iterdir(self) -> Iterator[Union[Text, PathLike]]:
        """{0}\n"""
        _cls = self.__bases__[0].__subclasses__()[1]
        yield from map(_cls, self.__bases__[0].iterdir())

    @docstring_parameter(BIDSDirAbstract.rglob.__doc__)
    def rglob(self, pattern: Text) -> Iterator[Union[Text, PathLike]]:
        """{0}\n"""
        _cls = self.__bases__[0].__subclasses__()[1]
        yield from map(_cls, self.__bases__[0].rglob(pattern))


class Derivatives(Subject):
    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)


__all__: List = [
    "BIDSDirAbstract", "Datatype", "Session", "Subject", "BIDSDir",
    "Derivatives"
]
