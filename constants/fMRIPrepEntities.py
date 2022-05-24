
"""
Documentation to help locate and match FMRIPrep derivatives.

"""

import os
from collections import namedtuple
from operator import itemgetter
from typing import Dict, List, Set, Tuple, Type

__path__ = [os.path.join('..', '__init__.py')]


FP_IMG_FILE_PATTERNS: Dict = {
    "aroma": "_desc-smoothAROMAnonaggr_bold",
    "nii.gz": "_space-.*_desc-preproc_bold.nii.gz",
    "dtseries.nii": "_space-.*_bold.dtseries.nii",
    "func.gii": "_space-.*_hemi-[LR]_bold.func.gii",
}

# anat
FP_ANAT_NIFTI: Set = {
'_desc-preproc_T1w.nii.gz', '_desc-brain_mask.nii.gz',
'_dseg.nii.gz', '_label-CSF_probseg.nii.gz',
'_label-GM_probseg.nii.gz', '_label-WM_probseg.nii.gz'
}
FP_ANAT_TRANSFORMS: Set = {
    '_to-T1w_mode-image_xfm.h5', '_mode-image_xfm.h5'
}
FS_ANAT_GIFTI: Set = {
    '_smoothwm.surf.gii', '_pial.surf.gii',
    '_midthickness.surf.gii', '_inflated.surf.gii'
}
FS_ANAT_TRANSFORMS: Set = {
    '_from-fsnative_to-T1w_mode-image_xfm.txt',
    '_from-T1w_to-fsnative_mode-image_xfm.txt'
}

# func
FP_FUNC_NIFTI: Set = {
    '_boldref.nii.gz', '_desc-brain_mask.nii.gz',
    '_desc-preproc_bold.nii.gz'
}
FS_FUNC_NIFTI: Set = {
    '_space-T1w_desc-aparcaseg_dseg.nii.gz',
    '_space-T1w_desc-aseg_dseg.nii.gz',
    '_space-<space_label>_hemi-[LR]_bold.func.gii'
}
FP_FUNC_TRANSFORMS: Set = {
    '_from-scanner_to-T1w_mode-image_xfm.txt',
    '_from-T1w_to-scanner_mode-image_xfm.txt'
}
FS_SPACES: Set = {
    'fsaverage', 'fsaverage5', 'fsaverage6', 'fsnative'
}

# confounds
FP_CONFOUNDS: Set = {
    '_desc-confounds_timeseries.tsv',
    '_desc-confounds_timeseries.json'
}
FP_AROMA_CONFOUNDS: Set = {
    '_AROMAnoiseICs.csv', '_desc-MELODIC_mixing.tsv'
}

__data__: Tuple = (
    FP_IMG_FILE_PATTERNS, FP_FUNC_TRANSFORMS,
    FP_CONFOUNDS, FP_AROMA_CONFOUNDS,
    FP_IMG_FILE_PATTERNS, FP_ANAT_NIFTI,
    FP_FUNC_NIFTI, FS_SPACES,
    FS_ANAT_GIFTI, FS_ANAT_TRANSFORMS,
    FS_FUNC_NIFTI
)
field_names: Tuple = (
'fp_img_file_patterns', 'fp_func_transforms', 'fp_confounds',
'fp_aroma_confounds', 'fp_img_file_patterns', 'fp_anat_nifti',
'fp_func_nifti', 'fs_spaces', 'fs_anat_gifti',
'fs_anat_transforms', 'fs_func_nifti'
)

_dict: Dict = dict(zip(field_names, __data__))

_fields: Tuple = tuple(_dict.keys())
fp_keys: Tuple = tuple(_dict.keys())[:8]
fs_keys: Tuple = tuple(_dict.keys())[8:]
fp_values: Tuple = itemgetter(*fp_keys)(_dict)
fs_values: Tuple = itemgetter(*fs_keys)(_dict)
fp_dict: Dict = dict(zip(fp_keys, fp_values))
fs_dict: Dict = dict(zip(fs_keys, fs_values))

fp: Type[Tuple] = namedtuple('FMRIPrep', field_names=fp_keys)
fs: Type[Tuple] = namedtuple('FreeSurfer', field_names=fs_keys)

