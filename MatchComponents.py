#!/usr/bin/env python3

"""
Path matching based on BIDS entity and non-entity components.

"""

import os
import re
from glob import iglob
from os import PathLike
from typing import Generator, Iterable, Optional, Text, Union
from bids_path.functions.BIDSPathCoreFunctions import ComponentsGen


def score_matches(path0: Union[Text, PathLike],
                  path1: Union[Text, PathLike]) -> int:
    set0, set1 = set(ComponentsGen(path0)), set(ComponentsGen(path1))
    return len(set0.intersection(set1))


def MatchComponents(dst: Union[Text, PathLike],
                    recursive: bool = False,
                    src: Optional[Union[Text, PathLike]] = None,
                    exclude: Optional[Iterable[Text]] = None,
                    pattern: Optional[Text] = None,
                    **kwargs) -> Generator:
    """
    Returns matching filenames based on the BIDS specification.

    The term "components" is used to designate both key-value
    BIDS entities and single-string identifiers
    (i.e. bids_suffix, extension, datatype).

    Notes:
        * All entities are named with their short form (e.g. "sub", "ses").
        * Both key and hyphen are included in each field's value.
        Example for user-specified (``kwargs``) and detected (``src``):
            {
                'sub': 'sub-<number>', 'ses': 'ses-<number>',
                'mod': 'mod-T1w', 'bids_suffix': 'defacemask',
                'extension': '.nii.gz', 'datatype': 'anat'
            }.

    Args:
        dst: str or PathLike
            Directory in which to start looking for matches.
            Can be used at user's discretion in combination
            with parameter ``recursive``.
        recursive: bool (Default=False)
            Whether to search recursively into directory ``dst``.
        src: str or PathLike, optional
            The path from which to lookup for matches.
        exclude: Iterable[str], optional
            Iterable representing string patterns that
            must not be present within the results.
        pattern: Iterable[str], optional
            Should match the '.gitignore' syntax.
        kwargs: Dict
            Used to overwrite or add different components than
            those found within path ``src``.
            Can be used to exclude components from the search
            by assigning an empty string ('') to a given key.

    Returns: Generator
        Yields unique file or directory paths matching the criteria.

    """
    kwargs, src = kwargs if kwargs else {}, src if src else ''
    components = dict((ComponentsGen(src, **kwargs))).values()
    pattern = pattern if pattern else '**/**'
    paths = set(iglob(os.path.join(str(dst), pattern), recursive=recursive))
    if exclude:
        ex = re.compile('|'.join(exclude))
        paths = set(filter(lambda p: not bool(ex.search(p)), paths))
    paths = set(filter(lambda p: all((x in p for x in components)), paths))
    paths = ((p, score_matches(src, p)) for p in paths)
    yield from iter(p[0] for p in sorted(paths, key=lambda s: s[::-1],
                                         reverse=True))
