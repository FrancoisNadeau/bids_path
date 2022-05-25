
from setuptools import setup
SETUP_REQUIRES = [
    'pandas ~= 1.4.2', 'nibabel ~= 3.2.2', 'numpy ~= 1.22.4',
]
AUTHOR = 'Francois Nadeau'
EMAIL = 'francois.nadeau1@gmail.com'

setup(
    name='bidspathlib',
    version='0.0.6.4',
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
    setup_requires=SETUP_REQUIRES,
    install_requires=[
        'nilearn @ git+https://github.com/nilearn/nilearn.git#egg=nilearn'
    ]
)
