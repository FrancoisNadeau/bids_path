
import os
import pandas as pd
import pickle
import sys
from abc import ABC
from bids_validator import BIDSValidator
from collections import UserString
from os import PathLike, stat_result
from os.path import isdir, isfile, samefile
from pathlib import Path
from typing import (
    Any, Dict, Generator, Iterable, List, NamedTuple,
    Optional, Text, Tuple, Union
)

from ..general_methods import docstring_parameter, SetFromDict
from ..BIDSPathLike import BIDSPathLike
from ..MatchComponents import MatchComponents
from ..constants import Modality
from ..functions.BIDSFileID import (
    IsNifti, Is4D, Is3D, IsEvent, IsBeh, IsPhysio, IsSidecar
)
from ..functions.BIDSDirID import (
    IsBIDSRoot, IsDatasetRoot, IsSubjectDir, IsSessionDir, IsDatatypeDir,
    IsDerivatives, IsDerivativesRoot, IsFMRIPrepDerivatives
)
from ..functions.BIDSPathCoreFunctions import (
    find_datatype, find_entity, find_extension, find_bids_suffix
)
from ..functions.BIDSPathFunctions import (
    DatasetName, GetBidsignore, FormattedCtime,
    GetComponents, GetEntities, GetEntityStrings,
    DatasetDescription, DatatypeModality, BIDSRoot,
    DatasetRoot, DerivativesRoot, GetDerivativesNames,
    SesDir, SubDir, RelativeToRoot, Validate
)


