
from setuptools import setup

AUTHOR = 'Francois Nadeau'
EMAIL = 'francois.nadeau1@gmail.com'

setup(
    name='bidspathlib',
    version='0.0.8.6',
    packages=[
        'core', 'core.tests', 'core.bids_dir', 'core.bids_file',
        'constants', 'functions'
    ],
    url='https://github.com/FrancoisNadeau/bids_path',
    license='MIT',
    author=AUTHOR,
    maintainer=AUTHOR,
    author_email=EMAIL,
    maintainer_email=EMAIL,
    description='Python package applying Path object machinery to BIDS datasets.',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.8',
    install_requires=[
        'bids-validator ~= 1.9.4',
        'pathlib2 ~= 2.3.7.post1',
        'pyyaml ~= 6.0',
        'nilearn @ git+https://github.com/nilearn/nilearn.git#egg=nilearn'
    ]
)
