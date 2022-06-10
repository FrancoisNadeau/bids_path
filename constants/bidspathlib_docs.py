
"""
BIDS documentation and variable names in a dict.

"""
import json
import os
import sys
from glob import iglob
from importlib import resources
from pathlib import Path
from typing import Dict, List, Text, Tuple, Union

__path__ = [os.path.join('', '__init__.py')]
# DOCS_PATH = os.path.join("**", "bidspathlib", "json_docs", "**")
DOCS_PATH = resources.files('bidspathlib')

DATATYPES_PATH, MODALITIES_PATH, E_DESC_PATH, N_DESC_PATH, FP_STRINGS_PATH = \
    sorted(iglob(DOCS_PATH))
#     sorted(map(lambda p: Path(p).absolute().relative_to(Path.cwd()).absolute(),
#                iglob(os.path.join('**', 'json_docs', '**'))))

ENTITY_FIELDS: Tuple = ('format', 'enum', 'entity', 'name', 'description', 'type')
DATATYPE_STRINGS: Tuple = (
    'anat', 'beh', 'dwi', 'eeg', 'fmap', 'func', 'ieeg',
    'meg', 'micr', 'perf', 'pet'
)
ENTITIES_ORDER: Tuple = (
    'subject', 'session', 'sample', 'task', 'acquisition', 'ceagent',
    'tracer', 'stain', 'reconstruction', 'direction', 'run', 'modality',
    'echo', 'flip', 'inversion', 'mtransfer', 'part', 'processing',
    'hemisphere', 'space', 'split', 'recording', 'chunk', 'atlas',
    'resolution', 'density', 'label', 'description'
)
ENTITY_STRINGS: Tuple = (
    'sub', 'ses', 'sample', 'task', 'acq', 'ce', 'trc', 'stain', 'rec', 'dir',
    'run', 'mod', 'echo', 'flip', 'inv', 'mt', 'part', 'proc', 'hemi', 'space',
    'split', 'recording', 'chunk', 'atlas', 'res', 'den', 'label', 'desc'
)
NIFTI_EXTENSIONS: Tuple = ('.dtseries.nii', '.func.gii', '.gii', '.gii.gz', '.nii', '.nii.gz')
SUFFIX_STRINGS: Tuple = (
    '2PE', 'BF', 'Chimap', 'CARS', 'CONF', 'DIC', 'DF', 'FLAIR', 'FLASH', 'FLUO',
    'IRT1', 'M0map', 'MEGRE', 'MESE', 'MP2RAGE', 'MPE', 'MPM', 'MTR', 'MTRmap',
    'MTS', 'MTVmap', 'MTsat', 'MWFmap', 'NLO', 'OCT', 'PC', 'PD', 'PDT2',
    'PDT2map', 'PDmap', 'PDw', 'PLI', 'R1map', 'R2map', 'R2starmap', 'RB1COR',
    'RB1map', 'S0map', 'SEM', 'SPIM', 'SR', 'T1map', 'T1rho', 'T1w',
    'T2map', 'T2star', 'T2starmap', 'T2starw', 'T2w', 'TB1AFI', 'TB1DAM', 'TB1EPI',
    'TB1RFM', 'TB1SRGE', 'TB1TFL', 'TB1map', 'TEM', 'UNIT1', 'VFA', 'angio', 'asl',
    'aslcontext', 'asllabeling', 'beh', 'blood', 'bold', 'cbv', 'channels',
    'coordsystem', 'defacemask', 'dwi', 'eeg', 'electrodes', 'epi', 'events',
    'fieldmap', 'headshape', 'ieeg', 'inplaneT1', 'inplaneT2', 'm0scan', 'magnitude',
    'magnitude1', 'magnitude2', 'markers', 'meg', 'pet', 'phase', 'phase1', 'phase2',
    'phasediff', 'photo', 'physio', 'sbref', 'scans', 'sessions', 'stim', 'uCT'
)
SPECIFIC_DATATYPE_FIELDS: Tuple = ('name', 'bids_suffixes', 'extensions', 'entities')
NO_EXTENSION_FILES: Tuple = ('README', 'CHANGES', 'LICENSE')
NON_ENTITY_COMPONENTS: Tuple = ('bids_suffix', 'extension', 'datatype')
DEPRECATED_BIDS_SUFFIXES: Dict = \
    {
      "T2star": {
        "long_name": "T2* image",
        "description": "Ambiguous, may refer to a parametric image or to a conventional image.",
        "change": "Replaced by T2starw or T2starmap."
      },
      "FLASH": {
        "long_name": "Fast-Low-Angle-Shot image",
        "description": "\n".join([
            "Vendor-specific implementation for spoiled gradient echo acquisition.,
            "Commonly used for rapid anatomical imaging and different qMRI applications.",
            "For a single file, it does not convey image contrast info.",
            "In a file collection, may result in between-application filename conflicts."
        ]),
        "change": "Removed from suffixes."
      },
      "PD": {
        "long_name": "Proton density image",
        "description": "Ambiguous, may refer to a parametric image or to a conventional image.",
        "change": "Replaced by PDw or PDmap."
      }
    }
