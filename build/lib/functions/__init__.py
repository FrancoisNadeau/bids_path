
"""
Functions and methods for the ``bidspathlib`` package.

"""

from .BIDSDirID import *
from .BIDSDirID import __methods__ as dir_id_functions
from .BIDSFileFunctions import *
from .BIDSFileFunctions import __methods__ as file_functions
from .BIDSFileID import *
from .BIDSFileID import __methods__ as file_id_functions
from .BIDSPathCoreFunctions import *
from .BIDSPathCoreFunctions import __methods__ as core_functions
from .BIDSPathFunctions import *
from .BIDSPathFunctions import __methods__ as bids_path_functions
from ..general_methods import *
from ..general_methods import __methods__ as general_methods

__all__ = [
    "BIDSPathCoreFunctions", "BIDSPathFunctions", "BIDSFileFunctions",
    "BIDSFileID", "BIDSDirID", "core_functions",
    "bids_path_functions", "file_functions", "general_methods",
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
