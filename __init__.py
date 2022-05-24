
"""
Python package applying Path object machinery to BIDS datasets

"""

from . import (
    BIDSPath, BIDSPathLike, bidspathlib_exceptions,
    BIDSPathConstants, core, functions, general_methods
)
from .BIDSPath import BIDSPath
from .BIDSPathLike import BIDSPathLike
from .core import *
from .bidspathlib_exceptions import *
from .BIDSPathConstants import *
from .functions import *
from .fMRIPrepEntities import *
from .general_methods import *
from .Modality import Modalities


__all__ = [
    # core
    "bids_dir", "bids_file", "BIDSPathAbstract", "BIDSDirAbstract", "BIDSFileAbstract",
    # core.bids_dir
    "BIDSDir", "Datatype", "Session", "Subject", "Derivatives",
    # core.bids_file
    "BehFile", "BIDSFile", "EventsFile", "FMRIFile",
    "MRIFile", "PhysioFile", "SideCarFile",
    # main
    "BIDSPathLike", "BIDSPath", "bidspathlib_exceptions", "fMRIPrepEntities",
    "BIDSPathConstants", "core", "functions", "general_methods",
    "Modality", "Modalities",
    # general_methods
    "docstring_parameter", "get_default_args",
    "camel_to_snake", "Snake2Camel",
    "SetFromDict", "SubclassesRecursive", "rev_dict",
    # bidspathlib_exceptions
    "NiftiError", "NotNiftiFileError",
    "Not3DError", "Not4DError",
    # functions
    "core_functions", "BIDSPathFunctions", "BIDSFileFunctions",
    "BIDSFileID", "BIDSDirID", "core_functions",
    "bids_path_functions", "file_functions", "general_methods",
    "dir_id_functions", "file_id_functions",
    # functions.BIDSPathCoreFunctions
    "find_datatype", "find_entity", "find_extension",
    "find_bids_suffix",
    # functions.BIDSPathFunctions
    "root_path", "_add_root", "RelativeToRoot",
    "Validate", "SubDir", "SesDir", "BIDSRoot", "DatasetRoot",
    "DerivativesRoot", "DatasetName", "DatasetDescription",
    "DatatypeModality", "ctime_fmt", "GetComponents",
    "GetEntities", "GetEntityStrings", "PathsByPatterns",
    "GetBidsignore", "GetDerivativesNames",
    # functions.BIDSFileFunctions
    "ShapeLength", "GetMD5CheckSum", "GetSha1Sum",
    "GetFrameTimes", "GetImgHeader", "GetTR",
    # functions.BIDSFileID
    "IsNifti", "Is4D", "Is3D", "IsEvent",
    "IsBeh", "IsPhysio", "IsSidecar",
    # functions.BIDSDirID
    "IsBIDSRoot", "IsDatasetRoot", "IsSubjectDir",
    "IsSessionDir", "IsDatatypeDir", "IsDerivatives",
    "IsDerivativesRoot", "IsFMRIPrepDerivatives",
    # functions.generators
    "EntityGen", "EntityStringsGen", "ComponentsGen", "SuffixGen",
    # functions.MatchComponents
    "score_matches", "MatchComponents",
    # general_methods
    "docstring_parameter", "get_default_args", "camel_to_snake",
    "Snake2Camel", "SetFromDict", "SubclassesRecursive", "rev_dict",
    # BIDSPathConstants
    "DATATYPE_STRINGS", "ENTITIES_ORDER", "ENTITY_STRINGS",
    "ENTITY_DESC", "SES_DESCRIPTION", "NIFTI_EXTENSIONS",
    "SUFFIX_STRINGS", "SPECIFIC_DATATYPE_FIELDS", "BIDS_RECOMMENDED",
    "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS", "COMPONENTS_NAMES",
    "ENTITY_COLLECTOR_SLOTS", "MODALITIES", "DEPRECATED_BIDS_SUFFIXES",
    "DATATYPES_DESCRIPTION", "FP_STRINGS", "LCS_PARAMS",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC", "Entities",
    "EntityStrings", "Components", "Datatypes",
    "BidsRecommended", "DD_FILE", "TIME_FORMAT",
    "BVE_MESSAGE", "GenericAlias",
    "SUFFIX_PATTERNS", "__dicts__", "__namedtuples__",
    "__others__", "__strings__", "__tuples__",
    # constants.fMRIPrepEntities
    "FMRIPrep", "FreeSurfer", "FMRIPrepEntities",
    "FP_IMG_FILE_PATTERNS", "FP_ANAT_NIFTI",
    "FP_ANAT_TRANSFORMS", "FS_ANAT_GIFTI",
    "FS_ANAT_TRANSFORMS", "FP_FUNC_NIFTI", "FS_SPACES",
    "FP_CONFOUNDS", "FP_AROMA_CONFOUNDS", "field_names",
    "__sets__", "__data__", "__anat__",
    "__functional__", "__confounds__"
]
