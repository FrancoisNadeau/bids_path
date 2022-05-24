"""
Subject level in a BIDS dataset directory hierarchy.

"""

import os
import warnings
from os import PathLike
from pandas import Series
from typing import Dict, Union

from ...core.BIDSDirAbstract import BIDSDirAbstract
from ...core.bids_dir.Session import Session

__path__ = [os.path.join('..', '__init__.py')]


class Subject(BIDSDirAbstract):
    """
    A person or animal participating in the study.

    References:
        [1] <https://bids-specification.readthedocs.io/en/stable/02-common-principles.html>

    """
    __slots__, __fspath__ = (), BIDSDirAbstract.__fspath__
    def __type__(self): return type(self)

    def __get_entities__(self):
        return super().__get_entities__()

    def __instancecheck__(self, instance) -> bool:
        return all((hasattr(self, 'entities'),
                    self.path.name.startswith('sub-')))

    def __name__(self):
        return self.path.name.replace('-', '')

    @property
    def metadata(self) -> Series:
        """
        Subject metadata read from the 'participants.tsv' file.

        Returns: Series
            Pandas ``Series`` object containing this subject's metadata,
            found in the 'participants.tsv' RECOMMENDED file.

        Notes:
            Corresponds to the participant's respective entry
            from the ``participants_index`` property of ``BIDSPath`` objects.
        """
        try:
            return self.participants_index.loc[self.path.name]
        except KeyError:
            msg = f"Subject {self.path.name} is not listed in participants.tsv."
            warnings.warn(msg)
            return Series(dtype='string')

    @property
    def sessions(self) -> Dict:
        """
        Returns a ``Dict`` of a subject's sessions, if any.

        """
        _ses_dirs = set(self.path.glob('ses-*'))
        return {self.find_ses_id(_s): Session(_s)
                for _s in sorted(_ses_dirs)}

    def __init__(self, src: Union[str, PathLike], **kwargs):
        super().__init__(src, **kwargs)


# def GetSubjectDerivatives(src: Union[str, PathLike],
#                           *args,
#                           ignore: Optional[Iterable] = None) -> Tuple:
#     """
#     Returns a ``namedtuple`` containing a subject's derivatives data.
#
#     Args:
#         src: str or PathLike
#             Path to a subject-level directory in a BIDS dataset.
#         ignore: Iterable (optional)
#             Paths of files and directories to ignore
#             (as defined in '.bidsignore').
#             Automatically retrieved if ``ignore`` is ``None``.
#     """
#
#     def deriv_path(_src: Union[str, PathLike], *_args) -> PathLike:
#         return Path(_src).joinpath(*_args)
#
#     def DGen(_path: Union[str, PathLike]) -> Union[str, PathLike]:
#         try:
#             return _SessionBase(_path) if IsSessionDir(_path) \
#                 else _DatatypeBase(_path)
#         except FileNotFoundError:
#             return ''
#
#     def DerivativesPathsGen(_paths: Iterable[PathLike]) -> Generator:
#         return ((basename(dirname(p)), DGen(p)) for p in _paths)
#
#     _ignore = set(ignore) if ignore \
#         else set(args) if args else FetchBidsignore(src)
#     _deriv_names = GetDerivativesNames(src, _ignore)
#     Derivatives = namedtuple('Derivatives', field_names=_deriv_names)
#     dpaths = set(deriv_path(DerivativesRoot(src), *(_name, basename(src)))
#                  for _name in _deriv_names).difference(_ignore)
#     return Derivatives(**dict(DerivativesPathsGen(dpaths)))
