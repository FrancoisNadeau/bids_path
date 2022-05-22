#!/usr/bin/env python3

from os import PathLike
from pandas import DataFrame, read_csv
from typing import Text, Union

from bids_path.core.BIDSFileAbstract import BIDSFileAbstract


class EventsFile(BIDSFileAbstract):
    """
    ``BIDSFileAbstract`` subclass storing events data along BIDS entities.

    Properties:
        table: DataFrame
            Experimental manipulation timing information.
        intent: str or PathLike
            Path of the corresponding functional scan file.
        sidecar: dict
            Description of each column found in property ``data``.

    References:
        <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html>
    """
    __slots__ = ()
    def __type__(self): return type(self)

    def __instancecheck__(self, instance) -> bool:
        return all((hasattr(instance, 'entities'),
                    self.is_event_file(instance)))

    def __init__(self, src: Union[Text, PathLike], **kwargs):
        super().__init__(src, **kwargs)

    @property
    def table(self, **kwargs) -> DataFrame:
        """
        Events from an experimental task.

        To be BIDS-compliant and work with ``nilearn``,
        the ``DataFrame`` MUST minimally have the
        {'onset', 'duration', 'trial_type'}.

        References:
            <https://nilearn.github.io/modules/generated/nilearn.glm.first_level.make_first_level_design_matrix.html#nilearn.glm.first_level.make_first_level_design_matrix>
        """
        return read_csv(self.path, sep='\t', **kwargs)
