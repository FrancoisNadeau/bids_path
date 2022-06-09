
"""
Package exceptions.

CONTENTS:
    NiftiError

    NotNiftiFileError

    Not3DError

    Not4DError


"""

import os
from typing import List, Tuple

from nibabel.filebasedimages import ImageFileError
from nilearn._utils.exceptions import DimensionError

_bases = (DimensionError, ImageFileError)

__path__ = [os.path.join('..', '__init__.py')]


class NiftiError(TypeError):
    __slots__ = ('DimensionError', 'ImageFileError')

    @classmethod
    def __prepare__(cls, *args, **kwargs):
        return cls.__prepare__(*args, **kwargs)

    @classmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        [object.__setattr__(self, obj.__name__, obj)
         for obj in _bases]


class NotNiftiFileError(NiftiError, TypeError):
    """
    Exception to raise when attempting operations requiring a Nifti1Image object.

    """
    @property
    def message(self, *args) -> str:
        return '{} is not a nibabel.nifti1.Nifti1Image object.'.format(*args[0])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Not3DError(NiftiError):
    """
    Exception to raise when attempting operations requiring a 3D nifti image.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required_dimension = 3
        if kwargs:
            self.file_dimension = kwargs.get('file_dimension')
        else:
            self.file_dimension = args[0]


class Not4DError(NiftiError):
    """
    Exception to raise when attempting operations requiring a 4D nifti image.

    """
    __slots__ = ('required_dimension', 'file_dimension')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required_dimension = 4
        if kwargs:
            self.file_dimension = kwargs.get('file_dimension')
        else:
            self.file_dimension = args[0]


__classes__: Tuple = (
    NiftiError, NotNiftiFileError, Not3DError, Not4DError
)

__all__: List = [
    "NiftiError", "NotNiftiFileError", "Not3DError",
    "Not4DError", "__classes__"
]
