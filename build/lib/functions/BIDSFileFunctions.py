
"""
Functions to retrieve attributes from files in a BIDS dataset.

The functions defined here are all implemented as
class methods of the ``BIDSPathBase.BIDSPathBase`` object.
"""
import os.path

from nibabel.nifti1 import Nifti1Image
from nilearn.image import load_img
from numpy import arange
from numpy.typing import ArrayLike
from os import PathLike
from typing import Dict, List, Text, Tuple, Union

NIFTI_EXTENSIONS = {
    '.dtseries.nii', '.func.gii', '.gii',
    '.gii.gz', '.nii', '.nii.gz'
}


def ShapeLength(src: Union[Text, Nifti1Image, PathLike]
                ) -> int:
    """
    Returns the number of dimensions of a nifti image file.

    """

    if isinstance(src, Nifti1Image):
        return len(src.shape)
    else:
        try:
            assert str(src).split('.', maxsplit=1)[1] \
                   in NIFTI_EXTENSIONS
            return len(load_img(str(src)).shape)
        except AssertionError:
            return 0


def GetImgHeader(img: Nifti1Image) -> Dict:
    """
    Returns the nifti image's header as a dictionary.

    """
    try:
        return dict(img.header)
    except AttributeError:
        return {}


def GetTR(img: Nifti1Image) -> float:
    """
    Returns a ``Nifti1Image`` scan's repetition time from its header.

    """
    try:
        return float(img.header.get_zooms()[-1])
    except AttributeError:
        return 0.0


def GetFrameTimes(img: Nifti1Image) -> ArrayLike:
    """
    Returns scan frame onset times from the repetition time of ``img``.

    """
    try:
        return arange(img.shape[-1]) * GetTR(img)
    except AttributeError:
        return []


__methods__: Tuple = (
    ShapeLength, GetFrameTimes, GetImgHeader, GetTR
)

__all__: List = [
    "ShapeLength", "GetFrameTimes", "GetImgHeader",
    "GetTR", "__methods__"
]

__path__: List = [os.path.join('..', '__init__.py')]
