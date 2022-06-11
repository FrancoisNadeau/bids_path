
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
            "Vendor-specific implementation for spoiled gradient echo acquisition.",
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

ENTITY_DESC: Dict = \
    {
    "subject": "\n".join([
        "A person or animal participating in the study."
    ]),
    "session": "\n".join([
        "A logical grouping of neuroimaging and behavioral data consistent across subjects.",
        "Session can (but doesn't have to) be synonymous to a visit in a longitudinal study.",
        "In general, subjects will stay in the scanner during one session."
        "However, for example, if a subject has to leave the scanner room and then",
        "be re-positioned on the scanner bed, the set of MRI acquisitions will still",
        "be considered as a session and match sessions acquired in other subjects.",
        "Similarly, in situations where different data types are obtained over several visits ",
        "(example fMRI on one day followed by DWI the day after) those can be grouped in one session.",
        "Defining multiple sessions is appropriate when several identical or similar",
        "data acquisitions are planned and performed on all -or most- subjects,",
        "often in the case of some intervention between sessions (for example, training)."
    ]),
  "sample": "\n".join([
      "A sample pertaining to a subject such as tissue, primary cell or cell-free sample.",
      "The `sample-<label>` key/value pair is used to distinguish between different",
      "samples from the same subject.",
      "The label MUST be unique per subject and is RECOMMENDED to be unique",
      "throughout the dataset."
  ]),
  "task": "\n".join([
      "Each task has a unique label that MUST only consist of letters and/or numbers.",
      "Other characters, including spaces and underscores, are not allowed.",
      "Those labels MUST be consistent across subjects and sessions."
  ]),
  "acquisition": "\n".join([
      "The `acq-<label>` key/value pair corresponds to a custom label the",
      "user MAY use to distinguish a different set of parameters used for",
      "acquiring the same modality.",
      "For example this should be used when a study includes two T1w images -",
      "one full brain low resolution and one restricted field of view but high resolution.",
      "In such case two files could have the following names:",
      "`sub-01_acq-highres_T1w.nii.gz` and `sub-01_acq-lowres_T1w.nii.gz`,",
      "however the user is free to choose any other label than `highres` and `lowres`",
      "as long as they are consistent across subjects and sessions.",
      "In case different sequences are used to record the same modality",
      "(for example, `RARE` and `FLASH` for T1w)"
      "this field can also be used to make that distinction.",
      "At what level of detail to make the distinction",
      "(for example,\njust between `RARE` and `FLASH`, or between `RARE`, `FLASH`, and `FLASHsubsampled`)",
      "remains at the discretion of the researcher."
  ]),
  "ceagent": "\n".join([
      "The `ce-<label>` key/value can be used to distinguish",
      "sequences using different contrast enhanced images.",
      "The label is the name of the contrast agent.",
      "The key `\"ContrastBolusIngredient\"` MAY also be added in the JSON file,",
      "with the same label."
  ]),
  "tracer": "\n".join([
      "The `trc-<label>` key/value can be used to distinguish",
      "sequences using different tracers.",
      "The key `\"TracerName\"` MUST also be included in the associated JSON file,",
      "although the label may be different."
  ]),
  "stain": "\n".join([
      "The `stain-<label>` key/pair values can be used to distinguish image files",
      "from the same sample using different stains or antibodies for contrast enhancement.",
      "Stains SHOULD be indicated in the `\"SampleStaining\"` key in the sidecar JSON file,",
      "although the label may be different.",
      "Description of antibodies SHOULD also be indicated as appropriate",
      "in `\"SamplePrimaryAntibodies\" and/or `\"SampleSecondaryAntobodies\"."
  ]),
  "reconstruction": "\n".join([
      "The `rec-<label>` key/value can be used to distinguish",
      "different reconstruction algorithms",
      "(for example `MoCo` for the ones using motion correction)."
  ]),
  "direction": "\n".join([
      "The `dir-<label>` key/value can be set to an arbitrary alphanumeric label",
      "(for example, `dir-LR` or `dir-AP`) to distinguish",
      "different phase-encoding directions."
  ]),
  "run": "\n".join([
      "If several scans with the same acquisition parameters are acquired in the same session,",
      "they MUST be indexed with the",
      "[`run-<index>`](../99-appendices/09-entities.md#run) entity:\n`_run-1`, `_run-2`, `_run-3`,",
      "and so on (only nonnegative integers are allowed as\nrun labels).",
      "If different entities apply,\nsuch as a different session indicated by",
      "[`ses-<label>`](../99-appendices/09-entities.md#ses),",
      "or different acquisition parameters indicated by",
      "[`acq-<label>`](../99-appendices/09-entities.md#acq),",
      "then `run` is not needed to distinguish the scans and MAY be omitted."
  ]),
  "modality": "\n".join([
      "The `mod-<label>` key/value pair corresponds to modality label for defacing masks,",
      "for example, T1w, inplaneT1, referenced by a defacemask image.",
      "For example, `sub-01_mod-T1w_defacemask.nii.gz`."
  ]),
  "echo": "\n".join([
      "If files belonging to an entity-linked file collection are acquired at different",
      "echo times, the `_echo-<index>` key/value pair MUST be used to distinguish individual files.",
      "This entity represents the `\"EchoTime\"` metadata field.",
      "Please note that the `<index>`\ndenotes the number/index (in the form of a nonnegative integer),",
      "not the\n`\"EchoTime\"` value which needs to be stored in the",
      "field `\"EchoTime\"` of the separate\nJSON file."
  ]),
  "flip": "\n".join([
      "If files belonging to an entity-linked file collection are acquired at different",
      "flip angles, the `_flip-<index>` key/value pair MUST be used to distinguish\nindividual files.",
      "This entity represents the `\"FlipAngle\"` metadata field.",
      "Please note that the `<index>`\ndenotes the number/index (in the form of a nonnegative integer),",
      "not the `\"FlipAngle\"`\nvalue which needs to be stored in the",
      "field `\"FlipAngle\"` of the separate JSON file."
  ]),
  "inversion": "\n".join([
      "If files belonging to an entity-linked file collection are acquired at different",
      "inversion times, the `_inv-<index>` key/value pair MUST be used to distinguish\nindividual files.",
      "This entity represents the `\"InversionTime` metadata field.",
      "Please note that the `<index>`\ndenotes the number/index (in the form of a nonnegative integer),",
      "not the `\"InversionTime\"`\nvalue which needs to be stored in",
      "the field `\"InversionTime\"` of the separate JSON file."
  ]),
  "mtransfer": "\n".join([
      "If files belonging to an entity-linked file collection are acquired at different",
      "magnetization transfer (MT) states, the `_mt-<label>` key/value pair MUST be used to",
      "distinguish individual files.",
      "This entity represents the `\"MTState\"` metadata field.",
      "Allowed label values for this\nentity are `on` and `off`,",
      "for images acquired in presence and absence of an MT pulse, respectively."
  ]),
  "part": "\n".join([
      "This entity is used to indicate which component of the complex",
      "representation of the MRI signal is represented in voxel data.",
      "The `part-<label>` key/value pair is associated with the DICOM Tag `0008, 9208`.",
      "Allowed label values for this entity are `phase`, `mag`, `real` and `imag`,",
      "which are typically used in `part-mag`/`part-phase` or\n`part-real`/`part-imag` pairs of files.",
      "Phase images MAY be in radians or in arbitrary units.",
      "The sidecar JSON file MUST include the units of the `phase` image.",
      "The possible options are `\"rad\"` or `\"arbitrary\"`.",
      "When there is only a magnitude image of a given type, the `part` key MAY be omitted."
  ]),
  "processing": "\n".join([
      "The proc label is analogous to rec for MR and denotes a variant of",
      "a file that was a result of particular processing performed on the device.",
      "This is useful for files produced in particular by Elekta's MaxFilter",
      "(for example, `sss`, `tsss`, `trans`, `quat` or `mc`),",
      "which some installations impose to be run on raw data because of active",
      "shielding software corrections before the MEG data can actually be exploited."
  ]),
  "hemisphere": "\n".join([
      "The `hemi-<label>` entity indicates which hemibrain is described by the file.",
      "Allowed label values for this entity are `L` and `R`,",
      "for the left and right hemibrains, respectively."
  ]),
  "space": "\n".join([
      "The space entity can be used to indicate in which way the electrode positions are interpreted",
      "(for EEG/MEG/iEEG data) or\nthe spatial reference to which a file has been aligned (for MRI data).",
      "The space `<label>` MUST be taken from one of the modality specific lists in",
      "[Appendix VIII](../99-appendices/08-coordinate-systems.md).",
      "For example for iEEG data, the restricted keywords listed under",
      "[iEEG Specific Coordinate Systems](../99-appendices/08-coordinate-systems.md#ieeg-specific-coordinate-systems)",
      "are acceptable for `<label>`.\n\nFor EEG/MEG/iEEG data, this entity can be applied to raw data, but",
      "for other data types, it is restricted to derivative data."
  ]),
  "split": "\n".join([
      "In the case of long data recordings that exceed a file size of 2Gb,",
      "the .fif files are conventionally split into multiple parts.",
      "Each of these files has an internal pointer to the next file.",
      "This is important when renaming these split recordings to the BIDS convention.",
      "Instead of a simple renaming, files should be read in and saved under their",
      "new names with dedicated tools like [MNE-Python](https://mne.tools/),",
      "which will ensure that not only the file names, but also the internal file pointers will be updated.",
      "It is RECOMMENDED that .fif files with multiple parts use the",
      "`split-<index>` entity to indicate each part.",
      "If there are multiple parts of a recording and the optional `scans.tsv` is provided,",
      "remember to list all files separately in `scans.tsv` and that the entries for the",
      "`acq_time` column in `scans.tsv` MUST all be identical,",
      "as described in\n[Scans file](../03-modality-agnostic-files.md#scans-file)."
  ]),
  "recording": "\n".join([
      "More than one continuous recording file can be included (with different\nsampling frequencies).",
      "In such case use different labels.",
      "For example: `_recording-contrast`, `_recording-saturation`."
  ]),
  "chunk": "\n".join([
      "The `chunk-<index>` key/value pair is used to distinguish between different",
      "regions, 2D images or 3D volumes files, of the same physical sample with",
      "different fields of view acquired in the same imaging experiment."
  ]),
  "atlas": "\n".join([
      "The `atlas-<label>` key/value pair corresponds to a custom label the user",
      "MAY use to distinguish a different atlas used for similar type of data.",
      "This entity is only applicable to derivative data."
  ]),
  "resolution": "\n".join([
      "Resolution of regularly sampled N-dimensional data.",
      "MUST have a corresponding `\"Resolution\"` metadata field to provide interpretation.",
      "This entity is only applicable to derivative data."
  ]),
  "density": "\n".join([
      "Density of non-parametric surfaces.",
      "MUST have a corresponding `Density` metadata field to provide interpretation.",
      "This entity is only applicable to derivative data."
  ]),
  "label": "\n".join([
      "Tissue-type label, following a prescribed vocabulary.",
      "Applies to binary masks and probabilistic/partial volume segmentations",
      "that describe a single tissue type.",
      "This entity is only applicable to derivative data."
  ]),
  "description": "\n".join([
      "When necessary to distinguish two files that do not otherwise have a",
      "distinguishing entity, the `_desc-<label>` keyword-value SHOULD be used.",
      "This entity is only applicable to derivative data."
  ])
}

