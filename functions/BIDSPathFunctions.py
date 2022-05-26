
"""
Path components-based file and directory identification in a BIDS dataset.

Functions to identify components of the BIDS-Schema within
a file or directory's name or path in a dataset.
This allows easy navigation through files and directories by
mapping the BIDS dataset hierarchy.

See <https://github.com/bids-standard/bids-schema/tree/main/versions/latest>
for more details.
"""

import json
import os
import warnings
from datetime import datetime as dt
from glob import iglob
from os import PathLike
from os.path import basename, exists, getctime
from pathlib import Path
from typing import (
    Dict, Generator, Iterable, Iterator,
    List, Optional, Text, Tuple, Union
)

from .BIDSDirID import (
    IsBIDSRoot, IsDatasetRoot, IsSubjectDir, IsSessionDir
)
from bids_validator import BIDSValidator
from more_itertools import flatten

from ..constants.BIDSPathConstants import (
    BVE_MESSAGE, DD_FILE, TIME_FORMAT,
    Entities, EntityStrings, Components
)
from ..constants.Modality import Modalities, Modality
from .BIDSPathCoreFunctions import (
    find_datatype, ComponentsGen, EntityGen, EntityStringGen
)


def root_path() -> Text:
    """
    Returns platform-independant root/drive directory.

    From the author:
    "On Linux this returns '/'.
    On Windows this returns 'C:\\' or whatever the current drive."

    References:
        <https://stackoverflow.com/questions/12041525/a-system-independent-way-using-python-to-get-the-root-directory-drive-on-which-p>
    """
    try:
        return os.path.abspath(os.path.sep)
    except RecursionError:
        return str(Path.cwd().root)


def _add_root(src: Union[Text, PathLike]) -> Union[Text, PathLike]:
    """
    Appends root directory or drive letter before path ``src``.

    """
    return os.path.join(root_path(), str(src))


def RelativeToRoot(src: Union[Text, PathLike]) -> Union[Text, PathLike]:
    """
    Returns ``self`` to be relative to the dataset's root.

    Allows ``BIDSValidator`` to perform its tasks.
    """
    return _add_root(Path(str(src)).relative_to(BIDSRoot(src)))


def Validate(src: Union[Text, PathLike]) -> bool:
    """
    Returns True if file path adheres to BIDS.

    Main method of the validator. uses other class methods for checking
    different aspects of the file path.

    Args:
        src: str or PathLike
            Path pointing to a file or directory within a BIDS dataset.
    Note:
        Path ``src`` is automatically rendered relative
        to the root of the BIDS dataset before validation.
    """
    _src = RelativeToRoot(str(src))
    return BIDSValidator().is_bids(str(_src))


def SubDir(src: Union[Text, PathLike]
           ) -> Union[Text, PathLike]:
    """
    Returns the subject-level directory path of ``src``, if any.

    If ``src`` points to either a modality agnostic file or to
    a dataset's top-level directory, returns an empty string ``''``.
    """
    try:
        return src if IsSubjectDir(src) else\
            next(filter(IsSubjectDir, Path(str(src)).parents))
    except StopIteration:
        return ''


def SesDir(src: Union[Text, PathLike]) -> Union[Text, PathLike]:
    """
    Returns the session-level directory path of ``src``, if any.

    If ``src`` points to either a modality agnostic file,
    to a dataset's top-level directory or to a subject-level directory,
    returns an empty string ``''``.
    """
    try:
        return src if IsSessionDir(src) else \
            next(filter(IsSessionDir, Path(str(src)).parents))
    except StopIteration:
        return ''


def BIDSRoot(src: Union[Text, PathLike]) -> PathLike:
    """
    Returns a BIDS dataset's top-level directory.

    If the current dataset is in the derivatives sub dataset,
    returns the top directory of this sub dataset.
    """
    return src if IsBIDSRoot(src) else \
        next(filter(IsBIDSRoot, Path(str(src)).parents))


def DatasetRoot(src: Union[Text, PathLike]) -> Union[Text, PathLike]:
    """
    Returns the topmost-level directory (derivatives notwithstanding).

    """
    try:
        assert src
        return src if IsDatasetRoot(src) else \
            next(filter(IsDatasetRoot, Path(src).parents))
    except AssertionError:
        pass
    except StopIteration:
        raise FileNotFoundError


def DerivativesRoot(src: Union[Text, PathLike]
                    ) -> Union[Text, PathLike]:
    """
    Returns the root directory of a derived dataset.

    """
    _d_dir = os.path.join(DatasetRoot(str(src)), 'derivatives')
    return Path(_d_dir) if exists(_d_dir) else ''


