
"""
Functions and methods for the ``bidspathlib`` package.

"""

import os
from typing import List

from .BIDSDirID import *
from .BIDSFileFunctions import *
from .BIDSFileID import *
from .core_functions import *
from .BIDSPathFunctions import *
from .MatchComponents import *

from .BIDSFileFunctions import __methods__ as file_functions
from .BIDSDirID import __methods__ as dir_id_functions
from .BIDSFileID import __methods__ as file_id_functions
from .core_functions import __methods__ as core_functions
from .BIDSPathFunctions import __methods__ as bids_path_functions


__all__ = [
    "core_functions", "BIDSPathFunctions", "BIDSFileFunctions",
    "BIDSFileID", "BIDSDirID", "core_functions",
    "bids_path_functions", "file_functions",
    "dir_id_functions", "file_id_functions",
    # BIDSPathCoreFunctions
    "find_datatype", "find_entity", "find_extension", "find_bids_suffix",
    # BIDSPathFunctions
    "root_path", "_add_root", "RelativeToRoot",
    "Validate", "SubDir", "SesDir", "BIDSRoot", "DatasetRoot",
    "DerivativesRoot", "DatasetName", "DatasetDescription",
    "DatatypeModality", "ctime_fmt", "GetComponents",
    "GetEntities", "GetEntityStrings", "PathsByPatterns",
    "GetBidsignore", "GetDerivativesNames",
    # BIDSFileFunctions
    "ShapeLength", "GetFrameTimes", "GetImgHeader", "GetTR",
    # BIDSFileID
    "IsNifti", "Is4D", "Is3D", "IsEvent", "IsBeh", "IsPhysio", "IsSidecar",
    # BIDSDirID
    "IsBIDSRoot", "IsDatasetRoot", "IsSubjectDir", "IsSessionDir",
    "IsDatatypeDir", "IsDerivatives", "IsDerivativesRoot", "IsFMRIPrepDerivatives",
    # generators
    "ComponentsGen", "EntityGen", "EntityStringsGen", "ExtensionGen", "SuffixGen",
    # MatchComponents
    "score_matches", "MatchComponents"
]

__path__: List = [os.path.join('..', '__init__.py')]
