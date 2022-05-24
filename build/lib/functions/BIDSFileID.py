
"""
Functions returning boolean values according to path characteristics.

Each function name starts by "Is" and indicates to which type
a file within a BIDS dataset corresponds to.

New bids_path_functions should be independent of other ``BIDSPath`` files,
except for those defined in the ``bidspathlib.constants.BIDSPathConstants``
and ``bidspathlib.bids_path_functions.BIDSPathCoreFunctions`` modules.
This is to avoid circular imports.
"""

import os
from os.path import isfile
from typing import List, Union, Text, Tuple

from nibabel import Nifti1Image
from nilearn.image import load_img

from .core_functions import find_bids_suffix

NIFTI_EXTENSIONS = {
    '.dtseries.nii', '.func.gii', '.gii',
    '.gii.gz', '.nii', '.nii.gz'
}


def IsNifti(src: Union[Text, Nifti1Image, os.PathLike]) -> bool:
    """
    Returns True if the path ``src`` points to a Nifti file.
    """
    return True if isinstance(src, Nifti1Image) else \
        str(src).split('.', maxsplit=1)[1] in NIFTI_EXTENSIONS


def Is4D(src: Union[Text, Nifti1Image, os.PathLike]
         ) -> bool:
    """
    Returns True if ``src`` points to a 4-dimensional Nifti file.

    """
    try:
        assert IsNifti(src)
        return len(load_img(str(src)).shape) == 4
    except AssertionError:
        return False


def Is3D(src: Union[Text, Nifti1Image, os.PathLike]
         ) -> bool:
    """
    Returns True if ``src`` points to a 3-dimensional Nifti file.

    """
    try:
        assert IsNifti(src)
        return len(load_img(str(src)).shape) == 3
    except AssertionError:
        return False


def IsEvent(src: Union[Text, os.PathLike]
            ) -> bool:
    """
    Returns True if path ``src`` points to a task events file.

    """
    return all((isfile(src), find_bids_suffix(src) == 'events'))


def IsBeh(src: Union[Text, os.PathLike]) -> bool:
    """
    Returns True if path ``src`` points to behavioural recordings file.

    """
    return all((isfile(str(src)), find_bids_suffix(src) == 'beh'))


def IsPhysio(src: Union[Text, os.PathLike]) -> bool:
    """
    Returns True if path ``src`` points to physiological recordings file.

    """
    return all((isfile(str(src)), find_bids_suffix(src) == 'physio'))


def IsSidecar(src: Union[Text, os.PathLike]) -> bool:
    """
    Returns True if ``src`` points to a .json sidecar file.

    """
    return str(src).split('.', maxsplit=1)[1] == '.json'


__methods__: Tuple = (
    IsBeh, IsEvent, IsNifti, IsPhysio, IsSidecar, Is3D, Is4D
)

__all__: List = [
    "IsBeh", "IsEvent", "IsNifti", "IsPhysio", "IsSidecar", "Is3D", "Is4D",
    "__methods__"
]

__path__: List = [os.path.join('..', '__init__.py')]
