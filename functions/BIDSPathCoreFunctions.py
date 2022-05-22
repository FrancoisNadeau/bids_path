#!/usr/bin/env python3

"""
Core functions for the ``bids_path`` package.

Each function defined here acts as the base of
other classes and methods in the ``bids_path`` package.
"""

import re
import warnings
from os import PathLike
from pathlib import Path
from typing import (
    Dict, Generator, List, Optional, Pattern, Text, Tuple, Union
)

from bids_path.constants.BIDSPathConstants import (
    DATATYPE_STRINGS, DEPRECATED_BIDS_SUFFIXES, ENTITIES_ORDER,
    ENTITY_STRINGS, SUFFIX_PATTERNS
)


def find_datatype(src: Union[Text, PathLike],
                  datatype: Optional[Text] = None) -> Text:
    """
    Returns a file's BIDS-supported datatype, if any.

    Args:
        src: str, os.PathLike or type(Path)
            Path to the BIDS dataset file or directory.

        datatype: str (optional)
            String representing a valid BIDS ``datatype`` name
            used to manually specify what to look up for.
            Valid choices are
            {'anat', 'beh', 'dwi', 'eeg', 'fmap', 'func',
            'ieeg', 'meg', 'micr', 'perf', 'pet'}.

    Returns: str
        Sting corresponding to a BIDS-supported datatype abbreviation.

    References:
        <https://bids-specification.readthedocs.io/en/stable/schema/index.html#datatypesyaml>
        Bullet-point 6.
    """
    to_compile = '|'.join(DATATYPE_STRINGS) \
        if datatype is None else datatype
    pattern: Pattern = re.compile(to_compile)
    try:
        return pattern.search(str(src)).group()
    except AttributeError:
        return ''


def find_entity(src: Union[Text, PathLike], entity: Text,
                keep_key: bool = True) -> Text:
    """
    Returns a hyphen-separated (or not) <name>-<value> BIDS ``entity`` string.

    Args:
        src: str, os.PathLike or type(Path)
            Path to the BIDS dataset file.
        entity: str
            Entity prefix (eg.: 'sub')
            Valid choices:
                {'subject', 'session', 'sample', 'task', 'acquisition',
                'ceagent', 'tracer', 'stain', 'reconstruction',
                'direction', 'run', 'modality', 'echo', 'flip',
                'inversion', 'mtransfer', 'part', 'processing',
                'hemisphere', 'space', 'split', 'recording',
                'chunk', 'atlas', 'resolution', 'density',
                'label', 'description'}
        keep_key: bool (Default = True)
            Indicates whether to strip the <key-> part.

    Returns: str

    References:
        <https://bids-specification.readthedocs.io/en/stable/schema/index.html#modalitiesyaml_1>
    """

    pat: Pattern = re.compile(fr"(?<={entity}-)[a-zA-Z\d]*")
    try:
        value = pat.search(str(src)).group()
        value = f'{entity}-' + value if keep_key else value
    except AttributeError:
        value: Text = ''
    return value


def find_bids_suffix(src: Union[Text, PathLike]) -> Text:
    """
    Returns a file's BIDS suffix, if any.

    Args:
        src: str, os.PathLike or type(Path)

    Returns: str

    Notes:
        Use ``bids_path.constants.SUFFIX_STRINGS``
        to view supported BIDS suffixes.

    References:
        <https://bids-specification.readthedocs.io/en/stable/02-common-principles.html>
        Bullet-point 13.
    """
    try:
        _suf = SUFFIX_PATTERNS.search(str(src)).group()
        if _suf in DEPRECATED_BIDS_SUFFIXES.keys():
            _msg = DEPRECATED_BIDS_SUFFIXES[_suf]
            warnings.warn('\n'.join((f"{_suf} ({_msg['long_name']}) is deprecated.",
                                     f"{_msg['change']}",
                                     f"{_msg['description']}")),
                          FutureWarning)
        return _suf
    except AttributeError:
        return ''


def find_extension(src: Union[Text, PathLike]) -> Text:
    """
    Returns a file's extension, if any.

    The file's extension is returned whole to
    distinguish multi-extension (e.g.: <file.nii>, <file.nii.gz>),
    including the leading dot.

    Args:
        src: str, os.PathLike or type(Path)

    Returns: str
    """
    try:
        split_name = str(src).split('.', maxsplit=1)
        return '.' + split_name[1]
    except IndexError:
        return ''


