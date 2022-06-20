"""
Class to access a participant's derived json_docs.

"""

import os
from nilearn.interfaces import fmriprep
from typing import Union, Text

from ...constants.fMRIPrepEntities import FMRIPrepEntities
from ...core.BIDSDirAbstract import BIDSDirAbstract

__path__ = [os.path.join('..', '__init__.py')]


class Derivatives(BIDSDirAbstract):
    """
    Class to access a participant's derived json_docs.

    The participant (subject) level is chosen to
    better integrate FMRIPrep derivatives, as the
    pipeline preprocesses raw json_docs at this level.

    Notes:
        Experimental: Class bases are subject to change.
    """
    __slots__ = ('fmriprep', 'fp_entities')

    # def __new__(cls, *args, **kwargs):
    #     kwargs = kwargs if kwargs else {}
    #     kwargs.update({'src': args[0]})
    #     _cls = super().__prepare__(*args)
    #     return type(_cls.__name__, (cls, _cls), kwargs)

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
        attrs = dict(fmriprep=fmriprep, fp_entities=FMRIPrepEntities)
        self.__set_from_dict__(attrs)
