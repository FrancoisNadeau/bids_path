
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
from collections import namedtuple
from glob import iglob
from pathlib import Path
from typing import Dict, List, Pattern, Text, Tuple, Type


__path__ = [os.path.join('', '__init__.py')]

DATATYPES_PATH, MODALITIES_PATH, DEPR_S_PATH, E_DESC_PATH, N_DESC_PATH, \
FP_STRINGS_PATH, BASE_DATA_PATH, LCS_PARAMS_PATH = \
    sorted(map(lambda p: Path(p).absolute().relative_to(Path.cwd()).absolute(),
               iglob(os.path.join('**', 'json_docs', '**'))))

base_data_strings = json.loads(BASE_DATA_PATH.read_text())

ENTITY_FIELDS, DATATYPE_STRINGS, ENTITIES_ORDER, ENTITY_STRINGS, \
NIFTI_EXTENSIONS, SUFFIX_STRINGS, SPECIFIC_DATATYPE_FIELDS,\
BIDS_RECOMMENDED, NO_EXTENSION_FILES, NON_ENTITY_COMPONENTS = \
    tuple(base_data_strings.values())

COMPONENTS_NAMES: Tuple = ENTITY_STRINGS+NON_ENTITY_COMPONENTS
ENTITY_COLLECTOR_SLOTS: Tuple = tuple(set(ENTITIES_ORDER + COMPONENTS_NAMES))

MODALITIES: Dict = json.loads(MODALITIES_PATH.read_text())
ENTITY_DESC: Dict = json.loads(E_DESC_PATH.read_text())
NON_ENTITY_DESC: Dict = json.loads(N_DESC_PATH.read_text())
LCS_PARAMS: Dict = json.loads(LCS_PARAMS_PATH.read_text())
FP_STRINGS: Dict = json.loads(FP_STRINGS_PATH.read_text())
DEPRECATED_BIDS_SUFFIXES: Dict = json.loads(DEPR_S_PATH.read_text())
DATATYPES_DESCRIPTION: Dict = json.loads(DATATYPES_PATH.read_text())

ENTITY_STRINGS_DESC: Dict = dict(zip(ENTITY_STRINGS, ENTITY_DESC.values()))
COMPONENTS_DESC: Dict = {**ENTITY_STRINGS_DESC, **NON_ENTITY_DESC}

DD_FILE: Text = 'dataset_description.json'
TIME_FORMAT: Text = "%d %m %Y, %H:%M"
BVE_MESSAGE: Text = "\n".join((
    f"{DD_FILE} is missing from project root.",
    "Every valid BIDS dataset must have this file."
))
SES_DESCRIPTION: Text = ENTITY_DESC['session']
SUFFIX_PATTERNS: Pattern = re.compile('|'.join(SUFFIX_STRINGS))

Entities: Type[Tuple] = namedtuple('Entities', field_names=ENTITIES_ORDER)
EntityStrings: Type[Tuple] = namedtuple('Entities', field_names=ENTITY_STRINGS)
Components: Type[Tuple] = namedtuple('Components', field_names=COMPONENTS_NAMES)
Datatypes: Type[Tuple] = namedtuple('Datatypes', field_names=DATATYPE_STRINGS)
BidsRecommended: Type[Tuple] = namedtuple('BidsRecommended', field_names=BIDS_RECOMMENDED)

__tuples__: Tuple = (
    DATATYPE_STRINGS, ENTITIES_ORDER, ENTITY_STRINGS,
    NIFTI_EXTENSIONS, SUFFIX_STRINGS, SPECIFIC_DATATYPE_FIELDS,
    BIDS_RECOMMENDED, NO_EXTENSION_FILES, NON_ENTITY_COMPONENTS,
    COMPONENTS_NAMES, ENTITY_COLLECTOR_SLOTS
)
__dicts__: Tuple = (
    MODALITIES, DEPRECATED_BIDS_SUFFIXES, DATATYPES_DESCRIPTION, FP_STRINGS,
    LCS_PARAMS, ENTITY_STRINGS_DESC, COMPONENTS_DESC
)
__namedtuples__: Tuple = (
    Entities, EntityStrings, Components, Datatypes, BidsRecommended
)
__strings__: Tuple = (DD_FILE, TIME_FORMAT, BVE_MESSAGE)

__all__: List = [
    "DATATYPE_STRINGS", "ENTITIES_ORDER",
    "ENTITY_STRINGS", "ENTITY_DESC", "SES_DESCRIPTION",
    "NIFTI_EXTENSIONS", "SUFFIX_STRINGS", "SPECIFIC_DATATYPE_FIELDS",
    "BIDS_RECOMMENDED", "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS", "MODALITIES",
    "DEPRECATED_BIDS_SUFFIXES",
    "DATATYPES_DESCRIPTION", "FP_STRINGS", "LCS_PARAMS",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC", "Entities",
    "EntityStrings", "Components", "Datatypes",
    "BidsRecommended", "DD_FILE", "TIME_FORMAT",
    "BVE_MESSAGE",
    "SUFFIX_PATTERNS", "__dicts__", "__namedtuples__",
    "__strings__", "__tuples__"
]
