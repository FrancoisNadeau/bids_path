
import json
import os
from io import BufferedIOBase, BytesIO
from nibabel.nifti1 import Nifti1Image
from os import PathLike
from os.path import isfile
from pathlib import Path
from typing import Dict, Text, Union

from ..general_methods import docstring_parameter, GetHashCheckSum
from ..constants.bidspathlib_docs import ENTITY_STRINGS
from ..core.BIDSPathAbstract import BIDSPathAbstract
from ..functions.BIDSFileFunctions import ShapeLength
from ..MatchComponents import MatchComponents

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
    def __type__(self): return type(self)

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
        try:
            _mapper = (
                (super().is_3d_file(src), 'MRIFile'),
                (super().is_4d_file(src), 'FMRIFile'),
                (super().is_event_file(src), 'EventsFile'),
                (super().is_beh_file(src), 'BehFile'),
                (super().is_physio_file(src), 'PhysioFile'),
                (super().is_sidecar_file(src), 'SideCarFile'),
                (Path(src).name == 'CHANGES', 'ChangesFile'),
                (Path(src).name == 'README', 'ReadMeFile'),
                (Path(src).name == 'LICENSE', 'LicenseFile'),
                (Path(src).name == '.gitattributes', 'GitAttributesFile')
            )
            _cls = next(filter(lambda item: bool(item[0]), _mapper))
            keywords = dict(zip(ENTITY_STRINGS,
                                super().__get_entities__(src)))
            subclass = subclass_dict[_cls[1]](src)
            subclass.__set_from_dict__(keywords)
            return subclass
        except StopIteration:
            print(src)

    @property
    def buf(self) -> BufferedIOBase:
        with open(self, mode='rb') as stream:
            return BytesIO(stream.read(self.stat.st_size))

    # General
    @staticmethod
    def get_sidecar(src: Union[Text, PathLike], **kwargs
                    ) -> Union[Text, PathLike]:
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
            with open(next(sc_path), mode='r') as jfile:
                sidecar = json.load(jfile)
                jfile.close()
                return sidecar
        except (StopIteration, FileNotFoundError, TypeError):
            return ''

    @staticmethod
    @docstring_parameter(GetHashCheckSum.__doc__)
    def get_hash_checksum(src: Union[Text, PathLike],
                         algo: Text = 'sha256',
                         unzip: bool = False) -> Text:
        """{0}\n"""
        return GetHashCheckSum(src, algo=algo, unzip=unzip)

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
            except NIFTI_ERRORS:
                return ''

    @staticmethod
    def get_beh_file(src: Union[Text, PathLike], **kwargs
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
        except NIFTI_ERRORS:
            return ''

    @staticmethod
    def get_events_file(src: Union[Text, PathLike], **kwargs
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
                    {'bids_suffix': 'events', 'extension': '.tsv'}.
                Any BIDS entity string (short name) is valid.

        Notes:
            Changing the keyword values of ``bids_suffix`` and/or
            ``extension`` SHOULD cause failure to retrieve
            the behavioural file in a BIDS-valid dataset.
        """
        kwargs = kwargs if kwargs else {}
        _task = find_entity(src, 'task', keep_key=False)
        keywords = dict(bids_suffix='events', extension='.tsv', task=_task)
        keywords = {**keywords, **kwargs}

        try:
            assert all((bool(_task), _task not in {'task-rest', 'rest'}))
            events_path = MatchComponents(dirname(src), src=src, **keywords)
            events_path = next(filter(IsEvent, events_path))
            return read_csv(events_path, sep='\t', **kwargs)
        except NIFTI_ERRORS[:-1]:
            return Series([], dtype='string')

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
        """{0}\n"""
        return self.get_sidecar(self.path)

    @staticmethod
    @docstring_parameter(ShapeLength.__doc__)
    def get_n_dims(src: Union[Text, PathLike, Nifti1Image]
                   ) -> int:
        """{0}\n"""
        return ShapeLength(src)
