"""
Class for 3D MRI image files.

"""

import os
from nibabel import Nifti1Image
from nilearn._utils.niimg_conversions import check_niimg
from numpy.typing import ArrayLike
from typing import Text, Optional, Any, Union, Dict

from ...general_methods import docstring_parameter
from ...core.BIDSFileAbstract import BIDSFileAbstract
from ...functions.BIDSFileFunctions import (
    GetImgHeader, GetTR, GetFrameTimes
)
from ...functions.BIDSFileID import Is3D
from ...bidspathlib_exceptions import Not3DError

__path__ = [os.path.join('..', '__init__.py')]


class MRIFile(BIDSFileAbstract):
    """
    Class for 3D MRI image files.

    This should only be instantiated on the path of a 4D nifti image file.
    Otherwise, ``Not4DError`` is raised.
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

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)

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
    def img(self) -> Union[Text, Nifti1Image]:
        """
        Returns the corresponding nifti file's image.

        """
        return check_niimg(self.path.__fspath__(), ensure_ndim=3)

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
