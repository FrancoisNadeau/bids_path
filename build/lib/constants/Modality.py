
from collections import namedtuple
from pprint import pprint
from typing import List, Text, Tuple

from .BIDSPathConstants import MODALITIES

MODALITY_FIELDS: Tuple = (
    'long_name', 'datatypes', 'name', 'long_description'
)


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
