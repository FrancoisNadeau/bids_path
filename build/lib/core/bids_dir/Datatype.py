
from operator import itemgetter
from os import PathLike
from typing import Any, Dict, Optional, Text, Union

from ..BIDSDirAbstract import BIDSDirAbstract
from ...constants.BIDSPathConstants import DATATYPES_DESCRIPTION
DATATYPE_BASE_FIELDS = ('description', 'long_name', 'specific')
# DATATYPE_SPEC_FIELDS = (
#     'name', 'bids_suffixes', 'extensions', 'datatypes', 'entities'
# )
# DatatypeSpec = namedtuple('DatatypeSpec', field_names=DATATYPE_SPEC_FIELDS)


class Datatype(BIDSDirAbstract):
    """
    Functional group of different types of data.

    Corresponds to a subdirectory into a subject's directory
    or within one of this subject's session directories, if any.

    References:
        <https://bids-specification.readthedocs.io/en/stable/02-common-principles.html>
        Bullet-point 6.
    """
    __slots__ = ('description', 'long_name', 'specific')
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        return all((hasattr(instance, 'entities'),
                    self.is_datatype_dir(instance)))

    def __index__(self, value: Any,
                  start: Optional[int] = 0,
                  stop: Optional[int] = 9223372036854775807,
                  ) -> int:
        args = (value, start, stop)
        try:
            return tuple(self.iterdir()).index(*args)
        except ValueError:
            try:
                _str_files = map(str, self._files)
                return tuple(_str_files).index(*args)
            except ValueError:
                raise ValueError


    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)
        _gen: Dict = DATATYPES_DESCRIPTION[self.datatype]
        _desc, _long_name, _spec = itemgetter(*DATATYPE_BASE_FIELDS)(_gen)
        self.__set_from_dict__(dict(description=_gen['description'],
                                    long_name=_gen['long_name'],
                                    specific=_spec))
