#!/usr/bin/env python3

from os import PathLike
from os.path import join
from typing import NamedTuple, Union

from bids_path.constants.BIDSPathConstants import (
    Datatypes, DATATYPES_DESC_DICT, DATATYPES_DESCRIPTIONS,
    SES_DESCRIPTION, DATATYPE_STRINGS,
)
from bids_path.core.BIDSDirAbstract import BIDSDirAbstract
from ... import docstring_parameter
from .Datatype import Datatype


@docstring_parameter(SES_DESCRIPTION)
class Session(BIDSDirAbstract):
    """
    Files associated with measurements from a single participant's visit.

    {0}\n
    """
    __slots__ = DATATYPE_STRINGS
    def __type__(self): return type(self)

    def __instancecheck__(self, instance):
        return all((hasattr(instance, 'entities'),
                    self.is_session(instance)))

    def __getitem__(self, value: Union[int, slice, str]):
        if isinstance(value, str):
            return object.__getattribute__(self, value)
        return object.__getattribute__(self, self.__slots__[value])

    def __get__(self, value: Union[str, int]):
        if isinstance(value, str):
            return object.__getattribute__(self, value)
        else:
            return self.__getitem__(self.__slots__[value])

    def __init__(self, src: Union[str, PathLike], **kwargs):
        super().__init__(src, **kwargs)
        _dtypes = dict(zip(DATATYPE_STRINGS, self.datatypes))
        [property(fget=_dtypes.get,
                  fset=setattr(self, key, _dtypes.get(key)),
                  doc='\n'.join((_dtypes.get(key).__doc__,
                                 DATATYPES_DESC_DICT[key])))
         for key in _dtypes.keys()]

    @property
    @docstring_parameter(Datatype.__doc__, DATATYPES_DESCRIPTIONS)
    def datatypes(self) -> NamedTuple:
        """{0}\n{1}\n"""
        def fetch_datatype(src: Union[str, PathLike]):
            try:
                return Datatype(src)
            except (FileNotFoundError, TypeError):
                return ''
        return Datatypes(**{_name: fetch_datatype(join(self, _name))
                            for _name in self.__slots__})


# class _Derivatives(Session):
#     def __init__(self, derivatives_path: Union[str, PathLike], **kwargs):
#         super().__init__(derivatives_path, **kwargs)
