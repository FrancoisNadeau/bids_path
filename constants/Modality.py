
import os
from collections import namedtuple
from pprint import pprint
from typing import Dict, List, Text, Tuple

BIDS_DATATYPE_MODALITIES: Dict = \
    {
  "mri": {
    "long_name": "Magnetic Resonance Imaging",
    "datatypes": [
      "anat",
      "dwi",
      "fmap",
      "func",
      "perf"
    ],
    "name": "mri",
    "long_description": "Data acquired with an MRI scanner."
  },
  "eeg": {
    "long_name": "Electroencephalography",
    "datatypes": [
      "eeg"
    ],
    "name": "eeg",
    "long_description": "Data acquired with EEG."
  },
  "ieeg": {
    "long_name": "Intracranial Electroencephalography",
    "datatypes": [
      "ieeg"
    ],
    "name": "ieeg",
    "long_description": "Data acquired with iEEG."
  },
  "meg": {
    "long_name": "Magnetoencephalography",
    "datatypes": [
      "meg"
    ],
    "name": "meg",
    "long_description": "Data acquired with an MEG scanner."
  },
  "beh": {
    "long_name": "Behavioral experiments",
    "datatypes": [
      "beh"
    ],
    "name": "beh",
    "long_description": "Behavioral data acquired without accompanying neuroimaging data."
  },
  "pet": {
    "long_name": "Positron Emission Tomography",
    "datatypes": [
      "pet"
    ],
    "name": "pet",
    "long_description": "Data acquired with PET."
  },
  "micr": {
    "long_name": "Microscopy",
    "datatypes": [
      "micr"
    ],
    "name": "micr",
    "long_description": "Data acquired with a microscope."
  }
}


MODALITY_FIELDS: Tuple = (
    'long_name', 'datatypes', 'name', 'long_description'
)
__path__ = [os.path.join('..', '__init__.py')]


class Modality(namedtuple('Modality', field_names=MODALITY_FIELDS)):
    """
    Category of brain data recorded by a file.

    For MRI data, different pulse sequences are
    considered distinct modalities (i.e. T1w, bold or dwi).
    For passive recording techniques (i.e. EEG, MEG or iEEG),
    the technique is sufficiently uniform to define
    the modalities eeg, meg and ieeg.
    When applicable, the modality is indicated in the suffix.
    The modality may overlap with, but should not
    be confused with the data type.

    References:
        <https://bids-specification.readthedocs.io/en/stable/02-common-principles.html>
        Bullet-point 10.
    """
    __slots__: Tuple = ()


    def __str__(self) -> Text:
        _str = '\n'.join((' :'.join((self.name, self.long_name)),
                          self.long_description,
                          f"Possible datatypes: {self.datatypes}"))
        return str(_str)

    def view(self): pprint(str(self))


Modalities: Tuple = tuple(map(lambda val: Modality(**val), MODALITIES.values()))

__all__: List = ["Modality", "Modalities"]
