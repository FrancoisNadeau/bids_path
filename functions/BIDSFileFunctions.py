
"""
Functions to retrieve attributes from files in a BIDS dataset.

The functions defined here are all implemented as
class methods of the ``BIDSPathBase.BIDSPathBase`` object.
"""

import json

from nibabel.nifti1 import Nifti1Image
from nilearn.image import load_img
from os import PathLike
from os.path import dirname
from pandas import read_csv, Series
from typing import (
    Dict, Iterable, List, Optional, Text, Tuple, Union
)

from ..general_methods import GetHashCheckSum
from ..constants.bidspathlib_docs import (
    NIFTI_ERRORS, NIFTI_EXTENSIONS
)
from .BIDSFileID import (
    IsNifti, IsEvent, IsBeh, IsSidecar
)
from .BIDSPathCoreFunctions import (
    find_entity, find_extension
)
from .BIDSPathFunctions import BIDSRoot, SubDir


def ShapeLength(src: Union[Text, Nifti1Image, PathLike]
                ) -> int:
    """
    Returns the number of dimensions of a nifti image file.

    """
    if not find_extension(src) in NIFTI_EXTENSIONS:
        return 0
    try:
        return len(load_img(str(src)).shape)
    except NIFTI_ERRORS:
        return 0


def GetNiftiImage(src: Union[Text, PathLike]
                  ) -> Union[Tuple, Nifti1Image]:
    """
    Returns a ``Nifti1Image`` from a nifti file.

    Returns an empty tuple if ``src`` doesn't point to a valid file.
    """
    try:
        if find_extension(src) in {'.nii', '.nii.gz'}:
            return load_img(str(src))
        else:
            raise NIFTI_ERRORS[-1]
    except NIFTI_ERRORS:
        return ()


def GetImgHeader(img: Nifti1Image) -> Dict:
    """
    Returns the nifti image's header as a dictionary.

    """
    try:
        return dict(img.header)
    except NIFTI_ERRORS:
        return {}


def GetTR(img: Nifti1Image) -> float:
    """
    Returns a ``Nifti1Image`` scan's repetition time from its header.

    """
    try:
        return float(img.header.get_zooms()[-1])
    except NIFTI_ERRORS:
        return 0.0


def GetFrameTimes(img: Nifti1Image) -> Iterable:
    """
    Returns scan frame onset times from the repetition time of ``img``.

    """
    try:
        _shape, tr, result, start = img.shape[-1], GetTR(img), [], 0
        for frame in range(_shape):
            start += tr
            result.append(start)
        return result
    except NIFTI_ERRORS:
        return []


__methods__: Tuple = (
    ShapeLength, GetFrameTimes, GetImgHeader, GetNiftiImage, GetTR
)

__all__: List = [
    "ShapeLength", "GetFrameTimes", "GetImgHeader", "GetNiftiImage", "GetTR",
    "__methods__"
]
