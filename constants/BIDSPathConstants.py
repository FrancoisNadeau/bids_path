
"""
Invariable values used in the BIDSPath package.

Predefined character strings, ``namedtuple`` containers,
type hinting shortcuts and exceptions*
for the BIDSPath package.

Notes:
    * See file ``constants.bidspathlib_exceptions``.

References:
    BIDS_RECOMMENDED:
        https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#scanner-hardware
    DATATYPE_STRINGS:
        https://github.com/bids-standard/bids-specification/blob/master/src/schema/objects/datatypes.yaml
    DEPRECATED_BIDS_SUFFIXES:
        https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#deprecated-suffixes
    ENTITIES_ORDER:
        https://github.com/bids-standard/bids-specification/blob/master/src/schema/rules/entities.yaml
    ENTITY_STRINGS:
        https://bids-specification.readthedocs.io/en/stable/99-appendices/09-entities.html
    NO_EXTENSION_FILES:
        https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html
    SUFFIX_STRINGS:
        https://github.com/bids-standard/bids-specification/blob/master/src/schema/objects/suffixes.yaml

"""
import json
import os
import re
import sys
from collections import namedtuple
from glob import iglob
from os.path import abspath, dirname, join
from pathlib import Path
from typing import (
    Dict, List, Optional, Pattern, Text, Tuple, Type, Union
)
from nibabel.filebasedimages import ImageFileError

from ..general_methods import root_path
from .bidspathlib_docs import *

__path__: List = [join(sys.path[0], '__init__.py')]

DD_FILE: Text = 'dataset_description.json'
TIME_FORMAT: Text = "%d %m %Y, %H:%M"
BVE_MESSAGE: Text = "\n".join((
    f"{DD_FILE} is missing from project root.",
    "Every valid BIDS dataset must have this file."
))

SUFFIX_PATTERNS: Pattern = re.compile('|'.join(SUFFIX_STRINGS))

Entities: Type[Tuple] = namedtuple('Entities', field_names=ENTITIES_ORDER)
EntityStrings: Type[Tuple] = namedtuple('Entities', field_names=ENTITY_STRINGS)
Components: Type[Tuple] = namedtuple('Components', field_names=COMPONENTS_NAMES)
Datatypes: Type[Tuple] = namedtuple('Datatypes', field_names=DATATYPE_STRINGS)
BidsRecommended: Type[Tuple] = namedtuple('BidsRecommended', field_names=BIDS_RECOMMENDED)

NIFTI_ERRORS: Tuple = (
    AssertionError, AttributeError, StopIteration,
    FileNotFoundError, TypeError, ImageFileError
)
GenericAlias: Type = type(List[int])

__namedtuples__: Tuple = (
    Entities, EntityStrings, Components, Datatypes, BidsRecommended
)
__strings__: Tuple = (DD_FILE, TIME_FORMAT, BVE_MESSAGE)

__others__: Tuple = (NIFTI_ERRORS, GenericAlias, SUFFIX_PATTERNS)

__all__: List = [
    "DATATYPE_STRINGS", "ENTITIES_ORDER",
    "ENTITY_STRINGS", "ENTITY_DESC",
    "NIFTI_EXTENSIONS", "SUFFIX_STRINGS", "SPECIFIC_DATATYPE_FIELDS",
    "BIDS_RECOMMENDED", "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS", "MODALITIES",
    "DEPRECATED_BIDS_SUFFIXES",
    "DATATYPES_DESCRIPTION", "FP_STRINGS", "LCS_PARAMS",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC", "Entities",
    "EntityStrings", "Components", "Datatypes",
    "BidsRecommended", "DD_FILE", "TIME_FORMAT",
    "BVE_MESSAGE", "NIFTI_ERRORS", "GenericAlias",
    "SUFFIX_PATTERNS", "__dicts__", "__namedtuples__",
    "__others__", "__strings__", "__tuples__"
]
