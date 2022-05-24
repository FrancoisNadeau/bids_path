
from setuptools import setup, find_packages

with open('README.md') as fp:
    LONG_DESCRIPTION = fp.read()

SETUP_REQUIRES = [
    'pandas ~= 1.4.2', 'nibabel ~= 3.2.2', 'numpy ~= 1.22.4',
]

setup(
    name='bidspathlib',
    version='0.0.8.5',
    url='https://github.com/FrancoisNadeau/bids_path',
    download_url='https://github.com/FrancoisNadeau/bids_path',
    license='MIT',
    author='francois',
    author_email='francois.nadeau1@gmail.com',
    maintainer='francois',
    maintainer_email='francois.nadeau1@gmail.com',
    description='Python package applying Path object machinery to BIDS datasets.',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'bidspathlib.json_docs': ['*.json']},

    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
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
