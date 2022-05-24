# bidspathlib
Python package applying Path object machinery to BIDS datasets

Inspired by the ``mne_bids`` package, ``bidspathlib`` proposes to extend
the former's functionality to functional and anatomical magnetic resonance imaging (MRI, fMRI).


PACKAGE CONTENTS

    BIDSPath
        Main metaclass factory and prefered instantiation method.

    BIDSPathLike (Protocol)
        Extension of the abstract base class ``os.PathLike``.

    MatchComponents
        Path matching based on BIDS entity and non-entity components.

    constants (package)
        Invariable values used in the BIDSPath package.

        Contents:
            BIDSPathConstants
                Invariable values used in the BIDSPath package.
            bidspathlib_exceptions
                Package exceptions
            fMRIPrepEntities
                Documentation to help locate and match FMRIPrep derivatives.

    core (package)
        Package containing the ``bidspathlib`` abstract base classes.

        Contents:
            BIDSDirAbstract
                Abstract base class for directories in a BIDS Dataset.

            BIDSFileAbstract
                Abstract base class for files in a BIDS Dataset.

            BIDSPathAbstract
                Abstract class emulating a ``pathlib.Path`` object.

            bids_dir (package)
                Submodule for directories in a BIDS dataset.

                Contents:
                    BIDSDir
                        Metaclass acting as a factory for ``bidspathlib.bids_dir`` subclasses.
                    Datatype
                        Datatype level in a BIDS dataset directory hierarchy.
                    Derivatives
                        Class to access a participant's derived data.
                    Session
                        Session level in a BIDS dataset directory hierarchy.
                    Subject
                        Subject level in a BIDS dataset directory hierarchy.

            bids_file (package)
                Submodule for files in a BIDS dataset.

                Contents:
                    BIDSFile
                        Metaclass acting as a factory for ``bidspathlib.bids_file`` subclasses.
                    BehFile
                        Class representing a behavioural task in a BIDS dataset.
                    EventsFile
                        ``BIDSFileAbstract`` subclass storing events data along BIDS entities.
                    FMRIFile
                        Class for 4D MRI image files.
                    MRIFile
                        Class for 3D MRI image files.
                    PhysioFile
                        Class for physiological data files.
                    SideCarFile
                        Class representing a JSON sidecar file in a BIDS dataset.

            tests (package)

    functions (package)
        Functions and methods for the ``bidspathlib`` package.

        Contents:
            BIDSDirID
                Functions returning boolean values according to path characteristics.
            BIDSFileFunctions
                Functions to retrieve attributes from files in a BIDS dataset.
            BIDSFileID
                Functions returning boolean values according to path characteristics.
            BIDSPathCoreFunctions
                Core functions for the ``bidspathlib`` package.
            BIDSPathFunctions
                Path components-based file and directory identification in a BIDS dataset.

    general_methods
        General purpose methods that can work independently of ``bidspathlib``.

    setup

Usage

``bidspathlib.BIDSPath`` takes a single argument (the path) to instantialize.


Example
```
>>> bold_src, ev_src, dt_src, sub_src = '/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-memory_bold.nii.gz', '/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-memory_events.tsv', '/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func', '/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082'
>>> all_src = (bold_src, ev_src, dt_src, sub_src)
>>> tests = tuple(map(bidspathlib.BIDSPath, all_src))
>>> set(tests[-2].iterdir())
{FMRIFile(PosixPath(/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-rest_bold.nii.gz)), SideCarFile(PosixPath(/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-memory_bold.json)), SideCarFile(PosixPath(/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-rest_bold.json)), EventsFile(PosixPath(/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-memory_events.tsv)), FMRIFile(PosixPath(/media/francois/seagate_5tb1/cimaqDr10LorisBids/sub-3239082/ses-V03/func/sub-3239082_ses-V03_task-memory_bold.nii.gz))}

```
MNE-BIDS : https://github.com/mne-tools/mne-bids

TODO
 * Complete the BIDS context protocol