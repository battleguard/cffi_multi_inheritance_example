#!/usr/bin/env python
import os
import typing
from setuptools import setup, find_namespace_packages

install_requires = [
    'cffi',
    'numpy',
    'py-afsim>=0.1.2'
]

tests_require = [
    'mypy',
    'flake8',
    'pytest',
    'pytest-cov',
    'pylint',
    'rope',
    'autopep8',
]


def get_data_files_from_root(
        root_path: str,
        rel_path_suffix: str = '') -> typing.List[typing.Tuple[str, typing.List[str]]]:
    """
    Builds data files list for adding files to package.
    Will keep the folder at the end of the root_path variable

    Parameters
    ----------
    root_path: root path to copy data file from
    rel_path_suffix: add this path to the install directory

    Returns
    -------
    the data files list to give the setup function
    """
    base_directory_name = os.path.basename(os.path.normpath(root_path))
    data_files_extra_dict = {}
    for dirpath, dirnames, filenames in os.walk(root_path):
        for item in filenames:
            full_path = os.path.join(dirpath, item)
            rel_path = os.path.relpath(dirpath, root_path)
            lister = data_files_extra_dict.setdefault(os.path.join(base_directory_name, rel_path, rel_path_suffix), [])
            lister.append(full_path)
    data_files_extra = [(key, value) for key, value in data_files_extra_dict.items()]
    return data_files_extra


# set the data files for learjet library
learjet_root = os.environ['PREFIX']
learjet_lib_path = os.path.join(learjet_root, 'lib')
learjet_include_path = os.path.join(learjet_root, 'include')
learjet_wsf_plugins_path = os.path.join(learjet_root, 'bin')
learjet_share_path = os.path.join(learjet_root, 'share')
data_files_learjet_lib = get_data_files_from_root(learjet_lib_path)
data_files_learjet_include = get_data_files_from_root(learjet_include_path)
data_files_learjet_wsf_plugins = get_data_files_from_root(learjet_wsf_plugins_path)
data_files_learjet_share = get_data_files_from_root(learjet_share_path)

setup(
    name='learjet-afsim',
    description='Python wrapper for learjet but viewed through afsim',
    python_requires='~=3.7',
    install_requires=install_requires,
    tests_require=tests_require,
    packages=find_namespace_packages(include=["pyafsim_plugins.learjet"]),
    data_files=data_files_learjet_lib + data_files_learjet_include + data_files_learjet_wsf_plugins + data_files_learjet_share
)
