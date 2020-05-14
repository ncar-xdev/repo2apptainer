#!/usr/bin/env python

"""The setup script."""
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    INSTALL_REQUIREs = f.read().strip().split('\n')
with open('README.md', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering',
]

setup(
    name='repo2singularity',
    description='Repo2singularity: Wrapper around repo2docker producing producing Jupyter enabled Singularity images.',
    long_description=LONG_DESCRIPTION,
    python_requires='>=3.6',
    maintainer='Anderson Banihirwe',
    classifiers=CLASSIFIERS,
    url='https://github.com/andersy005/repo2singularity',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=INSTALL_REQUIREs,
    license='Apache 2.0',
    zip_safe=False,
    entry_points={'console_scripts': ['repo2singularity = repo2singularity.core:main']},
    keywords='reproducible science environments docker singularity',
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0'],
)