def EntityGen(src: Union[Text, PathLike]) -> Generator:
    """
    Generator yielding BIDS ``entity`` key-value pairs.

    Args:
        src: str or PathLike
            Path pointing to a single run data acquisition file.

    Returns: Generator[Tuple[str, str]]
        Yields strings corresponding to hyphen-separated
        BIDS ``entity`` key-value pairs of strings.
        The format is as follows:
            {<entity name>: <entity value>}
            - i.e.: {subject: <entity value>}
    """
    yield from ((ENTITIES_ORDER[e[0]],
                 find_entity(src, e[1], keep_key=False))
                for e in enumerate(ENTITY_STRINGS))


def EntityStringGen(src: Union[Text, PathLike]) -> Generator:
    """
    Generator yielding BIDS ``entity`` key-value pairs.

    Args:
        src: str or PathLike
            Path pointing to a single run data acquisition file.

    Returns: Generator[Tuple[str, str]]
        Yields strings corresponding to hyphen-separated
        BIDS ``entity`` key-value pairs of strings.
        The format is a follows:
            {<entity string>: <entity string>-<entity value>}
            - i.e.: {sub: sub-<entity value>}
    """
    yield from ((ENTITY_STRINGS[e[0]],
                 find_entity(src, e[1], keep_key=True))
                for e in enumerate(ENTITY_STRINGS))


def ComponentsGen(src: Union[Text, PathLike], **kwargs) -> Generator:
    """
    Generator yielding all BIDS file name components strings.

    According to the BIDS Specification website,
    "A filename consists of a chain of entities,
    or key-value pairs, a suffix and an extension."[1]

    The ``suffix`` component is added as the ``bids_suffix`` property
    to avoid namespace conflict with ``pathlib.Path.suffix``.

    Note that the ``extension`` property includes the leading '.'.

    The ``datatype`` component is added at the very end since
    it is not already accessible via a path's sole file name.

    Args:
        src: str or PathLike
            Path to a directory within a BIDS dataset.

    Returns: Generator[str]
        Yields BIDS component strings found in path ``src``.

    References:
        [1] <https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#file-name-structure>
    """
    kwargs: Dict = kwargs if kwargs is not None else {}
    if src is not None:
        entity_dict = dict(EntityStringGen(src))
        entity_dict.update({'bids_suffix': find_bids_suffix(src),
                            'extension': find_extension(src),
                            'datatype': find_datatype(src)})
    else:
        entity_dict = {}
    entity_dict = {**entity_dict, **kwargs}
    yield from (item for item in entity_dict.items())


########################################################################
# For directories
########################################################################


def ExtensionGen(src: Union[Text, PathLike]) -> Generator:
    """
    Generator yielding BIDS extension strings.

    Args:
        src: str or PathLike
            Path to a directory within a BIDS dataset.

    Returns: Generator[str]
        Yields strings corresponding to the whole extension
        of files in the directory ``src``.
    """
    src = Path(src)
    filtered = filter(Path.is_file, src.rglob('*')) \
        if src.is_dir() else [src]
    files = set(map(lambda p: find_extension(p), filtered))
    yield from (_ for _ in files)


def SuffixGen(src: Union[Text, PathLike]) -> Generator:
    """
    Generator yielding BIDS ``suffix`` strings.

    Args:
        src: str or PathLike
            Path to a directory within a BIDS dataset.

    Returns: Generator[str]
        Yields BIDS ``suffix`` strings of files in directory ``src``.
    """
    src = Path(src)
    filtered = filter(Path.is_file, src.rglob('*')) \
        if src.is_dir() else [src]
    files = set(map(lambda p: find_bids_suffix(p), filtered))
    yield from (_ for _ in files)


__methods__: Tuple = (
    find_datatype, find_entity, find_extension,
    find_bids_suffix, EntityGen, EntityStringGen,
    ComponentsGen, ExtensionGen, SuffixGen
)

__all__: List = [
    "find_datatype", "find_entity", "find_extension",
    "find_bids_suffix", "EntityGen", "EntityStringGen", "ComponentsGen",
    "ExtensionGen", "SuffixGen",
    "__methods__"
]
