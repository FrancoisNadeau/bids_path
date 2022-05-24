"""
Class for 4D MRI image files.

"""

import os
from nibabel.nifti1 import Nifti1Image
from nilearn._utils.niimg_conversions import check_niimg
from numpy.typing import ArrayLike
from os import PathLike
from typing import Dict, Union, Text, Tuple

from ...general_methods import docstring_parameter
from ...BIDSPathConstants import BidsRecommended, BIDS_RECOMMENDED
from ..BIDSFileAbstract import BIDSFileAbstract
from ...functions.BIDSFileFunctions import (
    GetImgHeader, GetTR, GetFrameTimes
)
from ...functions.BIDSFileID import IsBeh, IsEvent
from ...functions.MatchComponents import MatchComponents

__path__ = [os.path.join('..', '__init__.py')]


class FMRIFile(BIDSFileAbstract):
    """
    Class for 4D MRI image files.

    This should only be instantiated on the path of a 4D nifti image file.
    Otherwise, ``Not4DError`` is raised.

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

        return check_niimg(self.path.__fspath__(), ensure_ndim=4)

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
    def events_file(self) -> Union[Text, PathLike]:
        """
        Returns the functional scan's associated "events" file.

        """
        try:
            keywords = dict(bids_suffix='events', extension='.tsv')
            assert all((bool(self.task), self.task not in {'task-rest', 'rest'}))
            events_path = MatchComponents(dst=self.path.parent, src=self.path, **keywords)
            return self.subclass_dict()['EventsFile'](next(filter(IsEvent, events_path)))
        except StopIteration:
            return ''

    @property
    def beh_file(self) -> Union[Text, PathLike]:
        """
        Returns the functional scan's associated "events" file.

        """
        keywords = {'bids_suffix': 'beh', 'extension': '.tsv'}
        beh_path = MatchComponents(dst=self.path.parent, src=self.path, **keywords)
        try:
            return self.subclass_dict()['BehFile'](next(filter(IsBeh, beh_path)))
        except StopIteration:
            return ''

    @property
    @docstring_parameter(BIDSFileAbstract.get_brain_mask.__doc__)
    def brain_mask_img(self, **kwargs) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.get_brain_mask(self.path, **kwargs)

    @property
    def hardware_info(self) -> Tuple:
        return BidsRecommended(**{field: self.sidecar.get(field, '')
                                  for field in BIDS_RECOMMENDED})
