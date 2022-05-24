"""
Class representing a JSON sidecar file in a BIDS dataset.

"""

import os
import json
from typing import Text, Union

from ...constants.BIDSPathConstants import BIDS_RECOMMENDED
from ..BIDSFileAbstract import BIDSFileAbstract

__path__ = [os.path.join('..', '__init__.py')]


class SideCarFile(BIDSFileAbstract):
    """
    Class representing a JSON sidecar file in a BIDS dataset.

    Descriptors correspond to the BIDS RECOMMENDED
    scanner hardware information.
    The defined fields are enumerated below:
        ('Manufacturer', 'ManufacturersModelName', 'DeviceSerialNumber',
         'StationName', 'SoftwareVersions', 'MagneticFieldStrength',
         'ReceiveCoilName', 'ReceiveCoilActiveElements', 'GradientSetType',
         'MRTransmitCoilSequence', 'MatrixCoilMode', 'CoilCombinationMethod')
    """
    __slots__ = BIDS_RECOMMENDED
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        conditions = (hasattr(instance, 'entities'),
                      instance.is_sidecar)
        return True if all(conditions) else False

    def view(self, indent: int = 2, **kwargs):
        viewer = json.dumps(self.path.read_text(),
                            indent=indent, **kwargs)
        print(viewer)

    def __init__(self, src: Union[Text, os.PathLike], **kwargs):
        super().__init__(src, **kwargs)
        self.__set_from_dict__(super().sidecar)
