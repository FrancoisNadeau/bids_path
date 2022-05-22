#!/usr/bin/env python3

"""
Functions returning boolean values according to path characteristics.

Each function name starts by "Is" and indicates to which type
a file within a BIDS dataset corresponds to.

New bidspath_functions should be independent of other ``BIDSPath`` files,
except for those defined in the ``bids_path.constants.BIDSPathConstants``
and ``bids_path.bidspath_functions.BIDSPathCoreFunctions`` modules.
This is to avoid circular imports.
"""

from nibabel import Nifti1Image
from nilearn.image import load_img
from os import PathLike
from os.path import isfile
from typing import List, Union, Text, Tuple

from bids_path.constants.BIDSPathConstants import NIFTI_EXTENSIONS, NIFTI_ERRORS
from bids_path.functions.BIDSPathCoreFunctions import find_extension, find_bids_suffix


def IsNifti(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if the path ``src`` points to a Nifti file.
    """

    return find_extension(src) in NIFTI_EXTENSIONS


def Is4D(src: Union[Text, Nifti1Image, PathLike]
         ) -> bool:
    """
    Returns True if ``src`` points to a 4-dimensional Nifti file.

    """
    if not find_extension(src) in NIFTI_EXTENSIONS:
        return False
    try:
        return len(load_img(str(src)).shape) == 4
    except NIFTI_ERRORS:
        return False


def Is3D(src: Union[Text, Nifti1Image, PathLike]
         ) -> bool:
    """
    Returns True if ``src`` points to a 3-dimensional Nifti file.

    """
    if not find_extension(src) in NIFTI_EXTENSIONS:
        return False
    try:
        return len(load_img(str(src)).shape) == 3
    except NIFTI_ERRORS:
        return False


def IsEvent(src: Union[Text, PathLike]
            ) -> bool:
    """
    Returns True if path ``src`` points to a task events file.

    """
    return all((isfile(src), find_bids_suffix(src) == 'events'))


def IsBeh(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if path ``src`` points to behavioural recordings file.

    """
    return all((isfile(str(src)), find_bids_suffix(src) == 'beh'))


def IsPhysio(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if path ``src`` points to physiological recordings file.

    """
    return all((isfile(str(src)), find_bids_suffix(src) == 'physio'))


def IsSidecar(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if ``src`` points to a .json sidecar file.

    """
    return find_extension(src) == '.json'


__methods__: Tuple = (
    IsBeh, IsEvent, IsNifti, IsPhysio, IsSidecar, Is3D, Is4D
)

__all__: List = [
    "IsBeh", "IsEvent", "IsNifti", "IsPhysio", "IsSidecar", "Is3D", "Is4D",
    "__methods__"
]
