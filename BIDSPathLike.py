
"""
Extension of the abstract base class ``os.PathLike`` for BIDS datasets.

"""

import collections
import os
from abc import abstractmethod
from typing import runtime_checkable, Protocol, Union, Text, Container

from .constants.bidspathlib_docs import GenericAlias

_check_methods = getattr(collections._collections_abc, '_check_methods')
__path__ = [os.path.join('..', '__init__.py')]


@runtime_checkable
class BIDSPathLike(Protocol):
    """
    Extension of the abstract base class ``os.PathLike``.

    Motivation:
        * Comply with python's file system path protocol.
        * Allow BIDS entity-based functionalities.
    """
    __slots__, __rmod__ = (), NotImplemented
    __class_getitem__ = classmethod(GenericAlias)

    @classmethod
    def __subclasshook__(cls, subclass):
        methods = ('__fspath__', '__get_entities__')
        if cls is os.PathLike:
            return _check_methods(subclass, *methods)
        return NotImplemented

    @abstractmethod
    def __fspath__(self) -> Union[Text, bytes]:
        """
        Return the file system path representation of the object.

        If the object is ``str`` or ``bytes``, then allow it to pass through as-is.
        If the object defines ``__fspath__()``, then return the result of that method.
        All other types raise ``TypeError``.

        Equivalent to ``super().__fspath__()``.

        """
        raise NotImplementedError

    @abstractmethod
    def __get_entities__(self) -> Container[Text]:
        """
        Returns an immutable container object of BIDS entities.

        """
        raise NotImplementedError
