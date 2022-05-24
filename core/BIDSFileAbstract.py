
import json
import os
import sys
from io import BufferedIOBase, BytesIO
from nibabel.nifti1 import Nifti1Image
from os import PathLike
from os.path import isfile
from typing import Dict, Text, Union

from ..general_methods import docstring_parameter
from ..constants.BIDSPathConstants import ENTITY_STRINGS
from ..core.BIDSPathAbstract import BIDSPathAbstract
from ..functions.BIDSFileFunctions import (
    GetAnat, GetBeh, GetBrainMask, GetEvents,
    GetMD5CheckSum, GetSidecar, ShapeLength, GetSha1Sum
)

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
        _mapper = (
            (super().is_3d_file(src), 'MRIFile'),
            (super().is_4d_file(src), 'FMRIFile'),
            (super().is_event_file(src), 'EventsFile'),
            (super().is_beh_file(src), 'BehFile'),
            (super().is_physio_file(src), 'PhysioFile'),
            (super().is_sidecar_file(src), 'SideCarFile')
        )
        _cls = next(filter(lambda item: bool(item[0]), _mapper))
        keywords = super().__get_entities__(src)._asdict()
        subclass = subclass_dict[_cls[1]](src)
        subclass.__set_from_dict__(keywords)
        return subclass

    @property
    def buf(self) -> BufferedIOBase:
        with open(self, mode='rb') as stream:
            return BytesIO(stream.read(self.stat.st_size))

    # General
    @staticmethod
    @docstring_parameter(GetSidecar.__doc__)
    def get_sidecar(src: Union[Text, PathLike], **kwargs
                    ) -> Union[Text, PathLike]:
        """{0}\n"""
        return GetSidecar(src, **kwargs)

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
    @docstring_parameter(GetAnat.__doc__)
    def get_anat_img(src: Union[Text, PathLike], **kwargs
                     ) -> Union[Text, PathLike]:
        """{0}\n"""
        return GetAnat(src, **kwargs)

    @staticmethod
    @docstring_parameter(GetBeh.__doc__)
    def get_beh_file(src: Union[Text, PathLike], **kwargs
                     ) -> Union[Text, PathLike]:
        """{0}\n"""
        return GetBeh(src, **kwargs)

    @staticmethod
    @docstring_parameter(GetBrainMask.__doc__)
    def get_brain_mask(src: Union[Text, PathLike], **kwargs
                       ) -> Union[Text, PathLike]:
        """{0}\n"""
        return GetBrainMask(src, **kwargs)

    @staticmethod
    @docstring_parameter(GetEvents.__doc__)
    def get_events_file(src: Union[Text, PathLike], **kwargs
                        ) -> Union[Text, PathLike]:
        """{0}\n"""
        return GetEvents(src, **kwargs)

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
    @docstring_parameter(GetSidecar.__doc__)
    def sidecar(self) -> Union[Text, PathLike, Dict]:
        """{0}\n"""
        return self.get_sidecar(self.path)

    @staticmethod
    @docstring_parameter(ShapeLength.__doc__)
    def get_n_dims(src: Union[Text, PathLike, Nifti1Image]
                   ) -> int:
        """{0}\n"""
        return ShapeLength(src)