FMRIPrep: Tuple = fp(**fp_dict)
FreeSurfer: Tuple = fs(**fs_dict)


class FMRIPrepEntities(namedtuple('FMRIPrepEntities',
                                  field_names=_fields)):
    """
    BIDS compliant entities for FreeSurfer and FMRIPrep outputs.


    Character strings corresponding to various FMRIPrep outputs.
    String families whose variable name starts with 'fp' or 'fs'
    represent entities defined by FMRIPrep or FreeSurfer, respectively.

    Descriptors:
        FMRIPrep:
            fp_img_file_patterns
            fp_func_transforms
            fp_confounds
            fp_aroma_confounds
            fp_img_file_patterns
            fp_anat_nifti
            fp_func_nifti
        FreeSurfer:
            * fs_spaces
            fs_anat_gifti
            fs_anat_transforms
            fs_func_nifti

    Properties: Shortcuts grouping string families by a common factor.
        freesurfer
        fmriprep
        anat_strings
        func_strings
        confounds_strings

    References:
        <https://fmriprep.org/en/stable/outputs.html#derivatives-of-fmriprep-preprocessed-data>
    *   <https://github.com/templateflow/templateflow>
    * See the Templateflow repository for a more comprehensive
      list of available resampling spaces.

    """
    __slots__: Tuple = ()

    @property
    def freesurfer(self) -> Tuple:
        """
        Shortcut to derivatives entity strings inherited from FreeSurfer.

        """
        return FreeSurfer

    @property
    def fmriperp(self) -> Tuple:
        """
        Shortcut to derivatives entity strings native to FMRIPrep.

        """
        return FMRIPrep

    @property
    def anat_strings(self) -> Dict:
        """
        Strings for anatomical outputs (both FreeSurfer and FMRIPrep).

        """
        _anat_fields = (
            'fp_anat_nifti', 'fp_anat_transforms',
            'fs_anat_gifti', 'fs_anat_transforms'
        )
        _values: Tuple = itemgetter(*_anat_fields)(self)
        return dict(zip(_anat_fields, _values))

    @property
    def func_strings(self) -> Dict:
        """
        Strings for functional outputs (both FreeSurfer and FMRIPrep).

        """
        _func_fields: Tuple = (
            'fp_func_transforms', 'fp_func_nifti',
            'fs_func_nifti'
        )
        _values: Tuple = itemgetter(*_func_fields)(self)
        return dict(zip(_func_fields, _values))

    @property
    def confounds_strings(self) -> Dict:
        """
        Strings for confounds files (FMRIPrep only).

        """
        _confounds_fields: Tuple = (
            'fp_confounds', 'fp_aroma_confounds'
        )
        _values = itemgetter(*_confounds_fields)(self)
        return dict(zip(_confounds_fields, _values))


FMRIPrepEntities = FMRIPrepEntities(**_dict)

__sets__: Tuple = (
    FP_ANAT_NIFTI, FP_ANAT_TRANSFORMS, FS_ANAT_GIFTI,
    FS_ANAT_TRANSFORMS, FP_FUNC_NIFTI, FS_SPACES,
    FP_CONFOUNDS, FP_AROMA_CONFOUNDS
)
__anat__: Tuple = (
    FP_ANAT_NIFTI, FP_ANAT_TRANSFORMS, FS_ANAT_GIFTI, FS_ANAT_TRANSFORMS
)
__functional__: Tuple = (
    FP_FUNC_NIFTI, FS_FUNC_NIFTI, FP_FUNC_TRANSFORMS, FS_SPACES
)
__confounds__: Tuple = (FP_CONFOUNDS, FP_AROMA_CONFOUNDS)

__all__: List = [
    "FMRIPrep", "FreeSurfer", "FMRIPrepEntities",
    "FP_IMG_FILE_PATTERNS", "FP_ANAT_NIFTI", "FP_ANAT_TRANSFORMS",
    "FS_ANAT_GIFTI", "FS_ANAT_TRANSFORMS", "FP_FUNC_NIFTI",
    "FS_SPACES", "FP_CONFOUNDS", "FP_AROMA_CONFOUNDS",
    "field_names", "__sets__", "__data__", "__anat__",
    "__functional__", "__confounds__"
]
