
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
import yaml
from collections import namedtuple
from nibabel.nifti1 import ImageFileError
from pathlib import Path
from typing import Dict, List, Pattern, Text, Tuple, Type

__path__ = [os.path.join('', '__init__.py')]

DATA_DIR: Text = os.path.dirname(__file__)
DOCS_DIRS: List = sorted(map(lambda d: os.path.join(DATA_DIR, d),
                             ('json_docs', 'yaml_docs')))
JSON_DOCS_DIR, YAML_DOCS_DIR = DOCS_DIRS

JSON_DOCS: Tuple = tuple(map(lambda j: json.loads(Path(j).read_text()),
                             sorted(Path(JSON_DOCS_DIR).iterdir())[:-1]))
print(sorted(os.listdir(JSON_DOCS_DIR)))
BIDS_RECOMMENDED, BIDS_DATATYPES,\
    DATA_MODALITIES, ENTITY_DESC, DEPRECATED_BIDS_SUFFIXES, \
    NON_ENTITY_DESC, = JSON_DOCS

DATATYPE_STRINGS: Tuple = tuple(BIDS_DATATYPES.keys())
ENTITIES_ORDER: Tuple = tuple(ENTITY_DESC.keys())
ENTITY_STRINGS: Tuple = tuple(map(lambda i: i.get('entity'), ENTITY_DESC.values()))
print(sorted(os.listdir(YAML_DOCS_DIR)))
YAML_DOCS: Tuple = tuple(map(lambda j: yaml.load(Path(j).read_text(),
                                                 Loader=yaml.FullLoader),
                             sorted(Path(YAML_DOCS_DIR).iterdir())))
NO_EXTENSION_FILES: Tuple = ("bids_suffix", "datatype", "extension")
NIFTI_EXTENSIONS, NON_ENTITY_COMPONENTS, \
    SPECIFIC_DATATYPE_FIELDS, SUFFIX_STRINGS = YAML_DOCS

COMPONENTS_NAMES: Tuple = ENTITY_STRINGS + NO_EXTENSION_FILES
ENTITY_COLLECTOR_SLOTS: Tuple = tuple(set(ENTITIES_ORDER + COMPONENTS_NAMES))
ENTITY_STRINGS_DESC: Dict = dict(zip(ENTITY_STRINGS, ENTITY_DESC.values()))
COMPONENTS_DESC: Dict = {**ENTITY_STRINGS_DESC, **NON_ENTITY_DESC}

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
__tuples__: Tuple = (
    DATATYPE_STRINGS, ENTITIES_ORDER, ENTITY_STRINGS,
    NIFTI_EXTENSIONS, SUFFIX_STRINGS, SPECIFIC_DATATYPE_FIELDS,
    NO_EXTENSION_FILES, NON_ENTITY_COMPONENTS,
    COMPONENTS_NAMES, ENTITY_COLLECTOR_SLOTS
)
__strings__: Tuple = (DD_FILE, TIME_FORMAT, BVE_MESSAGE)
__others__: Tuple = (NIFTI_ERRORS, GenericAlias, SUFFIX_PATTERNS)
__dicts__: Tuple = (
    BIDS_RECOMMENDED, BIDS_DATATYPES, COMPONENTS_DESC,
    DEPRECATED_BIDS_SUFFIXES, ENTITY_DESC, ENTITY_STRINGS_DESC,
    DATA_MODALITIES, NIFTI_EXTENSIONS
)

__all__: List = [
    "__namedtuples__",
    "Entities", "EntityStrings", "Components", "Datatypes", "BidsRecommended",
    "__tuples__",
    "DATATYPE_STRINGS", "ENTITIES_ORDER", "ENTITY_STRINGS",
    "SUFFIX_STRINGS", "SPECIFIC_DATATYPE_FIELDS",
    "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "NON_ENTITY_DESC",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS",
    "__strings__",
    "DD_FILE", "TIME_FORMAT", "BVE_MESSAGE",
    "__others__",
    "NIFTI_ERRORS", "GenericAlias", "SUFFIX_PATTERNS",
    "__dicts__",
    "BIDS_RECOMMENDED", "BIDS_DATATYPES", "COMPONENTS_DESC",
    "DEPRECATED_BIDS_SUFFIXES", "ENTITY_DESC", "ENTITY_STRINGS_DESC",
    "DATA_MODALITIES", "NIFTI_EXTENSIONS"
]
