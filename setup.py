#!/usr/bin/env python3

"""The setup script."""
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().strip().split('\n')
with open('README.md', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Scientific/Engineering',
]

setup(
    name='repo2singularity',
    description='Repo2singularity: Wrapper around repo2docker producing producing Jupyter enabled Singularity images.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    maintainer='Anderson Banihirwe',
    classifiers=CLASSIFIERS,
    url='https://repo2singularity.readthedocs.io',
    project_urls={
        'Documentation': 'https://repo2singularity.readthedocs.io',
        'Source': 'https://github.com/andersy005/repo2singularity',
        'Tracker': 'https://github.com/andersy005/repo2singularity/issues',
        'Discussions/Support': 'https://github.com/andersy005/repo2singularity/discussions',
    },
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    license='BSD-3-Clause',
    zip_safe=False,
    entry_points={'console_scripts': []},
    keywords='reproducible science environments docker singularity',
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
)
