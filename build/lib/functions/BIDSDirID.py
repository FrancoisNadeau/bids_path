
"""
Functions returning boolean values according to path characteristics.

Each function name starts by "Is" and indicates to which hierarchical
level a directory within a BIDS dataset corresponds to.

New bids_path_functions should be independent of other ``BIDSPath`` files,
except for those defined in the ``bidspathlib.constants.BIDSPathConstants``
and ``bidspathlib.bids_path_functions.BIDSPathCoreFunctions`` modules.
This is to avoid circular imports.
"""

import os
import re
from os import PathLike
from os.path import basename, isdir
from pathlib import Path
from typing import List, Union, Text, Tuple


def IsBIDSRoot(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if ``src`` points to a BIDS dataset's top-level directory.

    If ``src`` is in a derivatives sub dataset,
    returns this sub dataset's top-level directory.
    """
    try:
        return 'dataset_description.json' in os.listdir(str(src))
    except NotADirectoryError:
        return False


def IsDatasetRoot(src: Union[Text, bytes, PathLike]) -> bool:
    """
    Returns True if ``src`` points to the BIDS dataset's topmost directory.

    """
    try:
        assert Path(src).is_dir()
        return all(('dataset_description.json' in os.listdir(src),
                    'derivatives' not in os.fspath(src)))
    except (AssertionError, FileNotFoundError, NotADirectoryError, TypeError):
        return False


def IsSubjectDir(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if ``src`` points to a subject-level directory.

    """
    return basename(src).startswith('sub-') if isdir(src) else False


def IsSessionDir(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if ``src`` points to a session-level directory.

    """
    return basename(src).startswith('ses-') \
        if isdir(src) else False


def IsDatatypeDir(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if ``src`` points to a datatype-level directory.

    """
    _datatypes = {
        'anat', 'beh', 'dwi', 'eeg', 'fmap', 'func',
        'ieeg', 'meg', 'micr', 'perf', 'pet'
    }
    return basename(src) in _datatypes if isdir(src) else False


def IsDerivatives(src: Union[Text, PathLike]) -> bool:
    """
    Indicates if the dataset is derived from another one or not.

    """
    return 'derivatives' in str(src)


def IsDerivativesRoot(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if ``src`` points to a derived dataset's root directory.

    """
    return all((IsBIDSRoot(str(src)), IsDerivatives(str(src))))


def IsFMRIPrepDerivatives(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if path ``src`` points to a file or directory made with FMRIPrep.

    """
    lookup = ('derivatives', 'fmriprep')
    return all((re.findall(l, str(src).casefold()) for l in lookup))


__methods__: Tuple = (
    IsBIDSRoot, IsDatasetRoot, IsSubjectDir,
    IsSessionDir, IsDatatypeDir, IsDerivatives,
    IsDerivativesRoot, IsFMRIPrepDerivatives
)

__all__: List = [
    "IsBIDSRoot", "IsDatasetRoot", "IsSubjectDir",
    "IsSessionDir", "IsDatatypeDir", "IsDerivatives",
    "IsDerivativesRoot", "IsFMRIPrepDerivatives",
    "__methods__"
]

__path__: List = [os.path.join('..', '__init__.py')]
