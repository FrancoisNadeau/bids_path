"""
Metaclass acting as a factory for ``bidspathlib.bids_file`` subclasses.

Subclasses inherit from ``bidspathlib.core.BIDSFileAbstract.BIDSFileAbstract``.
Each subclass corresponds to the common file types for anatomical and functional
magnetic resonance imaging (MRI, fMRI) found in a BIDS dataset.

The factory``bidspathlib.bids_file.BIDSFile.BIDSFile`` instantiates objects acting as
interfaces for file identification, bundling and manipulation.

Each object has a ``buf`` property which is an instance of ``io.BytesIO`` containing
the file data as raw bytes. This property is read-only to prevent data contamination.
However, one can easily perform the desired operations by writing
to a different location on disk or in-memory stream.
"""

import os
from typing import Union, Text

from ..BIDSFileAbstract import BIDSFileAbstract

__path__ = [os.path.join('..', '__init__.py')]


class BIDSFile(BIDSFileAbstract):
    """
    Metaclass for files in a BIDS dataset.

    Subclasses:
        ``BIDSFile``
        ``BehFile``
        ``EventsFile``
        ``FMRIFile``
        ``MRIFile``
        ``PhysioFile``
        ``SideCarFile``

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __new__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__new__(*args, **kwargs)

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
