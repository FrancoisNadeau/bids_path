
import json
import os
from collections import namedtuple
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Text, Tuple

__path__ = [os.path.join('..', '__init__.py')]

DATA_MODALITIES_FILENAME: Text = "BIDS_datatypes_modalities.json"
DATA_MODALITIES_DIRNAME: Path = Path(os.path.dirname(__file__)).joinpath('json_docs')
DATA_MODALITIES_PATH: Path = DATA_MODALITIES_DIRNAME.joinpath(DATA_MODALITIES_FILENAME)
DATA_MODALITIES: Dict = json.loads(DATA_MODALITIES_PATH.read_text())

MODALITY_FIELDS: Tuple = (
    'long_name', 'datatypes', 'name', 'long_description'
)


class DataModality(namedtuple('DataModality', field_names=MODALITY_FIELDS)):
    """
    Category of brain json_docs recorded by a file.

    For MRI json_docs, different pulse sequences are
    considered distinct modalities (i.e. T1w, bold or dwi).
    For passive recording techniques (i.e. EEG, MEG or iEEG),
    the technique is sufficiently uniform to define
    the modalities eeg, meg and ieeg.
    When applicable, the modality is indicated in the suffix.
    The modality may overlap with, but should not
    be confused with the json_docs type.

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


DataModalities: Tuple = tuple(map(lambda val: DataModality(**val), DATA_MODALITIES.values()))

__all__: List = ["DataModality", "DataModalities", "DATA_MODALITIES"]
