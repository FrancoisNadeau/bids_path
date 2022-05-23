
"""
Functions to retrieve attributes from files in a BIDS dataset.

The functions defined here are all implemented as
class methods of the ``BIDSPathBase.BIDSPathBase`` object.
"""

import hashlib
import json
from gzip import decompress
from io import BytesIO
from nibabel.nifti1 import Nifti1Image
from nilearn.image import load_img
from numpy import arange
from numpy.typing import ArrayLike
from os import PathLike
from os.path import dirname
from pandas import read_csv, Series
from pathlib import Path
from typing import (
    Dict, Iterable, List, Optional, Text, Tuple, Union
)
from ..MatchComponents import MatchComponents
from ..constants.BIDSPathConstants import (
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


def GetSidecar(src: Union[Text, PathLike],
               exclude: Optional[Union[Iterable[Text], Text]] = None,
               **kwargs) -> Union[Text, Dict]:
    """
    Returns the associated sidecar of file ``src``, if any.

    """
    kwargs = kwargs if kwargs else {}
    _dst = BIDSRoot(src) if IsEvent(src) else dirname(src)
    keywords = {**{'extension': '.json'}, **kwargs}
    sc_path = filter(IsSidecar,
                     MatchComponents(_dst, src=src, exclude=exclude,
                                     recursive=True, **keywords))
    try:
        return json.loads(Path(next(sc_path)).read_text())
    except (StopIteration, FileNotFoundError, TypeError):
        return ''


def GetFMRI(src: Union[Text, PathLike], **kwargs
            ) -> Union[Text, PathLike]:
    """
    Returns the path of the matching fMRI file.

    Args:
        src: String or PathLike
            Path of a file in a BIDS dataset (any type of file).

        kwargs: Dict
            Keyword arguments to override the default options.
            Any BIDS entity string (short name) is valid.
    """
    src = str(src)
    kwargs = kwargs if kwargs else {}
    keywords = {'bids_suffix': 'bold', 'extension': '.nii.gz'}
    keywords = {**keywords, **kwargs}
    _intent = MatchComponents(dirname(src), src=src, **keywords)
    try:
        return next(filter(IsNifti, _intent))
    except (StopIteration, TypeError):
        return ''


def GetEvents(src: Union[Text, PathLike], **kwargs
              ) -> Union[Text, PathLike, Series]:
    """
    Returns the functional scan's associated "events" file.

    Args:
        src: Text or PathLike
            Path of a nifti scan file (generally fMRI).

        kwargs: Dict
            Keyword arguments to override the default options.
            By default, the returned path will match ``src``
            and the following keywords:
                {'bids_suffix': 'events', 'extension': '.tsv'}.
            Any BIDS entity string (short name) is valid.

    Notes:
        Changing the keyword values of ``bids_suffix`` and/or
        ``extension`` SHOULD cause failure to retrieve
        the behavioural file in a BIDS-valid dataset.
    """
    kwargs = kwargs if kwargs else {}
    _task = find_entity(src, 'task', keep_key=False)
    keywords = dict(bids_suffix='events', extension='.tsv',
                    task=_task)
    keywords = {**keywords, **kwargs}

    try:

        assert all((bool(_task), _task not in {'task-rest', 'rest'}))
        events_path = MatchComponents(dirname(src), src=src, **keywords)
        events_path = next(filter(IsEvent, events_path))
        return read_csv(events_path, sep='\t', **kwargs)
    except NIFTI_ERRORS[:-1]:
        return Series([], dtype='string')


def GetBeh(src: Union[Text, PathLike], **kwargs
           ) -> Union[Text, PathLike]:
    """
    Returns the functional scan's associated "events" file.

    Args:
        src: Text or PathLike
            Path of a nifti scan file (generally fMRI).

        kwargs: Dict
            Keyword arguments to override the default options.
            By default, the returned path will match ``src``
            and the following keywords:
                {'bids_suffix': 'beh', 'extension': '.tsv'}.
            Any BIDS entity string (short name) is valid.

    Notes:
        Changing the keyword values of ``bids_suffix`` and/or
        ``extension`` SHOULD cause failure to retrieve
        the behavioural file in a BIDS-valid dataset.
    """
    kwargs = kwargs if kwargs else {}
    keywords = {'bids_suffix': 'beh', 'extension': '.tsv'}
    keywords = {**keywords, **kwargs}
    beh_path = MatchComponents(dirname(src), src=src, **keywords)
    try:
        return next(filter(IsBeh, beh_path))
    except NIFTI_ERRORS[:-1]:
        return ''


def GetBrainMask(src: Union[Text, PathLike], **kwargs
                 ) -> Union[Text, PathLike]:
    """
    Returns ``src`` corresponding brain mask file path.

    Args:
        src: Text or PathLike
            Path of a nifti scan file (generally fMRI).

        kwargs: Dict
            Keyword arguments to override the default options.
            By default, the returned path will match ``src``
            and the following keywords:
                {'desc': 'desc-brain', 'bids_suffix': 'mask'}.
            Any BIDS entity string (short name) is valid.

    """
    kwargs = kwargs if kwargs else {}
    keywords = {'desc': 'desc-brain', 'bids_suffix': 'mask'}
    keywords = {**keywords, **kwargs}
    mask_path = MatchComponents(SubDir(src), src=src, **keywords)
    try:
        return next(filter(IsNifti, mask_path))
    except NIFTI_ERRORS:
        return ''


def GetAnat(src: Union[Text, PathLike], **kwargs
            ) -> Union[Text, PathLike]:
    """
    Returns the path of the corresponding anatomical scan file.

    First, an attempt to find a matching anatomical scan is
    performed using all available BIDS entities in path ``src``.
    On failure, another attempt is made without the "session"
    identifier, due to its optional nature.

    Args:
        src: Text or PathLike
            Path of a nifti scan file (generally fMRI).

        kwargs: Dict
            Keyword arguments to override the default options.
            By default, the returned path will match ``src``
            and the following keywords:
                {'datatype': 'anat', 'bids_suffix': 'T1w'}.
            Any BIDS entity string (short name) is valid.
    """
    kwargs = kwargs if kwargs else {}
    keywords = {'datatype': 'anat', 'bids_suffix': 'T1w'}
    keywords = {**keywords, **kwargs}
    anat_scan_path = MatchComponents(SubDir(src), src=src,
                                     exclude=['task'],
                                     recursive=True, **keywords)
    try:
        return next(filter(IsNifti, anat_scan_path))
    except StopIteration:
        try:
            keywords.update({'ses': ''})
            anat_scan_path = MatchComponents(SubDir(src), src=src,
                                             exclude=['task'],
                                             recursive=True, **keywords)
            return next(filter(IsNifti, anat_scan_path))
        except NIFTI_ERRORS:
            return ''


def GetMD5CheckSum(src: Union[Text, PathLike],
                   unzip: bool = False) -> Text:
    """
    Returns the MD5 checksum of a file as a hexadecimal string.

    Args:
        src: Text or PathLike
            Path of a file.

        unzip: bool (Default=False)
            Indicates if the bytes stream should be decompressed
            using ``gzip`` or not.

    Returns: Text
        String of double length, containing only hexadecimal digits.
    """
    m, _src = hashlib.md5(), Path(src).read_bytes
    _stream = BytesIO(decompress(_src())) \
        if unzip else BytesIO(_src())
    [m.update(line) for line in _stream.readlines()]
    return m.hexdigest()


def GetSha1Sum(src: Union[Text, PathLike],
               unzip: bool = False) -> Text:
    """
    Returns the sha1 checksum of file ``src`` as a hexadecimal string.

    Args:
        src: str or PathLike
            The path of the file to verify.

        unzip: bool (Default=False)
            If the file should be decompressed
            using gzip or not.

    Returns: str
        Hexadecimal string
    """
    m, _src = hashlib.sha1(), Path(src)
    _buf = BytesIO(_src.read_bytes()) if not unzip else \
        BytesIO(decompress(_src.read_bytes()))
    [m.update(line) for line in _buf.readlines()]
    return m.hexdigest()


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


def GetFrameTimes(img: Nifti1Image) -> ArrayLike:
    """
    Returns scan frame onset times from the repetition time of ``img``.

    """
    try:
        return arange(img.shape[-1]) * GetTR(img)
    except NIFTI_ERRORS:
        return []


__methods__: Tuple = (
    ShapeLength, GetSidecar, GetFMRI, GetEvents, GetBeh,
    GetBrainMask, GetAnat, GetMD5CheckSum, GetSha1Sum,
    GetFrameTimes, GetImgHeader, GetNiftiImage, GetTR

)

__all__: List = [
    "ShapeLength", "GetSidecar", "GetFMRI", "GetEvents", "GetBeh",
    "GetBrainMask", "GetAnat", "GetMD5CheckSum", "GetSha1Sum",
    "GetFrameTimes", "GetImgHeader", "GetNiftiImage", "GetTR",
    "__methods__"
]
