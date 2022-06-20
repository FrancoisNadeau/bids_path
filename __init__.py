
import sys
from .functions import (
    core_functions, file_functions, bids_path_functions
)
from .constants import *
    # (
#     FMRIPrepEntities, Modalities, DataModality,
#     LCStrategyDocs, BIDSDocs, BidsDocs
# )
from .core import bids_dir, bids_file
from .BIDSPath import BIDSPath
from .constants import *
# from .constants.bidspathlib_docs import BIDS_DATATYPES
# from .constants.bidspathlib_exceptions import *
# from .constants import BIDSPathConstants
from .core.bids_dir import BIDSDir, BIDSDirAbstract
from .core.bids_file import BIDSFile, BIDSFileAbstract
from .core.BIDSPathAbstract import BIDSPathAbstract

from .BIDSPathLike import BIDSPathLike
from .MatchComponents import MatchComponents
from .general_methods import *

print(sys.path[0])

__all__ = [
    "bids_dir", "bids_file", "core_functions", "file_functions",
    "bids_path_functions", "general_methods", "BIDSDir", "BIDSFile",
    "BIDSPathAbstract", "BIDSDirAbstract", "BIDSFileAbstract",
    "BIDSPathLike", "BIDSPath", "MatchComponents",
    "BIDSPathConstants", "BIDS_DATATYPES", "FMRIPrepEntities",
    "Modalities", "DataModality.py",
    "LCStrategyDocs", "BIDSDocs", "BidsDocs",
    "docstring_parameter", "get_default_args", "camel_to_snake",
    "Snake2Camel", "SetFromDict", "SubclassesRecursive",
    "rev_dict",
    "NiftiError", "NotNiftiFileError", "Not3DError",
    "Not4DError"
]
