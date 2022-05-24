
import json
import os
from io import BytesIO
from nibabel.nifti1 import Nifti1Image
from os import PathLike
from os.path import dirname, isfile
from pathlib import Path
from typing import Dict, Iterable, Optional, Text, Union

from ..general_methods import docstring_parameter, sizeof_fmt, GetMD5CheckSum, GetSha1Sum
from ..BIDSPathConstants import ENTITY_STRINGS
from ..core.BIDSPathAbstract import BIDSPathAbstract
from ..functions.BIDSFileFunctions import ShapeLength
from ..functions.BIDSFileID import IsEvent, IsNifti, IsSidecar
from ..functions.BIDSPathFunctions import BIDSRoot, SubDir
from ..functions.MatchComponents import MatchComponents

__path__ = [os.path.join('..', '__init__.py')]


class BIDSFileAbstract(BIDSPathAbstract):
    """
    Abstract base class for ``BIDSFile`` objects.

    Implements static methods to compute attributes.
    Determines which of its subclasses should be instantiated.
    Prepares the namespace for its children classes.
    Can be updated and extended via the
    ``core.BIDSFileFunctions.py`` file and importing
    the modifications as static or class methods.

    """
    __slots__ = ENTITY_STRINGS
    __fspath__ = BIDSPathAbstract.__fspath__
    def __type__(self): return type(self)

    def __get_entities__(self):
        return super().__get_entities__()

    def __subclasscheck__(self, subclass) -> bool:
        conditions = (hasattr(self, 'entities'),
                      isfile(str(self.path)))
        return all(conditions)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      isfile(str(instance.path)))
        return all(conditions)

    @classmethod
    def __prepare__(cls, /, src: Union[Text, PathLike], **kwargs):
        subclass_dict = BIDSFileAbstract.subclass_dict()
        if not isfile(str(src)):
            return src
        _mapper = (
            (super().is_3d_file(src), 'MRIFile'),
            (super().is_4d_file(src), 'FMRIFile'),
            (super().is_event_file(src), 'EventsFile'),
            (super().is_beh_file(src), 'BehFile'),
            (super().is_physio_file(src), 'PhysioFile'),
            (super().is_sidecar_file(src), 'SideCarFile')
        )
        _cls = next(filter(lambda item: bool(item[0]), _mapper))
        keywords = dict(zip(cls.__slots__,
                            super().__get_entities__(src)))
        subclass = subclass_dict[_cls[1]](src)
        subclass.__set_from_dict__(keywords)
        return subclass

    @property
    def buf(self) -> BytesIO:
        """
        BytesIO buffer contaning the file's raw bytes.

        Returns: BytesIO
        """
        return BytesIO(self.path.read_bytes())

    @property
    @docstring_parameter(sizeof_fmt.__doc__)
    def sizeof_fmt(self) -> Text:
        """{0}\n"""
        return sizeof_fmt(self.stat.st_size)

    # General
    @staticmethod
    def get_sidecar(src: Union[Text, PathLike],
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

    @staticmethod
    @docstring_parameter(GetMD5CheckSum.__doc__)
    def get_md5_checksum(src: Union[Text, PathLike],
                         unzip: bool = False) -> Text:
        """{0}\n"""
        return GetMD5CheckSum(src, unzip=unzip)

    @staticmethod
    @docstring_parameter(GetSha1Sum.__doc__)
    def get_sha1_checksum(src: Union[Text, PathLike],
                          unzip: bool = False) -> Text:
        """{0}\n"""
        return GetSha1Sum(src, unzip=unzip)

    # @staticmethod
    # @docstring_parameter(GetFMRI.__doc__)
    # def get_fmri_img(src: Union[Text, PathLike], **kwargs
    #                  ) -> PathLike:
    #     """{0}\n"""
    #     return GetFMRI(src, **kwargs)

    def md5_checksum(self, unzip: bool = False) -> Text:
        """
        Returns the MD5 checksum of this file as a hexadecimal string.

        Args:
            unzip: bool (Default=False)
                Indicates if the bytes stream should be
                decompressed using ``gzip`` or not.

        """
        return GetMD5CheckSum(str(self), unzip=unzip)

    @docstring_parameter(GetSha1Sum.__doc__)
    def sha1_checksum(self, unzip: bool = False) -> Text:
        """{0}\n"""
        return GetSha1Sum(str(self), unzip=unzip)

    # Nifti (fMRI)
    @staticmethod
    def get_anat_img(src: Union[Text, PathLike], **kwargs
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
            except StopIteration:
                return ''

    @staticmethod
    def get_brain_mask(src: Union[Text, PathLike], **kwargs
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
        except StopIteration:
            return ''

    @property
    def func_img(self) -> Union[Text, os.PathLike]:
        """
        Returns the path of the matching fMRI file.

        """
        keywords = {'bids_suffix': 'bold', 'extension': '.nii.gz'}
        _intent = MatchComponents(self.path.parent, src=self.path, **keywords)
        try:
            return next(filter(IsNifti, _intent))
        except (StopIteration, TypeError):
            return ''

    def view_sidecar(self, indent: int = 2, **kwargs):
        """
        Prints contents of the sidecar to stdout.

        Args:
            indent: int
                Desired indentation level.
                Passed to ``json.dumps`` method.
        """
        viewer = json.dumps(self.sidecar,
                            indent=indent, **kwargs)
        print(viewer)

    # Read-only properties
    @property
    def sidecar(self) -> Union[Text, PathLike, Dict]:
        """
        Returns the file's associated ".json" sidecar.

        """
        return self.get_sidecar(self.path)

    @staticmethod
    @docstring_parameter(ShapeLength.__doc__)
    def get_n_dims(src: Union[Text, PathLike, Nifti1Image]
                   ) -> int:
        """{0}\n"""
        return ShapeLength(src)