NON_ENTITY_DESC: Dict = \
    {
    "bids_suffix": "\n".join([
        "Alphanumeric value, located after the key-value_ pairs",
        "(thus after the final _), right before the File extension.",
        "For example, it is eeg in sub-05_task-matchingpennies_eeg.vhdr"
    ]),
    "extension": "\n".join([
        "Portion of the filename after the left-most",
        "period (.) preceded by any other alphanumeric.",
        "For example, .gitignore does not have a file extension,",
        "but the file extension of test.nii.gz is .nii.gz.",
        "Note that the left-most period is included in the file extension."
    ]),
    "datatype": "\n".join([
        "Functional group of different types of data."
    ])
}
DATATYPES_DESCRIPTION: Dict = \
    {
  "anat": {
    "long_name": "Anatomical Magnetic Resonance Imaging",
    "description": "Magnetic resonance imaging sequences designed to characterize static, anatomical features.",
    "specific": {
      "nonparametric": {
        "bids_suffixes": [
          "T1w",
          "T2w",
          "PDw",
          "T2starw",
          "FLAIR",
          "inplaneT1",
          "inplaneT2",
          "PDT2",
          "angio",
          "T2star",
          "FLASH",
          "PD"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "part": "optional"
        }
      },
      "parametric": {
        "bids_suffixes": [
          "T1map",
          "T2map",
          "T2starmap",
          "R1map",
          "R2map",
          "R2starmap",
          "PDmap",
          "MTRmap",
          "MTsat",
          "UNIT1",
          "T1rho",
          "MWFmap",
          "MTVmap",
          "PDT2map",
          "Chimap",
          "S0map",
          "M0map"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional"
        }
      },
      "defacemask": {
        "bids_suffixes": [
          "defacemask"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "modality": "optional"
        }
      },
      "multiecho": {
        "bids_suffixes": [
          "MESE",
          "MEGRE"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "required",
          "part": "optional"
        }
      },
      "multiflip": {
        "bids_suffixes": [
          "VFA"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "optional",
          "flip": "required",
          "part": "optional"
        }
      },
      "multiinversion": {
        "bids_suffixes": [
          "IRT1"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "inversion": "required",
          "part": "optional"
        }
      },
      "mp2rage": {
        "bids_suffixes": [
          "MP2RAGE"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "optional",
          "flip": "optional",
          "inversion": "required",
          "part": "optional"
        }
      },
      "vfamt": {
        "bids_suffixes": [
          "MPM",
          "MTS"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "optional",
          "flip": "required",
          "mtransfer": "required",
          "part": "optional"
        }
      },
      "mtr": {
        "bids_suffixes": [
          "MTR"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "anat"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "mtransfer": "required",
          "part": "optional"
        }
      }
    }
  },
  "beh": {
    "long_name": "Behavioral Data",
    "description": "Behavioral data.",
    "specific": {
      "timeseries": {
        "bids_suffixes": [
          "stim",
          "physio"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "beh"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional",
          "recording": "optional"
        }
      },
      "noncontinuous": {
        "bids_suffixes": [
          "events",
          "beh"
        ],
        "extensions": [
          ".tsv",
          ".json"
        ],
        "datatypes": [
          "beh"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      }
    }
  },
  "dwi": {
    "long_name": "Diffusion-Weighted Imaging",
    "description": "Diffusion-weighted imaging (DWI).",
    "specific": {
      "dwi": {
        "bids_suffixes": [
          "dwi"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json",
          ".bvec",
          ".bval"
        ],
        "datatypes": [
          "dwi"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "part": "optional"
        }
      },
      "sbref": {
        "bids_suffixes": [
          "sbref"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "dwi"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "part": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "dwi"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "part": "optional",
          "recording": "optional"
        }
      }
    }
  },
  "eeg": {
    "long_name": "Electroencephalography",
    "description": "Electroencephalography",
    "specific": {
      "eeg": {
        "bids_suffixes": [
          "eeg"
        ],
        "extensions": [
          ".json",
          ".edf",
          ".vhdr",
          ".vmrk",
          ".eeg",
          ".set",
          ".fdt",
          ".bdf"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "channels": {
        "bids_suffixes": [
          "channels"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "coordsystem": {
        "bids_suffixes": [
          "coordsystem"
        ],
        "extensions": [
          ".json"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "space": "optional"
        }
      },
      "electrodes": {
        "bids_suffixes": [
          "electrodes"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "space": "optional"
        }
      },
      "events": {
        "bids_suffixes": [
          "events"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "photo": {
        "bids_suffixes": [
          "photo"
        ],
        "extensions": [
          ".jpg",
          ".png",
          ".tif"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "eeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional",
          "recording": "optional"
        }
      }
    }
  },
  "fmap": {
    "long_name": "Field maps",
    "description": "MRI scans for estimating B0 inhomogeneity-induced distortions.",
    "specific": {
      "fieldmaps": {
        "bids_suffixes": [
          "phasediff",
          "phase1",
          "phase2",
          "magnitude1",
          "magnitude2",
          "magnitude",
          "fieldmap"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "pepolar": {
        "bids_suffixes": [
          "epi",
          "m0scan"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "direction": "required",
          "run": "optional"
        }
      },
      "TB1DAM": {
        "bids_suffixes": [
          "TB1DAM"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "flip": "required",
          "inversion": "optional",
          "part": "optional"
        }
      },
      "TB1EPI": {
        "bids_suffixes": [
          "TB1EPI"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "required",
          "flip": "required",
          "inversion": "optional",
          "part": "optional"
        }
      },
      "RFFieldMaps": {
        "bids_suffixes": [
          "TB1AFI",
          "TB1TFL",
          "TB1RFM",
          "RB1COR"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "optional",
          "flip": "optional",
          "inversion": "optional",
          "part": "optional"
        }
      },
      "TB1SRGE": {
        "bids_suffixes": [
          "TB1SRGE"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "echo": "optional",
          "flip": "required",
          "inversion": "required",
          "part": "optional"
        }
      },
      "parametric": {
        "bids_suffixes": [
          "TB1map",
          "RB1map"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "fmap"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "run": "optional",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional"
        }
      }
    }
  },
  "func": {
    "long_name": "Task-Based Magnetic Resonance Imaging",
    "description": "Task (including resting state) imaging data",
    "specific": {
      "func": {
        "bids_suffixes": [
          "bold",
          "cbv",
          "sbref"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "func"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "echo": "optional",
          "part": "optional"
        }
      },
      "phase": {
        "bids_suffixes": [
          "phase"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "func"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "echo": "optional"
        }
      },
      "events": {
        "bids_suffixes": [
          "events"
        ],
        "extensions": [
          ".tsv",
          ".json"
        ],
        "datatypes": [
          "func"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "func"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "ceagent": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "recording": "optional"
        }
      }
    }
  },
  "ieeg": {
    "long_name": "Intracranial electroencephalography",
    "description": "Intracranial electroencephalography (iEEG) or electrocorticography (ECoG) data",
    "specific": {
      "ieeg": {
        "bids_suffixes": [
          "ieeg"
        ],
        "extensions": [
          ".mefd/",
          ".json",
          ".edf",
          ".vhdr",
          ".eeg",
          ".vmrk",
          ".set",
          ".fdt",
          ".nwb"
        ],
        "datatypes": [
          "ieeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "channels": {
        "bids_suffixes": [
          "channels"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "ieeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "coordsystem": {
        "bids_suffixes": [
          "coordsystem"
        ],
        "extensions": [
          ".json"
        ],
        "datatypes": [
          "ieeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "space": "optional"
        }
      },
      "electrodes": {
        "bids_suffixes": [
          "electrodes"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "ieeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "space": "optional"
        }
      },
      "events": {
        "bids_suffixes": [
          "events"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "ieeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "photo": {
        "bids_suffixes": [
          "photo"
        ],
        "extensions": [
          ".jpg",
          ".png",
          ".tif"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "ieeg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional",
          "recording": "optional"
        }
      }
    }
  },
  "meg": {
    "long_name": "Magnetoencephalography",
    "description": "Magnetoencephalography",
    "specific": {
      "meg": {
        "bids_suffixes": [
          "meg"
        ],
        "extensions": [
          "/",
          ".ds/",
          ".json",
          ".fif",
          ".sqd",
          ".con",
          ".raw",
          ".ave",
          ".mrk",
          ".kdf",
          ".mhd",
          ".trg",
          ".chn"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional",
          "processing": "optional",
          "split": "optional"
        }
      },
      "calibration": {
        "bids_suffixes": [
          "meg"
        ],
        "extensions": [
          ".dat"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": {
            "requirement": "required",
            "type": "string",
            "enum": [
              "calibration"
            ]
          }
        }
      },
      "crosstalk": {
        "bids_suffixes": [
          "meg"
        ],
        "extensions": [
          ".fif"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": {
            "requirement": "required",
            "type": "string",
            "enum": [
              "crosstalk"
            ]
          }
        }
      },
      "headshape": {
        "bids_suffixes": [
          "headshape"
        ],
        "extensions": [
          ".*",
          ".pos"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional"
        }
      },
      "markers": {
        "bids_suffixes": [
          "markers"
        ],
        "extensions": [
          ".sqd",
          ".mrk"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "optional",
          "acquisition": "optional",
          "space": "optional"
        }
      },
      "coordsystem": {
        "bids_suffixes": [
          "coordsystem"
        ],
        "extensions": [
          ".json"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional"
        }
      },
      "channels": {
        "bids_suffixes": [
          "channels"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional",
          "processing": "optional"
        }
      },
      "events": {
        "bids_suffixes": [
          "events"
        ],
        "extensions": [
          ".json",
          ".tsv"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional"
        }
      },
      "photo": {
        "bids_suffixes": [
          "photo"
        ],
        "extensions": [
          ".jpg",
          ".png",
          ".tif"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "meg"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "acquisition": "optional",
          "run": "optional",
          "processing": "optional",
          "recording": "optional"
        }
      }
    }
  },
  "micr": {
    "long_name": "Microscopy",
    "description": "Microscopy",
    "specific": {
      "microscopy": {
        "bids_suffixes": [
          "TEM",
          "SEM",
          "uCT",
          "BF",
          "DF",
          "PC",
          "DIC",
          "FLUO",
          "CONF",
          "PLI",
          "CARS",
          "2PE",
          "MPE",
          "SR",
          "NLO",
          "OCT",
          "SPIM"
        ],
        "extensions": [
          ".ome.tif",
          ".ome.btf",
          ".png",
          ".tif",
          ".json"
        ],
        "datatypes": [
          "micr"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "sample": "required",
          "acquisition": "optional",
          "stain": "optional",
          "run": "optional",
          "chunk": "optional"
        }
      },
      "photo": {
        "bids_suffixes": [
          "photo"
        ],
        "extensions": [
          ".jpg",
          ".png",
          ".tif"
        ],
        "datatypes": [
          "micr"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "sample": "required",
          "acquisition": "optional"
        }
      }
    }
  },
  "perf": {
    "long_name": "Perfusion imaging",
    "description": "Blood perfusion imaging data, including arterial spin labeling (ASL)",
    "specific": {
      "asl": {
        "bids_suffixes": [
          "asl",
          "m0scan"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "perf"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional"
        }
      },
      "aslcontext": {
        "bids_suffixes": [
          "aslcontext"
        ],
        "extensions": [
          ".tsv",
          ".json"
        ],
        "datatypes": [
          "perf"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional"
        }
      },
      "asllabeling": {
        "bids_suffixes": [
          "asllabeling"
        ],
        "extensions": [
          ".jpg"
        ],
        "datatypes": [
          "perf"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "run": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "perf"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "acquisition": "optional",
          "reconstruction": "optional",
          "direction": "optional",
          "run": "optional",
          "recording": "optional"
        }
      }
    }
  },
  "pet": {
    "long_name": "Positron Emission Tomography",
    "description": "Positron emission tomography data",
    "specific": {
      "pet": {
        "bids_suffixes": [
          "pet"
        ],
        "extensions": [
          ".nii.gz",
          ".nii",
          ".json"
        ],
        "datatypes": [
          "pet"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "optional",
          "tracer": "optional",
          "reconstruction": "optional",
          "run": "optional"
        }
      },
      "blood": {
        "bids_suffixes": [
          "blood"
        ],
        "extensions": [
          ".tsv",
          ".json"
        ],
        "datatypes": [
          "pet"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "optional",
          "tracer": "optional",
          "reconstruction": "optional",
          "run": "optional",
          "recording": "required"
        }
      },
      "events": {
        "bids_suffixes": [
          "events"
        ],
        "extensions": [
          ".tsv",
          ".json"
        ],
        "datatypes": [
          "pet"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "required",
          "tracer": "optional",
          "reconstruction": "optional",
          "run": "optional"
        }
      },
      "timeseries": {
        "bids_suffixes": [
          "physio",
          "stim"
        ],
        "extensions": [
          ".tsv.gz",
          ".json"
        ],
        "datatypes": [
          "pet"
        ],
        "entities": {
          "subject": "required",
          "session": "optional",
          "task": "optional",
          "tracer": "optional",
          "reconstruction": "optional",
          "run": "optional",
          "recording": "optional"
        }
      }
    }
  }
}

COMPONENTS_NAMES: Tuple = ENTITY_STRINGS+NON_ENTITY_COMPONENTS
ENTITY_COLLECTOR_SLOTS: Tuple = tuple(set(ENTITIES_ORDER + COMPONENTS_NAMES))

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
    ENTITY_STRINGS_DESC, COMPONENTS_DESC
)

__all__: List = [
    "ENTITY_FIELDS", "DATATYPE_STRINGS", "ENTITIES_ORDER",
    "ENTITY_STRINGS", "NIFTI_EXTENSIONS", "SUFFIX_STRINGS",
    "SPECIFIC_DATATYPE_FIELDS", "BIDS_RECOMMENDED",
    "NO_EXTENSION_FILES", "NON_ENTITY_COMPONENTS",
    "COMPONENTS_NAMES", "ENTITY_COLLECTOR_SLOTS",
    "MODALITIES", "ENTITY_DESC", "NON_ENTITY_DESC", "FP_STRINGS",
    "DATATYPES_DESCRIPTION", "DEPRECATED_BIDS_SUFFIXES",
    "ENTITY_STRINGS_DESC", "COMPONENTS_DESC",
    "__tuples__", "__dicts__"
]
