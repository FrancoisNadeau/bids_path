
"""
Submodule for directories in a BIDS dataset.

"""
import json
import os
from importlib_resources import files, as_file
from typing import List

from ..BIDSDirAbstract import BIDSDirAbstract
from ..bids_dir import (
    BIDSDir, Datatype, Dataset, Derivatives, Session, Subject
)
# from ...constants.bidspathlib_docs import BIDS_DATATYPES
# source = files('.json_docs', package='bidspathlib.constants').joinpath('datatypes_description.json')
# with as_file(source) as jfile:
#     BIDS_DATATYPES = json.load(jfile)
#     jfile.close()


__all__: List = [
    "BIDSDirAbstract", "BIDSDir", "Dataset", "Datatype",
    "Session", "Subject", "Derivatives"
]

__path__ = [os.path.join('..', '..', 'core', '__init__.py')]
