#******************************************************************************
# CUI
#
# The Advanced Framework for Simulation, Integration, and Modeling (AFSIM)
#
# This is a US Government Work not subject to copyright protection in the US.
#
# The use, dissemination or disclosure of data in this file is subject to
# limitation or restriction. See accompanying README and LICENSE for details.
#******************************************************************************
#
#******************************************************************************

"""
This class sets up the interface interface between c-afsim and py-afsim using CFFI.

The code in this class will check to see if c-afsim exists then loads the header files to be used by the py-afsim
interface.
"""

import logging
import os

import plugin_util as putil

log = logging.getLogger(__name__)


class UnitsFFI(putil.InterfaceFFI):
    """
    AFSIMFFI Provides C Foreign Function Interface for Python.
    """
    _LIBNAME = "cafsim"
    PLUGINS = None

    """
    Absolute Path to the library root where the include,bin,lib folders are located. This will be set after the first
    __init__ is called on this class
    """
    LIBRARY_ROOT = ""
    """
    Absolute path to the .so or .dll of cafsim. This will be set after the first __init is called on this class
    """
    LIBRARY_LOCATION = ""

    hints = {
        "ENV": "CAFSIM_ROOT",
        "PATH": [
            "/opt/libcafsim",
            "/usr/local"
        ]
    }

    def __init__(self):
        """
        The init function for an AfsimFFI class

        This Function first checks if the AfsimFFi plugin is loaded if not then it loads the plugins.
        Then if on linux loads the proper directory to the ld_library_path environment var.
        If the AFSIMFFI.Lib is empty set a var library_root which contains the path to c-afsim get headers
        from libary_root. Get AfsimFFI.FFI and AfsimFFI.Lib
        """
        putil.InterfaceFFI.__init__(self)

        if AfsimFFI.LIB is not None:
            return

        # find the library root and library location
        AfsimFFI.LIBRARY_ROOT, AfsimFFI.LIBRARY_LOCATION = putil.find_library_root_2(AfsimFFI._LIBNAME,
                                                                                     hints=AfsimFFI.hints,
                                                                                     is_lib_good=AfsimFFI.is_cafsim_root_good)

        # setup LD_LIBRARY_PATH or PATH for handling library loading
        if os.name == 'nt':
            path_suffixes = ['bin', 'wsf_plugins', os.path.join('bin', 'wsf_plugins')]
            env_var_name = 'PATH'
        else:
            path_suffixes = ['lib', 'wsf_plugins', os.path.join('bin', 'lib'),
                             os.path.join('bin', 'wsf_plugins')]
            env_var_name = 'LD_LIBRARY_PATH'
        for path_suffix in path_suffixes:
            full_path = os.path.join(AfsimFFI.LIBRARY_ROOT, path_suffix)
            if os.path.isdir(full_path):
                if os.getenv(env_var_name) is not None:
                    os.environ[env_var_name] += os.pathsep + full_path
                else:
                    os.environ[env_var_name] = full_path

        # get the headers for the library using the library_root
        headers = AfsimFFI.get_headers(library_root=AfsimFFI.LIBRARY_ROOT)
        # get FFI and LIB from the load library
        AfsimFFI.FFI, AfsimFFI.LIB = putil.load_library(AfsimFFI.LIBRARY_LOCATION, headers=headers)

        # setup WSF_PLUGIN_PATH environment variable
        if "WSF_PLUGIN_PATH" in os.environ:
            if not os.path.isdir(os.environ["WSF_PLUGIN_PATH"]):
                raise NotADirectoryError(f"WSF_PLUGIN_PATH environment variable was set to "
                                         f"{os.environ['WSF_PLUGIN_PATH']} but directory not found. This is needed "
                                         f"in order to utilize py-afsim. Please try updating this environment "
                                         f"variable or removing it so py-afsim can use the default path instead")
        else:
            from os.path import join, isdir
            possible_wsf_plugins_dirs = [join(AfsimFFI.LIBRARY_ROOT, "bin", "wsf_plugins"),
                                         join(AfsimFFI.LIBRARY_ROOT, "wsf_plugins")]
            for wsf_plugin_dir in possible_wsf_plugins_dirs:
                if isdir(wsf_plugin_dir):
                    os.environ["WSF_PLUGIN_PATH"] = wsf_plugin_dir
                    break
            if os.getenv("WSF_PLUGIN_PATH") is None:
                raise NotADirectoryError(f"py-afsim could not find a wsf_plugins directory which is required to run"
                                         f"afsim. Paths looked = {possible_wsf_plugins_dirs}")

        # load all plugins
        if not AfsimFFI.PLUGINS:
            AfsimFFI.PLUGINS = putil.load_plugins()

    @staticmethod
    def is_cafsim_root_good(path: str, file_to_check='ArticulatedPart.h'):
        """
        Check if the path for the library root is good or not

        Parameters
        ----------
        path: str
            The path to c-afsim root
        file_to_check: ArticulatedPart.h
            File that is part of c-afsim root

        Returns
        -------
        bool
            Returns true if found_lib, header_directory_path, single_header_path exists
        """
        header_result, header_path = putil.locate_file(file_to_check, path, [os.path.join('include', 'c-afsim')])

        return header_result

    @classmethod
    def get_headers(cls: "AfsimFFI", library_root: str = None):
        """Gets the cafsim headers

        Parameters
        ----------
        library_root: str
            Location of the cafsim root
        """
        if library_root is None:
            library_root = putil.find_library_root(AfsimFFI._LIBNAME,
                                                   hints=AfsimFFI.hints,
                                                   is_lib_good=AfsimFFI.is_cafsim_root_good)
        headers = putil.find_library_headers(library_root=library_root, subfolders=["c-afsim"], glob=['**/*.h'])

        # check to see if single header already exists
        single_header = [h for h in headers if h.name == 'cafsim.h']
        if single_header:
            with open(single_header[0], 'r') as fin:
                return fin.read()
        else:
            import_order = [
                "Util.h",  # contains cBool
                "Path.h",  # has enums used in waypoint
                "Types.h",  # contains SpatialDomain
                "ArticulatedPart.h",
                "EmInteraction.h",
                "EmTypes.h",
                "Sensor.h",
            ]

            return putil.load_headers(headers, import_order=import_order)
