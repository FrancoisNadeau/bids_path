#!/usr/bin/env python3

"""
Invariable values used in the BIDSPath package.

Predefined character strings, ``namedtuple`` containers,
type hinting shortcuts and exceptions*
for the BIDSPath package.

Notes:
    * See file ``constants.exceptions``.

References:
    DEPRECATED_BIDS_SUFFIXES:
        <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#deprecated-suffixes>

"""
import json
import re
from collections import namedtuple
from nibabel.filebasedimages import ImageFileError
from pathlib import Path
from typing import Dict, List, NamedTuple, Pattern, Text, Tuple, Type

DATATYPE_STRINGS: Tuple = (
    'anat', 'beh', 'dwi', 'eeg', 'fmap', 'func',
    'ieeg', 'meg', 'micr', 'perf', 'pet'
)
ENTITIES_ORDER: Tuple = (
    'subject', 'session', 'sample', 'task', 'acquisition', 'ceagent',
    'tracer', 'stain', 'reconstruction', 'direction', 'run',
    'modality', 'echo', 'flip', 'inversion', 'mtransfer', 'part',
    'processing', 'hemisphere', 'space', 'split', 'recording',
    'chunk', 'atlas', 'resolution', 'density', 'label', 'description'
)
ENTITY_STRINGS: Tuple = (
    'sub', 'ses', 'sample', 'task', 'acq', 'ce', 'trc', 'stain',
    'rec', 'dir', 'run', 'mod', 'echo', 'flip', 'inv', 'mt', 'part',
    'proc', 'hemi', 'space', 'split', 'recording', 'chunk', 'atlas',
    'res', 'den', 'label', 'desc'
)
NIFTI_EXTENSIONS: Tuple = (
    '.dtseries.nii', '.func.gii', '.gii',
    '.gii.gz', '.nii', '.nii.gz'
)
SUFFIX_STRINGS: Tuple = (
    '2PE', 'BF', 'Chimap', 'CARS', 'CONF', 'DIC', 'DF', 'FLAIR',
    'FLASH', 'FLUO', 'IRT1', 'M0map', 'MEGRE', 'MESE', 'MP2RAGE',
    'MPE', 'MPM', 'MTR', 'MTRmap', 'MTS', 'MTVmap', 'MTsat', 'MWFmap',
    'NLO', 'OCT', 'PC', 'PD', 'PDT2', 'PDT2map', 'PDmap', 'PDw', 'PLI',
    'R1map', 'R2map', 'R2starmap', 'RB1COR', 'RB1map', 'S0map', 'SEM',
    'SPIM', 'SR', 'T1map', 'T1rho', 'T1w', 'T2map', 'T2star',
    'T2starmap', 'T2starw', 'T2w', 'TB1AFI', 'TB1DAM', 'TB1EPI',
    'TB1RFM', 'TB1SRGE', 'TB1TFL', 'TB1map', 'TEM', 'UNIT1', 'VFA',
    'angio', 'asl', 'aslcontext', 'asllabeling', 'beh', 'blood',
    'bold', 'cbv', 'channels', 'coordsystem', 'defacemask', 'dwi',
    'eeg', 'electrodes', 'epi', 'events', 'fieldmap', 'headshape',
    'ieeg', 'inplaneT1', 'inplaneT2', 'm0scan', 'magnitude',
    'magnitude1', 'magnitude2', 'markers', 'meg', 'pet', 'phase',
    'phase1', 'phase2', 'phasediff', 'photo', 'physio', 'sbref',
    'scans', 'sessions', 'stim', 'uCT'
)
SPECIFIC_DATATYPE_FIELDS: Tuple = (
    'name', 'bids_suffixes', 'extensions', 'entities'
)
BIDS_RECOMMENDED: Tuple = (
    "Manufacturer", "ManufacturersModelName",
    "DeviceSerialNumber", "StationName",
    "SoftwareVersions", "MagneticFieldStrength",
    "ReceiveCoilName", "ReceiveCoilActiveElements",
    "GradientSetType", "MRTransmitCoilSequence",
    "MatrixCoilMode", "CoilCombinationMethod"
)
NO_EXTENSION_FILES: Tuple = ('README', 'CHANGES', 'LICENSE')
NON_ENTITY_COMPONENTS: Tuple = ('bids_suffix', 'extension', 'datatype')
COMPONENTS_NAMES: Tuple = ENTITY_STRINGS+NON_ENTITY_COMPONENTS
ENTITY_COLLECTOR_SLOTS: Tuple = tuple(set(ENTITIES_ORDER + COMPONENTS_NAMES))

MODALITIES_PATH: Text = 'bids_path/constants/BIDS_datatypes_modalities.json'
D_DESC_PATH: Text = 'bids_path/constants/BIDS_datatypes_descriptions.json'
E_DESC_PATH: Text = 'bids_path/constants/BIDS_entities_descriptions.json'
N_DESC_PATH: Text = 'bids_path/constants/BIDS_non_entity_components_descriptions.json'
HARDWARE_DOCS_PATH: Text = 'bids_path/constants/BIDS_scanner_hardware_metadata.json'
LCS_PARAMS_PATH: Text = 'bids_path/constants/load_confounds_strategy_parameters.json'
FP_STRINGS_PATH: Text = 'bids_path/constants/FMRIPrep_output_strings.json'
DEPR_S_PATH: Text = 'bids_path/constants/BIDS_deprecated_suffixes.json'
DATATYPES_PATH: Text = 'bids_path/constants/BIDS_datatypes.json'

