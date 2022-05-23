
from nibabel import Nifti1Image
from numpy.typing import ArrayLike
from os import PathLike
from typing import Text, Optional, Any, Union, Dict

from ...general_methods import docstring_parameter
from ...core.BIDSFileAbstract import BIDSFileAbstract
from ...functions.BIDSFileFunctions import (
    GetNiftiImage, GetImgHeader, GetTR, GetFrameTimes
)



class MRIFile(BIDSFileAbstract):
    """
    Class for 3D MRI image files.

    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      self.is_3d_file(instance))
        return all(conditions)

    def _fget(self, key: Text, default: Optional[Any] = None) -> Any:
        return object.__getattribute__(self, 'sidecar').get(key, default)

    def _fset(self, key: Text, default: Optional[Any] = None) -> Any:
        return object.__setattr__(self, key, self._fget(key, default))

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)

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
