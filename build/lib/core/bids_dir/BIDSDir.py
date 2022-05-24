"""
Metaclass acting as a factory for ``bidspathlib.bids_dir`` subclasses.

Subclasses inherit from ``bidspathlib.core.BIDSDirAbstract.BIDSDirAbstract``.
Each subclass corresponds to the BIDS entities whose name is a directory
in a BIDS dataset.
Each of these instances have three common methods
to facilitate navigation within the dataset, namely
``glob``, ``iterdir`` and ``rglob``.

These methods are implementations of the homologous method of
``pathlib.Path`` or ``pathlib.PurePath`` objects with two twists:

    * [1] ".bidsignore" filtering
    The files and directories mentioned in the
    ".bidsignore" file (if any) are automatically ignored.

    * [2] Automatic instantiation (like ``pathlib`` objects would)
    The methods return already instantiated
    ``BIDSDir`` or ``BIDSFile`` objects.


"""

import os
from os import PathLike
from typing import Union, Text, Iterator

from ..BIDSDirAbstract import BIDSDirAbstract

__path__ = [os.path.join('..', '__init__.py')]


class BIDSDir(BIDSDirAbstract):
    """
    Metaclass for directories in a BIDS Dataset.

    Subclasses:
        ``BIDSDir``
        ``Datatype``
        ``Derivatives``
        ``Session``
        ``Subject``
    """
    __slots__, __fspath__ = (), BIDSDirAbstract.__fspath__
    def __type__(self): return type(self)

    def __get_entities__(self):
        return super().__get_entities__()

    def __new__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__new__(*args, **kwargs)

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)

    def glob(self, pattern: Text) -> Iterator[Union[Text, PathLike]]:
        """
        Yields all existing paths matching a relative pattern in this subtree.

        Files defined in the '.bidsignore' file are omitted.

        """
        _cls = self.__bases__[0].__subclasses__()[1]
        yield from map(_cls, self.__bases__[0].glob(pattern))

    def iterdir(self) -> Iterator[Union[Text, PathLike]]:
        """
        Iterate over paths in this directory.

        Does not yield any result for the special paths
        '.' and '..'. and those defined in the '.bidsignore' file.
        """
        _cls = self.__bases__[0].__subclasses__()[1]
        yield from map(_cls, self.__bases__[0].iterdir())

    def rglob(self, pattern: Text) -> Iterator[Union[Text, PathLike]]:
        """
        Recursively yields all paths matching ``pattern`` in this subtree.

        Paths defined in the '.bidsignore' file are omitted.
        Args:
            pattern: str
                Pattern relative to ``self.path``.

        Returns: Iterator
        """
        _cls = self.__bases__[0].__subclasses__()[1]
        yield from map(_cls, self.__bases__[0].rglob(pattern))