class BIDSPathAbstract(*(str, BIDSPathLike, ABC)):
    """
    Abstract class emulating a ``pathlib.Path`` object.

    Concretely, class ``BIDSPathAbstract`` is a
    ``collections.UserString`` object with methods and properties
    from both its parent class and those
    of a ``pathlib.Path`` object.

    To increase stability, properties and zero-argument
    instance methods from ``pathlib.Path`` are all read-only
    (and thus not callable) data descriptors.
    Other instance and classmethods inherited from
    ``collections.UserString`` and ``pathlib.Path``
    are called normally.

    This ABC also implements the core and higher-leveldata
    bids_path_functions of module``BIDSPath`` (respectively found in
    ``core.BIDSPathCoreFunctions`` and ``core.BIDSPathFunctions``).

    Notes:
        Concrete subclasses must override
        ``__new__`` or ``__init__``,
        ``__getitem__``, ``__len__``,
        ``__fspath__`` and ``__get_entities__``.
    """
    __slots__ = ()
    def __type__(self): return type(self)

    __int__, __float__, __complex__ = [NotImplemented]*3
    __delattr__, __rmod__ = [NotImplemented]*2
    __reversed__, __getnewargs__, __weakref__ = [NotImplemented]*3
    __dict__ = NotImplemented

    # Mandatory abstract methods
    @docstring_parameter(os.fspath.__doc__)
    def __fspath__(self) -> Text:
        """{0}\n"""
        return ''.join(self._chars)

    @docstring_parameter(GetEntityStrings.__doc__)
    def __get_entities__(self) -> NamedTuple:
        """{0}\n"""
        return GetEntityStrings(self)

    @classmethod
    def __subclasshook__(cls, subclass: Any):
        conditions = (hasattr(subclass, '__fspath__'),
                      hasattr(subclass, '__get_entities__'))
        return True if all(conditions) \
            else NotImplemented

    def __subclasscheck__(self, subclass: Any) -> bool:
        candidates = (str, PathLike, UserString)
        return any(c in candidates for c in subclass.mro())

    def __instancecheck__(self, instance: Any) -> bool:
        return any(map(self.__subclasscheck__, instance.__mro__))

    @classmethod
    @docstring_parameter(SetFromDict.__doc__)
    def __set_from_dict__(cls, attrs: Dict,
                          keys: Optional[Iterable] = None,
                          default: Optional[Any] = None,
                          **kwargs) -> None:
        """{0}"""
        SetFromDict(cls, attrs, keys, default, **kwargs)


    @property
    def participants_index(self) -> pd.DataFrame:
        """
        Returns the contents of RECOMMENDED file "participants.tsv" as a DataFrame.

        References:
            <https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file>
        """
        meta_path = os.path.join(selfset_root, 'participants.tsv')
        print(f"Path {meta_path} exists: {os.path.exists(meta_path)}")
        if os.path.exists(meta_path):
            return pd.read_csv(str(meta_path), sep='\t',
                               index_col='participant_id')
        else:
            return pd.DataFrame(dtype='string')

    @property
    @docstring_parameter(GetBidsignore.__doc__)
    def bidsignore(self) -> Generator:
        """{0}\n"""
        yield from GetBidsignore(self.path)
    
    @property
    def _chars(self) -> List:
        return list(self)
    
    @property
    def _default_encoding(self) -> Text:
        return sys.getdefaultencoding()

    def __repr__(self) -> Text:
        """
        Returns repr(self).

        """
        _name = type(self).__name__
        os_path_type = type(self.path).__name__
        return f"{_name}({os_path_type}({self.__str__()}))"

    # Dunder methods inherited from ``pathlib.Path``
    def __reduce__(self) -> Tuple:
        """
        Helper for pickle.

        """
        return self.path.__reduce__()

    def __reduce_ex__(self, protocol: int = pickle.HIGHEST_PROTOCOL
                      ) -> Tuple:
        """
        Extended helper for pickle.

        """
        return self.path.__reduce_ex__(protocol)

    def __bytes__(self) -> bytes:
        """
        Returns the byte representation of the path.

        Notes:
            Only recommended to use under Unix.
        """
        return b''.join(map(lambda c: c.encode(sys.getdefaultencoding()), self))

    def __hash__(self) -> int:
        return self.path.__hash__()

    def __enter__(self): self.path.__enter__()

    def __exit__(self, exc_type: Any,
                 exc_val: Any, exc_tb: Any):
        self.path.__exit__(exc_type, exc_val, exc_tb)

    def __truediv__(self, other: Any):
        return self.path.__truediv__(other)

    def __rtruediv__(self, other: Any):
        return self.path.__rtruediv__(other)

    @docstring_parameter(getattr.__doc__)
    def __getitem__(self, item: Union[int, slice, Text]) -> Any:
        """
        {0}\n
        If ``item`` is an integer or a slice, returns the
        characters in the path's string with the same index.
        """
        if item in self.__slots__ or hasattr(self, item):
            return object.__getattribute__(self, item)
        elif isinstance(item, (int, slice)):
            if item < 0 or item >= len(self):
                raise IndexError(item)
            return self[item]
        else:
            raise AttributeError

    def __call__(self, /, *args, **kwargs):
        return object.__call__(*args, **kwargs)

    @property
    @docstring_parameter(Path.__doc__)
    def path(self):
        """
        Main property of ``BIDSPath`` objects.

        {0}\n"""
        return Path(self)

    # Pathlib and os bids_path_functions as static methods
    @staticmethod
    def isdir(src: Union[Text, PathLike]) -> bool:
        """
        Returns True if ``src`` refers to an existing directory.

        """
        return isdir(src)

    @staticmethod
    def isfile(src: Union[Text, PathLike]) -> bool:
        """
        Returns True if a path is a regular file.

        """
        return isfile(src)

    @staticmethod
    def isreserved(src: Union[Text, PathLike]) -> bool:
        """
        Returns True if the path contains any system-reserved special names.

        """
        return Path(src).is_reserved()

    @staticmethod
    def get_parent(src: Union[Text, PathLike]) -> PathLike:
        """
        Returns the logical parent of path ``src``.

        """
        return Path(src).parent

    @staticmethod
    def get_parents(src: Union[Text, PathLike]) -> Generator:
        """
        Yields from iterating over this path's logical parents.

        """
        yield from Path(src).parents

    @staticmethod
    def get_drive(src: PathLike) -> Text:
        """
        Returns the drive prefix (letter or UNC path), if any.

        """
        return Path(src).drive

    @staticmethod
    def get_root(src: Union[Text, PathLike]) -> Text:
        """
        Returns the root of path ``src``, if any.

        """
        return Path(src).root

    @staticmethod
    @docstring_parameter(samefile.__doc__)
    def is_samefile(src: Union[Text, PathLike],
                    other_path: Union[Text, PathLike]
                    ) -> bool:
        """{0}\n"""
        return samefile(str(src), str(other_path))

    @staticmethod
    @docstring_parameter(Path.match.__doc__)
    def is_match(src: Union[Text, PathLike],
                 path_pattern: Text) -> bool:
        """{0}\n"""
        return Path(src).match(path_pattern)

    @staticmethod
    @docstring_parameter(Path.relative_to.__doc__)
    def make_relative_to(src: Union[Text, PathLike],
                         *other
                         ) -> PathLike:
        """{0}\n"""
        return Path(str(src)).relative_to(*other)

    @staticmethod
    @docstring_parameter(Path.cwd.__doc__)
    def cwd():
        """{0}\n"""
        return Path.cwd()

    # Pathlib instance methods
    @docstring_parameter(Path.match.__doc__)
    def match(self, path_pattern: Text) -> bool:
        """{0}\n"""
        return self.path.match(path_pattern)

    @docstring_parameter(Path.relative_to.__doc__)
    def relative_to(self, *other) -> PathLike:
        """{0}\n"""
        return self.path.relative_to(*other)

    @docstring_parameter(Path.chmod.__doc__)
    def chmod(self, mode: int):
        """{0}\n"""
        self.path.chmod(mode)

    @docstring_parameter(Path.lchmod.__doc__)
    def lchmod(self, mode: int):
        """{0}\n"""
        self.path.lchmod(mode)

    @docstring_parameter(Path.link_to.__doc__)
    def link_to(self, target: Union[Text, PathLike]):
        """{0}\n"""
        self.path.link_to(target)

    @docstring_parameter(Path.symlink_to.__doc__)
    def symlink_to(self,
                   target: Union[Text, PathLike],
                   target_is_directory: bool = False):
        """{0}\n"""
        self.path.symlink_to(target, target_is_directory)

    @docstring_parameter(samefile.__doc__)
    def samefile(self, other_path: Union[Text, PathLike]) -> bool:
        """{0}\n"""
        return samefile(self, str(other_path))

    @docstring_parameter(Path.mkdir.__doc__)
    def mkdir(self, mode: int = 511,
              parents: bool = False,
              exist_ok: bool = False):
        """{0}\n"""
        self.path.mkdir(mode=mode, parents=parents,
                        exist_ok=exist_ok)

    @docstring_parameter(Path.rename.__doc__)
    def rename(self, target: Union[Text, PathLike]):
        """{0}\n"""
        self.path.rename(target)

    @docstring_parameter(open.__doc__)
    def open(self,  mode: Text = 'r', buffering: int = -1,
             encoding: Optional[Text] = None,
             errors: Optional[Text] = None,
             newline: Optional[Text] = None):
        """{0}\n"""
        self.path.open(mode=mode, buffering=buffering,
                       encoding=encoding, errors=errors,
                       newline=newline)

    @docstring_parameter(Path.rmdir.__doc__)
    def rmdir(self):
        """{0}\n"""
        self.path.rmdir()

    @docstring_parameter(Path.read_bytes.__doc__)
    def read_bytes(self) -> bytes:
        """{0}\n"""
        return self.path.read_bytes()

    @docstring_parameter(Path.write_bytes.__doc__)
    def write_bytes(self, data: bytes):
        """{0}\n"""
        self.path.write_bytes(data)

    @docstring_parameter(Path.read_text.__doc__)
    def read_text(self, encoding: Optional[Text] = None,
                  errors: Optional[Text] = None) -> Text:
        """{0}\n"""
        return self.path.read_text(encoding=encoding,
                                   errors=errors)

    @docstring_parameter(Path.write_text.__doc__)
    def write_text(self, data: Text,
                   encoding: Optional[Text] = None,
                   errors: Optional[Text] = None):
        """{0}\n"""
        self.path.write_text(data, encoding=encoding,
                             errors=errors)

    @docstring_parameter(Path.unlink.__doc__)
    def unlink(self, missing_ok: bool = False):
        """{0}\n"""
        self.path.unlink(missing_ok=missing_ok)

    @docstring_parameter(Path.mkdir.__doc__)
    def mkdir(self, mode: int = 511,
              parents: bool = False,
              exist_ok: bool = False):
        """{0}\n"""
        self.path.mkdir(mode=mode, parents=parents,
                        exist_ok=exist_ok)

    @docstring_parameter(Path.joinpath.__doc__)
    def joinpath(self, *args):
        """{0}\n"""
        return self.joinpath(*args)

    @docstring_parameter(Path.touch.__doc__)
    def touch(self, mode: int = 438, exist_ok: bool = True):
        """{0}\n"""
        self.path.touch(mode, exist_ok)

    @docstring_parameter(Path.with_name.__doc__)
    def with_name(self, name: Text) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.with_name(name)

    @docstring_parameter(Path.with_suffix.__doc__)
    def with_suffix(self, suffix: Text) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.with_suffix(suffix)

    # Core bids_path_functions
    @classmethod
    def subclass_dict(cls) -> Dict:
        """
        Returns a dictionary mapping subclass names to namespaces.

        """
        return {c.__name__: c for c in
                cls.__subclasses__()}

    @classmethod
    @docstring_parameter(SetFromDict.__doc__)
    def __set_from_dict__(cls, attrs: Dict,
                          keys: Optional[Iterable] = None,
                          default: Optional[Any] = None,
                          **kwargs) -> None:
        """{0}"""
        SetFromDict(cls, attrs, keys, default, **kwargs)

    @staticmethod
    @docstring_parameter(find_entity.__doc__)
    def find_entity(src: Union[Text, PathLike],
                    entity: Text,
                    keep_key: bool = True) -> Text:
        """{0}\n"""
        return find_entity(src, entity, keep_key)

    @staticmethod
    @docstring_parameter(find_bids_suffix.__doc__)
    def find_bids_suffix(src: Union[Text, PathLike]) -> Text:
        """{0}\n"""
        return find_bids_suffix(src)

    @staticmethod
    @docstring_parameter(find_extension.__doc__)
    def find_extension(src: Union[Text, PathLike]) -> Text:
        """{0}\n"""
        return find_extension(src)

    @staticmethod
    @docstring_parameter(find_datatype.__doc__)
    def find_datatype(src: Union[Text, PathLike]) -> Text:
        """{0}\n"""
        return find_datatype(src)

    # Core bids_path_functions extended
    @staticmethod
    def find_ses_id(src: Union[Text, PathLike]) -> Text:
        """
        Returns a session's BIDS identifier (``ses-`` prefix included).

        Same output as ```self.ses``` on an
        instantiated ``BIDSPath`` object.
        """
        return find_entity(src, 'ses')

    @staticmethod
    def find_sub_id(src: Union[Text, PathLike]) -> Text:
        """
        Returns a subject's BIDS identifier (``sub-`` prefix included).

        Same output as ```self.sub``` on an
        instantiated ``BIDSPath`` object.
        """
        return find_entity(src, 'sub')

    @staticmethod
    @docstring_parameter(FormattedCtime.__doc__)
    def formatted_ctime(src: Union[Text, PathLike],
                        time_fmt: Text = "%d %m %Y, %H:%M"
                        ) -> Text:
        """{0}\n"""
        return FormattedCtime(src, time_fmt)

    @staticmethod
    @docstring_parameter(GetEntities.__doc__)
    def get_entities(src: Union[Text, PathLike]) -> Tuple:
        """{0}\n"""
        return GetEntities(src)

    @staticmethod
    @docstring_parameter(GetEntityStrings.__doc__)
    def get_entity_strings(src: Union[Text, PathLike]
                           ) -> Tuple:
        """{0}\n"""
        return GetEntityStrings(src)

    @staticmethod
    @docstring_parameter(GetComponents.__doc__)
    def get_components(src: Union[Text, PathLike]) -> Tuple:
        """{0}\n"""
        return GetComponents(src)

    @staticmethod
    @docstring_parameter(GetBidsignore.__doc__)
    def fetch_bidsignore(src: Union[Text, PathLike]
                         ) -> Generator:
        """{0}\n"""
        return GetBidsignore(src)

    @staticmethod
    @docstring_parameter(DatasetName.__doc__)
    def get_dataset_name(src: Union[Text, PathLike]):
        """{0}\n"""
        return DatasetName(src)

    @staticmethod
    @docstring_parameter(DatasetDescription.__doc__)
    def get_dataset_description(src: Union[Text, PathLike]
                                ) -> Dict:
        """{0}\n"""
        return DatasetDescription(src)

    @staticmethod
    @docstring_parameter(DatatypeModality.__doc__)
    def get_datatype_modality(src: Union[Text, PathLike]
                              ) -> Union[Text, Modality]:
        """{0}\n"""
        return DatatypeModality(src)

    @staticmethod
    @docstring_parameter(RelativeToRoot.__doc__)
    def relative_to_root(src: Union[Text, PathLike]
                         ) -> PathLike:
        """{0}\n"""
        return RelativeToRoot(src)

    @staticmethod
    @docstring_parameter(Validate.__doc__)
    def validate(src: Union[Text, PathLike]) -> bool:
        """{0}\n"""
        return Validate(src)

    @staticmethod
    @docstring_parameter(DerivativesRoot.__doc__)
    def get_derivatives_root(src: Union[Text, PathLike]
                             ) -> Union[Text, PathLike]:
        """{0}\n"""
        return DerivativesRoot(src)

    @staticmethod
    @docstring_parameter(BIDSRoot.__doc__)
    def get_bids_root(src: Union[Text, PathLike]
                      ) -> PathLike:
        """{0}\n"""
        return BIDSRoot(src)

    @staticmethod
    @docstring_parameter(SubDir.__doc__)
    def get_subject_dir(src: Union[Text, PathLike]
                        ) -> PathLike:
        """{0}\n"""
        return SubDir(src)

    @staticmethod
    @docstring_parameter(SesDir.__doc__)
    def get_session_dir(src: Union[Text, PathLike]
                        ) -> PathLike:
        """{0}\n"""
        return SesDir(src)

    @staticmethod
    @docstring_parameter(MatchComponents.__doc__)
    def match_components(dst: Union[Text, PathLike],
                         recursive: bool = False,
                         src: Optional[Union[Text, PathLike]] = None,
                         exclude: Optional[Union[Iterable[Text], Text]] = None,
                         **kwargs) -> Generator:
        """{0}\n"""
        return MatchComponents(dst, recursive=recursive,
                               src=src,
                               exclude=exclude, **kwargs)

    @staticmethod
    @docstring_parameter(IsEvent.__doc__)
    def is_event_file(src: Union[Text, PathLike]
                      ) -> bool:
        """{0}\n"""
        return IsEvent(src)

    @staticmethod
    @docstring_parameter(IsBeh.__doc__)
    def is_beh_file(src: Union[Text, PathLike]
                    ) -> bool:
        """{0}\n"""
        return IsBeh(src)

    @staticmethod
    @docstring_parameter(IsBIDSRoot.__doc__)
    def is_fmriprep_derivative(src: Union[Text, PathLike]
                               ) -> bool:
        """{0}\n"""
        return IsFMRIPrepDerivatives(src)

    @staticmethod
    @docstring_parameter(IsSubjectDir.__doc__)
    def is_subject_dir(src: Union[Text, PathLike]) -> bool:
        """{0}\n"""
        return IsSubjectDir(src)

    @staticmethod
    @docstring_parameter(IsSessionDir.__doc__)
    def is_session_dir(src: Union[Text, PathLike]) -> bool:
        """{0}\n"""
        return IsSessionDir(src)

    @staticmethod
    @docstring_parameter(IsDatatypeDir.__doc__)
    def is_datatype_dir(src: Union[Text, PathLike]
                        ) -> bool:
        """{0}\n"""
        return IsDatatypeDir(src)

    @staticmethod
    @docstring_parameter(IsNifti.__doc__)
    def is_nifti_file(src: Union[Text, PathLike]) -> bool:
        """{0}\n"""
        return IsNifti(src)

    @staticmethod
    @docstring_parameter(Is4D.__doc__)
    def is_4d_file(src: Union[Text, PathLike]) -> bool:
        """{0}\n"""
        return Is4D(src)

    @staticmethod
    @docstring_parameter(Is3D.__doc__)
    def is_3d_file(src: Union[Text, PathLike]) -> bool:
        """{0}"""
        return Is3D(src)

    @staticmethod
    @docstring_parameter(IsPhysio.__doc__)
    def is_physio_file(src: Union[Text, PathLike]
                       ) -> bool:
        """{0}"""
        return IsPhysio(src)

    @staticmethod
    @docstring_parameter(IsSidecar.__doc__)
    def is_sidecar_file(src: Union[Text, PathLike]
                        ) -> bool:
        """{0}\n"""
        return IsSidecar(src)

    @staticmethod
    @docstring_parameter(IsDerivativesRoot.__doc__)
    def is_derivatives_root_dir(src: Union[Text, PathLike]
                                ) -> bool:
        """{0}\n"""
        return IsDerivativesRoot(src)

    @staticmethod
    @docstring_parameter(IsDatasetRoot.__doc__)
    def is_dataset_root_dir(src: Union[Text, PathLike]
                            ) -> bool:
        """{0}\n"""
        return IsDatasetRoot(src)

    @staticmethod
    @docstring_parameter(IsDerivatives.__doc__)
    def isderivatives(src: Union[Text, PathLike]
                      ) -> bool:
        """{0}\n"""
        return IsDerivatives(src)

    @staticmethod
    @docstring_parameter(DatasetRoot.__doc__)
    def get_dataset_root(src: Union[Text, PathLike]
                         ) -> PathLike:
        """{0}\n"""
        return DatasetRoot(src)

        # Pathlib properties

    @property
    @docstring_parameter(Path.drive.__doc__)
    def drive(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.drive

    @property
    @docstring_parameter(Path.root.__doc__)
    def root(self) -> Text:
        """{0}\n"""
        return self.path.root

    @property
    @docstring_parameter(Path.anchor.__doc__)
    def anchor(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.anchor

    @property
    @docstring_parameter(Path.parent.__doc__)
    def parent(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.parent

    @property
    def parents(self) -> Generator:
        """
        Returns a generator of this path's logical parents.

        """
        yield from self.path.parents

    @property
    @docstring_parameter(Path.name.__doc__)
    def name(self) -> Text:
        """{0}\n"""
        return self.path.name

    @property
    def suffix(self) -> Text:
        """
        Returns the final component's last suffix, if any.

        This includes the leading period. For example: '.txt'

        Notes:
            Not to be confounded with ``bids_suffix``.
        """
        return self.path.suffix

    @property
    def suffixes(self) -> Generator:
        """
        Returns a generator of the final component's suffixes, if any.

        These include the leading periods. For example: ['.tar', '.gz']

        Notes:
            Not to be confounded with ``bids_suffix``.
        """
        yield from self.path.suffixes

    @property
    @docstring_parameter(Path.stem.__doc__)
    def stem(self) -> Text:
        """{0}\n"""
        return self.path.stem

    @property
    @docstring_parameter(Path.as_posix.__doc__)
    def as_posix(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.as_posix()

    @property
    @docstring_parameter(Path.as_uri.__doc__)
    def as_uri(self) -> Text:
        """{0}\n"""
        return self.path.as_uri()

    @property
    @docstring_parameter(Path.expanduser.__doc__)
    def expanduser(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.expanduser()

    @property
    @docstring_parameter(Path.owner.__doc__)
    def owner(self) -> Text:
        """{0}\n"""
        return self.path.owner()

    @property
    @docstring_parameter(Path.group.__doc__)
    def group(self) -> Text:
        """{0}\n"""
        return self.path.group()

    @property
    @docstring_parameter(Path.resolve.__doc__)
    def resolve(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return self.path.resolve()

    @property
    @docstring_parameter(Path.home.__doc__)
    def home(self) -> Union[Text, PathLike]:
        """{0}"""
        return self.path.home()

    @property
    @docstring_parameter(Path.stat.__doc__)
    def stat(self) -> stat_result:
        """{0}\n"""
        return self.path.stat()

    @property
    @docstring_parameter(Path.lstat.__doc__)
    def lstat(self) -> stat_result:
        """{0}\n"""
        return self.path.lstat()

    @property
    @docstring_parameter(Path.exists.__doc__)
    def exists(self) -> bool:
        """{0}\n"""
        return self.path.exists()

    @property
    @docstring_parameter(Path.is_absolute.__doc__)
    def is_absolute(self) -> bool:
        """{0}\n"""
        return self.path.is_absolute()

    @property
    @docstring_parameter(Path.is_dir.__doc__)
    def is_dir(self) -> bool:
        """{0}\n"""
        return self.path.is_dir()

    @property
    @docstring_parameter(Path.is_file.__doc__)
    def is_file(self) -> bool:
        """{0}\n"""
        return self.path.is_file()

    @property
    @docstring_parameter(Path.is_mount.__doc__)
    def is_mount(self) -> bool:
        """{0}\n"""
        return self.path.is_mount()

    @property
    @docstring_parameter(Path.is_symlink.__doc__)
    def is_symlink(self) -> bool:
        """{0}\n"""
        return self.path.is_mount()

    @property
    @docstring_parameter(Path.is_symlink.__doc__)
    def is_socket(self) -> bool:
        """{0}\n"""
        return self.path.is_socket()

    @property
    @docstring_parameter(Path.is_fifo.__doc__)
    def is_fifo(self) -> bool:
        """{0}\n"""
        return self.path.is_fifo()

    @property
    @docstring_parameter(Path.is_block_device.__doc__)
    def is_block_device(self) -> bool:
        """{0}\n"""
        return self.path.is_block_device()

    @property
    @docstring_parameter(Path.is_char_device.__doc__)
    def is_char_device(self) -> bool:
        """{0}\n"""
        return self.path.is_char_device()

    @property
    def is_reserved(self) -> bool:
        """
        Returns True if ``self.path`` contains any system-reserved special names.

        """
        return self.path.is_reserved()

    # BIDSPath Properties
    @property
    @docstring_parameter(find_bids_suffix.__doc__)
    def bids_suffix(self) -> Text:
        """{0}\n"""
        return find_bids_suffix(self)

    @property
    @docstring_parameter(find_extension.__doc__)
    def extension(self) -> Text:
        """{0}\n"""
        return find_extension(self)

    @property
    @docstring_parameter(find_datatype.__doc__)
    def datatype(self) -> Text:
        """{0}\n"""
        return find_datatype(self)

    @property
    @docstring_parameter(IsBIDSRoot.__doc__)
    def is_bids_root(self) -> bool:
        """{0}\n"""
        return IsBIDSRoot(self)

    @property
    @docstring_parameter(IsDatatypeDir.__doc__)
    def is_datatype(self) -> bool:
        """{0}\n"""
        return IsDatatypeDir(self)

    @property
    @docstring_parameter(IsDerivatives.__doc__)
    def is_derivatives(self) -> bool:
        """{0}\n"""
        return IsDerivatives(self)

    @property
    @docstring_parameter(IsDerivativesRoot.__doc__)
    def is_derivatives_root(self) -> bool:
        """{0}\n"""
        return IsDerivativesRoot(self)

    @property
    @docstring_parameter(IsBeh.__doc__)
    def is_beh(self) -> bool:
        """{0}\n"""
        return IsBeh(self)

    @property
    @docstring_parameter(IsEvent.__doc__)
    def is_event(self) -> bool:
        """{0}\n"""
        return IsEvent(self)

    @property
    @docstring_parameter(IsFMRIPrepDerivatives.__doc__)
    def is_fmriprep_derivatives(self) -> bool:
        """{0}\n"""
        return IsFMRIPrepDerivatives(self)

    @property
    @docstring_parameter(IsNifti.__doc__)
    def is_nifti(self) -> bool:
        """{0}\n"""
        return IsNifti(self)

    @property
    @docstring_parameter(Is3D.__doc__)
    def is_3d(self) -> bool:
        """{0}\n"""
        return Is3D(self)

    @property
    @docstring_parameter(Is4D.__doc__)
    def is_4d(self) -> bool:
        """{0}\n"""
        return Is4D(self)

    @property
    @docstring_parameter(IsPhysio.__doc__)
    def is_physio(self) -> bool:
        """{0}\n"""
        return IsPhysio(self)

    @property
    @docstring_parameter(IsSidecar.__doc__)
    def is_sidecar(self) -> bool:
        """{0}\n"""
        return IsSidecar(self)

    @property
    @docstring_parameter(IsSubjectDir.__doc__)
    def is_subject(self) -> bool:
        """{0}\n"""
        return IsSubjectDir(self)

    @property
    @docstring_parameter(IsSessionDir.__doc__)
    def is_session(self) -> bool:
        """{0}\n"""
        return IsSessionDir(self)

    @property
    @docstring_parameter(IsDerivatives.__doc__)
    def is_derivatives(self) -> bool:
        """{0}\n"""
        return IsDerivatives(self)

    @property
    @docstring_parameter(IsDatasetRoot.__doc__)
    def is_dataset_root(self) -> bool:
        """{0}\n"""
        return IsDatasetRoot(self)

    @property
    @docstring_parameter(GetEntities.__doc__)
    def entities(self) -> NamedTuple:
        """{0}\n"""
        return GetEntities(self)

    @property
    @docstring_parameter(GetEntityStrings.__doc__)
    def entity_strings(self) -> NamedTuple:
        """{0}\n"""
        return GetEntityStrings(self)

    @property
    @docstring_parameter(GetComponents.__doc__)
    def components(self) -> Tuple:
        """{0}\n"""
        return GetComponents(self)

    @property
    @docstring_parameter(DatasetName.__doc__)
    def dataset_name(self):
        """{0}\n"""
        return DatasetName(self)

    @property
    @docstring_parameter(DatasetDescription.__doc__)
    def dataset_description(self) -> Dict:
        """{0}\n"""
        return DatasetDescription(self)

    @property
    @docstring_parameter(DatatypeModality.__doc__)
    def get_datatype_modality(self) -> Union[Text, Modality]:
        """{0}\n"""
        return DatatypeModality(self)

    @property
    @docstring_parameter(RelativeToRoot.__doc__)
    def r2r(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return RelativeToRoot(self)

    @property
    @docstring_parameter(BIDSValidator.__doc__)
    def validator(self):
        """
        Returns an instance of ``bids_validator.BIDSValidator``.

        {0}\n
        """
        return BIDSValidator()

    @property
    @docstring_parameter(Validate.__doc__)
    def is_bids(self) -> bool:
        """{0}\n"""
        return Validate(self)

    @property
    @docstring_parameter(BIDSRoot.__doc__)
    def bids_root(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return BIDSRoot(self)

    @property
    @docstring_parameter(DatasetRoot.__doc__)
    def dataset_root(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return DatasetRoot(self)

    @property
    @docstring_parameter(DerivativesRoot.__doc__)
    def derivatives_root(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return DerivativesRoot(self)

    @property
    @docstring_parameter(GetDerivativesNames.__doc__)
    def derivatives_names(self) -> Tuple:
        """{0}\n"""
        return GetDerivativesNames(self)

    @property
    @docstring_parameter(SesDir.__doc__)
    def ses_dir(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return SesDir(self)

    @property
    @docstring_parameter(SubDir.__doc__)
    def sub_dir(self) -> Union[Text, PathLike]:
        """{0}\n"""
        return SubDir(self)
