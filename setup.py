
from setuptools import setup
SETUP_REQUIRES = [
    'pandas ~= 1.4.2', 'nibabel ~= 3.2.2', 'numpy ~= 1.22.4',
]

setup(
    name='bidspathlib',
    version='0.0.1',
    packages=[
        'core', 'core.tests', 'core.bids_dir', 'core.bids_file',
        'constants', 'functions'
    ],
    url='https://github.com/FrancoisNadeau/bids_path',
    license='MIT',
    author='francois',
    author_email='francois.nadeau1@gmail.com',
    description='Python package applying Path object machinery to BIDS datasets.',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.8',
    setup_requires=SETUP_REQUIRES,
    install_requires=[
        'nilearn @ git+https://github.com/nilearn/nilearn.git#egg=nilearn'
    ]
)