MODALITIES: Dict = json.loads(Path.cwd().joinpath(MODALITIES_PATH).read_text())
DATATYPES_DESC_DICT: Dict = json.loads(Path.cwd().joinpath(D_DESC_PATH).read_text())
ENTITY_DESC: Dict = json.loads(Path.cwd().joinpath(E_DESC_PATH).read_text())
NON_ENTITY_DESC: Dict = json.loads(Path.cwd().joinpath(N_DESC_PATH).read_text())
HARDWARE_DESC: Dict = json.loads(Path.cwd().joinpath(HARDWARE_DOCS_PATH).read_text())
LCS_PARAMS: Dict = json.loads(Path.cwd().joinpath(LCS_PARAMS_PATH).read_text())
FP_STRINGS: Dict = json.loads(Path.cwd().joinpath(FP_STRINGS_PATH).read_text())
DEPRECATED_BIDS_SUFFIXES: Dict = json.loads(Path.cwd().joinpath(DEPR_S_PATH).read_text())
DATATYPES_DESCRIPTION: Dict = json.loads(Path.cwd().joinpath(DATATYPES_PATH).read_text())

ENTITY_STRINGS_DESC: Dict = dict(zip(ENTITY_STRINGS, ENTITY_DESC.values()))
COMPONENTS_DESC: Dict = {**ENTITY_STRINGS_DESC, **NON_ENTITY_DESC}

DD_FILE: Text = 'dataset_description.json'
TIME_FORMAT: Text = "%d %m %Y, %H:%M"
BVE_MESSAGE: Text = "\n".join((
    f"{DD_FILE} is missing from project root.",
    "Every valid BIDS dataset must have this file."
))
DATATYPES_DESCRIPTIONS: Text = json.dumps(DATATYPES_DESC_DICT, indent=2)
SES_DESCRIPTION: Text = ENTITY_DESC['session']
SUFFIX_PATTERNS: Pattern = re.compile('|'.join(SUFFIX_STRINGS))

Entities: Type[NamedTuple] = namedtuple('Entities', field_names=ENTITIES_ORDER)
EntityStrings: Type[NamedTuple] = namedtuple('Entities', field_names=ENTITY_STRINGS)
Components: Type[Tuple] = namedtuple('Components', field_names=COMPONENTS_NAMES)
Datatypes: Type[NamedTuple] = namedtuple('Datatypes', field_names=DATATYPE_STRINGS)
BidsRecommended: Type[NamedTuple] = namedtuple('BidsRecommended', field_names=BIDS_RECOMMENDED)

NIFTI_ERRORS: Tuple = (
    AssertionError, AttributeError, StopIteration,
    FileNotFoundError, TypeError, ImageFileError
)
GenericAlias: Type = type(List[int])

__tuples__: Tuple = (
    DATATYPE_STRINGS, ENTITIES_ORDER, ENTITY_STRINGS,
    NIFTI_EXTENSIONS, SUFFIX_STRINGS, SPECIFIC_DATATYPE_FIELDS,
    BIDS_RECOMMENDED, NO_EXTENSION_FILES, NON_ENTITY_COMPONENTS,
    COMPONENTS_NAMES, ENTITY_COLLECTOR_SLOTS
)
__dicts__: Tuple = (
    MODALITIES, HARDWARE_DESC, DATATYPES_DESC_DICT,
    DEPRECATED_BIDS_SUFFIXES, DATATYPES_DESCRIPTION, FP_STRINGS,
    LCS_PARAMS, ENTITY_STRINGS_DESC, COMPONENTS_DESC
)
__namedtuples__: Tuple = (
    Entities, EntityStrings, Components, Datatypes, BidsRecommended
)
__strings__: Tuple = (DD_FILE, TIME_FORMAT, BVE_MESSAGE)

__others__: Tuple = (NIFTI_ERRORS, GenericAlias, SUFFIX_PATTERNS)

__all__: List = [
    "DATATYPE_STRINGS", "DATATYPES_DESCRIPTIONS", "ENTITIES_ORDER",
    "ENTITY_STRINGS", "ENTITY_DESC", "SES_DESCRIPTION",
    "NIFTI_EXTENSIONS", "SUFFIX_STRINGS", "SPECIFIC_DATATYPE_FIELDS",
    "BIDS_RECOMMENDED", "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS", "MODALITIES",
    "HARDWARE_DESC", "DATATYPES_DESC_DICT", "DEPRECATED_BIDS_SUFFIXES",
    "DATATYPES_DESCRIPTION", "FP_STRINGS", "LCS_PARAMS",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC", "Entities",
    "EntityStrings", "Components", "Datatypes",
    "BidsRecommended", "DD_FILE", "TIME_FORMAT",
    "BVE_MESSAGE", "NIFTI_ERRORS", "GenericAlias",
    "SUFFIX_PATTERNS", "__dicts__", "__namedtuples__",
    "__others__", "__strings__", "__tuples__"
]