LCS_PARAMS: Dict = \
    {
    "simple": {
        "high_pass": true,
        "motion": "full",
        "wm_csf": "basic",
        "global_signal": "None",
        "demean": true
      },
    "scrubbing": {
        "high_pass": true,
        "motion": "full",
        "wm_csf": "full",
        "global_signal": "None",
        "scrub": 5.0,
        "fd_threshold": 0.2,
        "std_dvars_threshold": 3.0,
        "demean": true
      },
    "compcor": {
        "high_pass": true,
        "motion": "full",
        "compcor": "anat_combined",
        "n_compcor": "all",
        "demean": true
      },
    "ica_aroma": {
        "high_pass": true,
        "wm_csf": "basic",
        "global_signal": "None",
        "ica_aroma": "full",
        "demean": true
      }
}

COMPONENTS_NAMES: Tuple = ENTITY_STRINGS+NON_ENTITY_COMPONENTS
ENTITY_COLLECTOR_SLOTS: Tuple = tuple(set(ENTITIES_ORDER + COMPONENTS_NAMES))

MODALITIES: Dict = json.loads(MODALITIES_PATH.read_text())
ENTITY_DESC: Dict = json.loads(E_DESC_PATH.read_text())
NON_ENTITY_DESC: Dict = json.loads(N_DESC_PATH.read_text())
LCS_PARAMS: Dict = json.loads(LCS_PARAMS_PATH.read_text())
FP_STRINGS: Dict = json.loads(FP_STRINGS_PATH.read_text())
DEPRECATED_BIDS_SUFFIXES: Dict = json.loads(DEPR_S_PATH.read_text())
DATATYPES_DESCRIPTION: Dict = json.loads(DATATYPES_PATH.read_text())
ENTITY_STRINGS_DESC: Dict = dict(zip(ENTITY_STRINGS, ENTITY_DESC.values()))
COMPONENTS_DESC: Dict = {**ENTITY_STRINGS_DESC, **NON_ENTITY_DESC}

__tuples__: Tuple = (
    DATATYPE_STRINGS, ENTITIES_ORDER, ENTITY_STRINGS,
    NIFTI_EXTENSIONS, SUFFIX_STRINGS, SPECIFIC_DATATYPE_FIELDS,
    BIDS_RECOMMENDED, NO_EXTENSION_FILES, NON_ENTITY_COMPONENTS,
    COMPONENTS_NAMES, ENTITY_COLLECTOR_SLOTS
)
__dicts__: Tuple = (
    MODALITIES, DEPRECATED_BIDS_SUFFIXES,
    DATATYPES_DESCRIPTION, FP_STRINGS,
    LCS_PARAMS, ENTITY_STRINGS_DESC, COMPONENTS_DESC
)

__all__: List = [
    "ENTITY_FIELDS", "DATATYPE_STRINGS", "ENTITIES_ORDER",
    "ENTITY_STRINGS", "NIFTI_EXTENSIONS", "SUFFIX_STRINGS",
    "SPECIFIC_DATATYPE_FIELDS", "BIDS_RECOMMENDED",
    "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS",
    "MODALITIES", "ENTITY_DESC", "NON_ENTITY_DESC",
    "LCS_PARAMS", "FP_STRINGS",
    "DATATYPES_DESCRIPTION", "DEPRECATED_BIDS_SUFFIXES",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC",
    "__tuples__", "__dicts__"
]
