
from nibabel.nifti1 import Nifti1Image
from numpy.typing import ArrayLike
from os import PathLike
from typing import Dict, Union, Text, Tuple

from ...general_methods import docstring_parameter
from ...functions.BIDSFileFunctions import GetEvents
from ...constants.BIDSPathConstants import (
    BidsRecommended, BIDS_RECOMMENDED
)
from ..BIDSFileAbstract import BIDSFileAbstract
from ...functions.BIDSFileFunctions import (
    GetNiftiImage, GetImgHeader, GetTR, GetFrameTimes
)


class FMRIFile(BIDSFileAbstract):
    """
    Class for 4D MRI image files.

    """
    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      self.is_4d_file(instance))
        return all(conditions)

    __slots__ = ()

    def __type__(self): return type(self)

    def __init__(self, src: Union[Text, PathLike], *args, **kwargs):
        super().__init__(src, *args, **kwargs)

    @staticmethod
    @docstring_parameter(GetEvents.__doc__)
    def get_events_file(src: Union[Text, PathLike], **kwargs
                        ) -> Union[Text, PathLike]:
        """{0}\n"""
        return GetEvents(src, **kwargs)

    @staticmethod
    @docstring_parameter(GetNiftiImage.__doc__)
    def get_img(src: Union[Text, PathLike]) -> Nifti1Image:
        """{0}\n"""
        return GetNiftiImage(src)

    @staticmethod
    @docstring_parameter(GetImgHeader.__doc__)
    def get_img_header(img: Nifti1Image) -> Dict:
        """{0}\n"""
        return GetImgHeader(img)

    @staticmethod
    @docstring_parameter(GetFrameTimes.__doc__)
    def get_frame_times(img: Nifti1Image) -> ArrayLike:
        """{0}\n"""
        return GetFrameTimes(img)

    @staticmethod
    @docstring_parameter(GetTR.__doc__)
    def get_tr(img: Nifti1Image) -> float:
        """{0}\n"""
        return GetTR(img)

    @property
    @docstring_parameter(*(GetNiftiImage.__doc__,
                           Nifti1Image.__doc__))
    def img(self) -> Union[Text, Nifti1Image]:
        """{0}\n{1}\n"""
        return GetNiftiImage(self.path)

    @property
    @docstring_parameter(GetImgHeader.__doc__)
    def img_header(self) -> Dict:
        """{0}\n"""
        return GetImgHeader(self.img)

    @property
    @docstring_parameter(GetFrameTimes.__doc__)
    def frame_times(self) -> ArrayLike:
        """{0}\n"""
        return GetFrameTimes(self.img)

    @property
    @docstring_parameter(GetTR.__doc__)
    def t_r(self) -> float:
        """{0}\n"""
        return GetTR(self.img)

    @property
    @docstring_parameter(BIDSFileAbstract.get_anat_img.__doc__)
    def anat_img(self, **kwargs) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.get_anat_img(self.path, **kwargs)

    @property
    @docstring_parameter(BIDSFileAbstract.get_beh_file.__doc__)
    def beh_file(self, **kwargs) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.get_beh_file(self.path, **kwargs)

    @property
    @docstring_parameter(BIDSFileAbstract.get_brain_mask.__doc__)
    def brain_mask_img(self, **kwargs) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.get_brain_mask(self.path, **kwargs)

    @property
    @docstring_parameter(BIDSFileAbstract.get_events_file.__doc__)
    def events_file(self, **kwargs) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.get_events_file(self.path, **kwargs)

    @property
    def hardware_info(self) -> Tuple:
        return BidsRecommended(**{field: self.sidecar.get(field, '')
                                  for field in BIDS_RECOMMENDED})