def DatasetName(src: Union[Text, PathLike]) -> Text:
    """
    Returns the name of the dataset.

    For raw data, returns the name of the topmost dataset directory.
    For derivatives dataa, returns the name of the pipeline used.
    It SHOULD correspond to the name of the said data derivatives
    directory in lowercase.
    """
    return basename(BIDSRoot(str(src)))


def DatasetDescription(src: Union[Text, PathLike]) -> Dict:
    """
    Returns 'dataset_description.json' file's contents as a Dict.

    """
    _desc_path = Path(BIDSRoot(src)).joinpath(DD_FILE)
    try:
        return json.loads(_desc_path.read_text())
    except FileNotFoundError:
        warnings.warn(UserWarning(BVE_MESSAGE))


def DatatypeModality(src: Union[Text, PathLike]
                     ) -> Union[Text, Modality]:
    """
    Returns a ``Modality`` object.

    A ``Modality`` object contains the name and
    documentation about a file's datatype
    brain recording modality.

    Please see ```help(Modality)``` for details.
    """
    try:
        return next((_m for _m in Modalities
                     if find_datatype(src) in
                     _m.datatypes))
    except StopIteration:
        return ''


def FormattedCtime(src: Union[Text, PathLike],
                   time_fmt: Text = TIME_FORMAT) -> Text:
    """
    Returns a formatted string from the creation timestamp of path ``src``.

    Args:
        src: str or PathLike
            Path on the file-system

        time_fmt: str (Default="%d %m %Y, %H:%M")
            Formatting string passed to the
            ``time.strftime`` function.
    """
    file_time = dt.fromtimestamp(getctime(src))
    return file_time.strftime(time_fmt)


def GetEntities(src: Union[Text, PathLike]) -> Tuple:
    """
    Returns a ``namedtuple`` object of BIDS entities.

    """
    return Entities(**dict(EntityGen(src)))


def GetEntityStrings(src: Union[Text, PathLike]
                     ) -> Tuple:
    """
    Returns a ``namedtuple`` object of BIDS entities key-value string pairs.

    """
    return EntityStrings(**dict(EntityStringGen(src)))


def GetComponents(src: Union[Text, PathLike]) -> Tuple:
    """
    Returns a ``namedtuple`` object of BIDS path components key-value pairs.

    """
    return Components(**dict(ComponentsGen(src)))


def PathsByPatterns(src: Union[Text, PathLike],
                    patterns: Iterable[Text],
                    ) -> Iterator:
    """
    Returns an iterator of paths matching the provided patterns.

    Patterns should match the '.gitignore' syntax.
    """
    _type = type(src)
    patterns = [patterns] if isinstance(patterns, str) else patterns
    _paths = flatten(iglob(os.path.join(src, _pat), recursive=True)
                     for _pat in patterns)
    yield from iter(set(map(_type, _paths)))


def GetBidsignore(src: Union[Text, PathLike]) -> Generator:
    """
    Yields paths matching patterns defined in the '.bidsignore' file.

    """
    try:
        assert src
        _ds_root = DatasetRoot(src)
        _ignore_path = os.path.join(_ds_root, '.bidsignore')
        _lines = Path(_ignore_path).read_text().splitlines()
        yield from PathsByPatterns(_ds_root, _lines)
    except AssertionError:
        pass
    except FileNotFoundError:
        yield from iter(set())


def GetDerivativesNames(src: Union[Text, PathLike],
                        ignore: Optional[Union[Iterable[Text], Text]] = None
                        ) -> Tuple:
    """
    Returns the pipeline names of software used to derive source data.

    Args:
        src: str or PathLike
            Any path in a BIDS dataset.

        ignore: Iterable (optional)
            Paths of files and directories to ignore
            (as defined in '.bidsignore').
    """
    _ignore = set(ignore) if ignore else GetBidsignore(src)
    _d_root = Path(DerivativesRoot(src))
    _d_paths = set(_d_root.iterdir()).difference(_ignore)
    return tuple(map(lambda p: p.name, _d_paths))



__methods__: Tuple = (
    root_path, _add_root, RelativeToRoot,
    Validate, SubDir, SesDir, BIDSRoot, DatasetRoot,
    DerivativesRoot, DatasetName, DatasetDescription,
    DatatypeModality, FormattedCtime, GetComponents,
    GetEntities, GetEntityStrings, PathsByPatterns,
    GetBidsignore, GetDerivativesNames
)
__all__: List = (
    "root_path", "_add_root", "RelativeToRoot",
    "Validate", "SubDir", "SesDir", "BIDSRoot", "DatasetRoot",
    "DerivativesRoot", "DatasetName", "DatasetDescription",
    "DatatypeModality", "FormattedCtime", "GetComponents",
    "GetEntities", "GetEntityStrings", "PathsByPatterns",
    "GetBidsignore", "GetDerivativesNames",
    "__methods__"
)
