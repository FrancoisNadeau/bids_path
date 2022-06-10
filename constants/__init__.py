
"""
Invariable values used in the BIDSPath package.

"""

import os
from collections import namedtuple
from pprint import pprint
from typing import Dict, List, Tuple, Type

from . import (
    bidspathlib_exceptions, Modality, fMRIPrepEntities
)
from .Modality import *
from .bidspathlib_docs import *
from .BIDSPathConstants import *
from .bidspathlib_exceptions import *
from .fMRIPrepEntities import *

__path__ = [os.path.join('..', '..', '__init__.py')]

BIDS_DOCS: Dict = {
    'BIDS_datatypes_descriptions': DATATYPES_DESCRIPTION,
    'BIDS_datatypes_modalities': MODALITIES,
    'BIDS_entities_descriptions': ENTITY_DESC,
    'BIDS_entity_strings_description': ENTITY_STRINGS_DESC,
    'BIDS_components_description': COMPONENTS_DESC
}
LCS_PARAMS: Dict = \
    LCS_PARAMS: Dict = \
    {
    "simple": {
        "high_pass": true,
        "motion": "full",
        "wm_csf": "basic",
        "global_signal": "None",
        "demean": true
      },
    "scrubbing": {
        "high_pass": true,
        "motion": "full",
        "wm_csf": "full",
        "global_signal": "None",
        "scrub": 5.0,
        "fd_threshold": 0.2,
        "std_dvars_threshold": 3.0,
        "demean": true
      },
    "compcor": {
        "high_pass": true,
        "motion": "full",
        "compcor": "anat_combined",
        "n_compcor": "all",
        "demean": true
      },
    "ica_aroma": {
        "high_pass": true,
        "wm_csf": "basic",
        "global_signal": "None",
        "ica_aroma": "full",
        "demean": true
      }
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
    "BIDSPathConstants", "bidspathlib_exceptions", "Modality", "Modalities",
    "fMRIPrepEntities", "FMRIPrepEntities", "BIDS_DOCS", "LC_DOCS",
    "LC_FIELDS", "BD_FIELDS", "LCStrategyDocs", "BidsDocs", "BIDSDocs",
    # BIDSPathConstants
    "DATATYPE_STRINGS", "ENTITIES_ORDER", "ENTITY_STRINGS", "ENTITY_DESC",
    "SES_DESCRIPTION", "NIFTI_EXTENSIONS", "SUFFIX_STRINGS",
    "SPECIFIC_DATATYPE_FIELDS", "BIDS_RECOMMENDED", "NO_EXTENSION_FILES",
    "NON_ENTITY_COMPONENTS", "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS",
    "MODALITIES", "DEPRECATED_BIDS_SUFFIXES",
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
