#!/usr/bin env python3

from collections import namedtuple
from pprint import pprint
from typing import Dict, List, Tuple, Type

from bids_path.constants import BIDSPathConstants
from bids_path.constants import exceptions
from bids_path.constants import Modality
from bids_path.constants import fMRIPrepEntities
from bids_path.constants.BIDSPathConstants import *
from bids_path.constants.exceptions import *
from bids_path.constants.fMRIPrepEntities import *
from bids_path.constants.Modality import Modality, Modalities
from bids_path.constants.fMRIPrepEntities import FMRIPrepEntities

BIDS_DOCS: Dict = {
    'BIDS_datatypes_descriptions': DATATYPES_DESC_DICT,
    'BIDS_datatypes_modalities': MODALITIES,
    'BIDS_entities_descriptions': ENTITY_DESC,
    'BIDS_entity_strings_description': ENTITY_STRINGS_DESC,
    'BIDS_components_description': COMPONENTS_DESC
}

LC_DOCS: Dict = {
'load_confounds_strategy_parameters': LCS_PARAMS
}

LC_FIELDS: Tuple = tuple(LC_DOCS.keys())
BD_FIELDS: Tuple = tuple(BIDS_DOCS.keys())


class LCStrategyDocs(namedtuple('FMRIPrepDocs', field_names=LC_FIELDS)):
    """
    Contains ``load_confounds_strategy`` parameters.

    Allows calling both ``load_confounds_strategy`` and
    ``load_confounds`` methods from ``nilearn.interfaces.fmriprep``
    with a single call depending on the user's parameters.
    """
    __slots__ = ()

    def view(self): pprint(str(self))


LCStrategyDocs: Tuple = LCStrategyDocs(**LC_DOCS)

BidsDocs: Type[Tuple] = namedtuple('BIDSDocs', field_names=BD_FIELDS)
BIDSDocs: Tuple = BidsDocs(**BIDS_DOCS)

__all__: List = [
    "BIDSPathConstants", "exceptions", "Modality", "Modalities",
    "fMRIPrepEntities", "FMRIPrepEntities", "BIDS_DOCS", "LC_DOCS",
    "LC_FIELDS", "BD_FIELDS", "LCStrategyDocs", "BidsDocs", "BIDSDocs",
    # BIDSPathConstants
    "DATATYPE_STRINGS", "DATATYPES_DESCRIPTIONS", "ENTITIES_ORDER",
    "ENTITY_STRINGS", "ENTITY_DESC", "SES_DESCRIPTION",
    "NIFTI_EXTENSIONS", "SUFFIX_STRINGS", "SPECIFIC_DATATYPE_FIELDS",
    "BIDS_RECOMMENDED", "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS", "MODALITIES",
    "HARDWARE_DESC", "DATATYPES_DESC_DICT", "DEPRECATED_BIDS_SUFFIXES",
    "DATATYPES_DESCRIPTION", "FP_STRINGS", "LCS_PARAMS",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC", "Entities",
    "EntityStrings", "Components", "Datatypes",
    "BidsRecommended", "DD_FILE", "TIME_FORMAT",
    "BVE_MESSAGE", "NIFTI_ERRORS", "GenericAlias",
    "SUFFIX_PATTERNS", "__dicts__", "__namedtuples__",
    "__others__", "__strings__", "__tuples__",
    # exceptions
    "NiftiError", "NotNiftiFileError", "Not3DError",
    "Not4DError", "__classes__",
    # fMRIPrepEntities
    "FMRIPrep", "FreeSurfer", "FMRIPrepEntities",
    "FP_IMG_FILE_PATTERNS", "FP_ANAT_NIFTI",
    "FP_ANAT_TRANSFORMS", "FS_ANAT_GIFTI",
    "FS_ANAT_TRANSFORMS", "FP_FUNC_NIFTI", "FS_SPACES",
    "FP_CONFOUNDS", "FP_AROMA_CONFOUNDS", "field_names",
    "__sets__", "__data__", "__anat__",
    "__functional__", "__confounds__"
]
