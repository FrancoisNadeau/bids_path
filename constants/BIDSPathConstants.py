
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
BIDS_RECOMMENDED: Dict = \
    {
  "Manufacturer": {
    "description": "Manufacturer of the equipment that produced the measurements.",
    "dicom_tag": "Corresponds to DICOM Tag 0008, 0070 Manufacturer."
  },
  "ManufacturersModelName": {
    "description": "Manufacturer's model name of the equipment that produced the measurements.",
    "dicom_tag": "Corresponds to DICOM Tag 0008, 1090 Manufacturers Model Name."
  },
  "DeviceSerialNumber": {
    "description": "The serial number of the equipment that produced the measurements.\nA pseudonym can also be used to prevent the equipment from being identifiable, so long as each pseudonym is unique within the dataset.",
    "dicom_tag": "Corresponds to DICOM Tag 0018, 1000 DeviceSerialNumber."
  },
  "StationName": {
    "description": "Institution defined name of the machine that produced the measurements.",
    "dicom_tag": "Corresponds to DICOM Tag 0008, 1010 Station Name."
  },
  "SoftwareVersions": {
    "description": "Manufacturer's designation of software version of the equipment that produced the measurements.",
    "dicom_tag": "Corresponds to DICOM Tag 0018, 1020 Software Versions."
  },
  "MagneticFieldStrength": {
    "description": "Nominal field strength of MR magnet in Tesla.",
    "dicom_tag": "Corresponds to DICOM Tag 0018, 0087 Magnetic Field Strength."
  },
  "ReceiveCoilName": {
    "description": "Information describing the receiver coil.\nNot all vendors populate that DICOM Tag, in which case this field can be derived from an appropriate private DICOM field.",
    "dicom_tag": "Corresponds to DICOM Tag 0018, 1250 Receive Coil Name"
  },
  "ReceiveCoilActiveElements": {
    "description": "Information describing the active or selected elements of the receiver coil.\nThe vendor-defined terminology for active coil elements can go in this field.",
    "dicom_tag": "None"
  },
  "GradientSetType": {
    "description": "It should be possible to infer the gradient coil from the scanner model.\nIf not, for example because of a custom upgrade or use of a gradient insert set, then the specifications of the actual gradient coil should be reported independently.",
    "dicom_tag": "None"
  },
  "MRTransmitCoilSequence": {
    "description": "This is a relevant field if a non-standard transmit coil is used.",
    "dicom_tag": "Corresponds to DICOM Tag 0018, 9049 MR Transmit Coil Sequence."
  },
  "MatrixCoilMode": {
    "description": "(If used) A method for reducing the number of independent channels by combining in analog the signals from multiple coil elements.\nThere are typically different default modes when using un-accelerated or accelerated (for example, \"GRAPPA\", \"SENSE\") imaging.",
    "dicom_tag": "None"
  },
  "CoilCombinationMethod": {
    "description": "Most fMRI studies using phased-array coils use root-sum-of-squares (rSOS) combination, but other methods exist.\nThe image reconstruction is changed by the coil combination method (as for the matrix coil mode above), so anything non-standard should be reported.",
    "dicom_tag": "None"
  },
  "HardcopyDeviceSoftwareVersion": {
    "description": "Manufacturer's designation of the software of the device that created this Hardcopy Image (the printer).",
    "dicom_tag": "Corresponds to DICOM Tag 0018, 101A Hardcopy Device Software Version."
  }
}


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
