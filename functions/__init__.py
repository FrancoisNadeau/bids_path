#!/usr/bin/env python3

"""
Functions and methods for the ``bids_path`` package.

"""

from bids_path.functions import (
    BIDSPathCoreFunctions, BIDSPathFunctions,
    BIDSFileFunctions, BIDSFileID, BIDSDirID
)
from bids_path.functions.BIDSPathCoreFunctions import __methods__ as core_functions
from bids_path.functions.BIDSPathFunctions import __methods__ as bidspath_functions
from bids_path.functions.BIDSFileFunctions import __methods__ as file_functions
from bids_path.functions.BIDSDirID import __methods__ as dir_id_functions
from bids_path.functions.BIDSFileID import __methods__ as file_id_functions
from bids_path.functions.general_methods import __methods__ as general_methods
from bids_path.functions.BIDSPathCoreFunctions import *
from bids_path.functions.BIDSPathFunctions import *
from bids_path.functions.BIDSFileFunctions import *
from bids_path.functions.BIDSDirID import *
from bids_path.functions.BIDSFileID import *
from bids_path.functions.general_methods import *


__all__ = [
    "BIDSPathCoreFunctions", "BIDSPathFunctions", "BIDSFileFunctions",
    "BIDSFileID", "BIDSDirID", "core_functions",
    "bidspath_functions", "file_functions", "general_methods",
    "dir_id_functions", "file_id_functions", "general_methods",
    # BIDSPathCoreFunctions
    "find_datatype", "find_entity", "find_extension", "find_bids_suffix",
    "EntityGen", "EntityStringGen", "ComponentsGen", "ExtensionGen", "SuffixGen",
    # BIDSPathFunctions
    "root_path", "_add_root", "RelativeToRoot",
    "Validate", "SubDir", "SesDir", "BIDSRoot", "DatasetRoot",
    "DerivativesRoot", "DatasetName", "DatasetDescription",
    "DatatypeModality", "FormattedCtime", "GetComponents",
    "GetEntities", "GetEntityStrings", "PathsByPatterns",
    "GetBidsignore", "GetDerivativesNames",
    # BIDSFileFunctions
    "ShapeLength", "GetSidecar", "GetFMRI", "GetEvents", "GetBeh",
    "GetBrainMask", "GetAnat", "GetMD5CheckSum", "GetSha1Sum",
    "GetFrameTimes", "GetImgHeader", "GetNiftiImage", "GetTR",
    # BIDSFileID
    "IsNifti", "Is4D", "Is3D", "IsEvent", "IsBeh", "IsPhysio", "IsSidecar",
    # BIDSDirID
    "IsBIDSRoot", "IsDatasetRoot", "IsSubjectDir", "IsSessionDir",
    "IsDatatypeDir", "IsDerivatives", "IsDerivativesRoot", "IsFMRIPrepDerivatives",
    # general_methods
    "docstring_parameter", "get_default_args", "camel_to_snake",
    "Snake2Camel", "SetFromDict", "SubclassesRecursive", "rev_dict"
]
