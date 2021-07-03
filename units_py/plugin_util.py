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

import abc
import importlib
import os
import pathlib
import pkgutil
import re
import sys
import typing
import weakref
from collections import OrderedDict
from ctypes.util import find_library

import cffi
HeaderList = typing.List[typing.Type[pathlib.Path]]
GlobList = typing.Union[typing.List[str], typing.Tuple[str]]


def load_plugins():
    """
    Loads namespace plugins
    """

    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    import pyafsim_plugins
    discovered_plugins = {}
    for finder, name, ispkg in iter_namespace(pyafsim_plugins):
        discovered_plugins[name] = importlib.import_module(name)

    return discovered_plugins


def load_headers(headers: HeaderList, import_order: list = None) -> str:
    """
    Reads in headers and removes macros, comments, and other items that aren't cffi (pycparser) compliant

    Parameters
    ----------
    headers
        List of header files
    import_order
        Order of header files that should be processed first because they are included in other headers

    Returns
    -------
    str
        All of the headers combined into a single string
    """
    def remove_comments(string):
        string = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", string)  # remove /* COMMENTS */
        string = re.sub(re.compile(r"//.*?\n"), "", string)  # //COMMENTS\n
        return string

    # order in which headers should be included
    if import_order is None:
        import_order = []
    import_idx = OrderedDict([(h.name, idx) for idx, h in enumerate(headers) if h.name in import_order])
    priority_headers = [headers[import_idx[v]] for v in import_order]
    [headers.remove(h) for h in priority_headers]
    headers = priority_headers + headers
    cdef = []
    for h in headers:
        with open(h, 'r') as fin:
            ignore = False
            found_extern = False
            for line in fin.readlines():
                strip_line = line.strip()
                if strip_line.startswith("/"):
                    continue
                elif strip_line.startswith("}") and ignore:
                    continue
                elif strip_line.startswith("#"):
                    if "__cplusplus" in strip_line:
                        ignore = True

                        # assumes __cplusplus surrounds extern "C"
                        found_extern = True if not found_extern else False
                        continue
                    elif strip_line.startswith("#endif") and ignore:
                        ignore = False
                        continue
                    else:
                        continue
                elif ignore or not found_extern:
                    continue
                else:
                    add_line = line.rstrip()
                    if add_line:
                        # remove comments /*
                        if add_line.strip().startswith("*") or add_line.strip().startswith("/"):
                            continue
                        # remove // comments at end of lines
                        comment_idx = add_line.find("//")
                        if comment_idx > 0:
                            add_line = add_line[:comment_idx]

                        add_line = add_line.rstrip()
                        if add_line.startswith("WRAPPER_EXPORT"):
                            add_line = add_line[15:]

                        cdef.append(add_line)

    cdef_str = '\n'.join(cdef)
    return remove_comments(cdef_str)


def find_library_root(name: str, hints: dict = None,
                      path_suffixes: typing.List[str] = None,
                      is_lib_good: typing.Callable[[str], bool] = None) -> str:
    """

    Parameters
    ----------
    name
        library name to search for
    hints
        root paths to search. If None is passed it will use by default the following:
        ["bin/lib", "lib", "bin", "bin/wsf_plugins", "wsf_plugins"]
    path_suffixes
        list of paths to append to the paths it searches
    is_lib_good
    hints
        the following keys in dict that define where root library install is, include lib and include folder
        {
            "ENV": ENV_VAR
            "PATH": [ABS_PATH1, ABS_PATH2,  ...]
        }

    Returns
    -------
    str
        Root location where library is located, should be similar to following directory structure

        library_root
        ├── include
        │   └── mylib.h
        └── lib
            └── mylib.so

    """
    library_root, library_file_path = find_library_root_2(name, hints, path_suffixes, is_lib_good)
    return library_root


def find_library_root_2(name: str, hints: dict = None,
                        path_suffixes: typing.List[str] = None,
                        is_lib_good: typing.Callable[[str], bool] = None) -> typing.Tuple[str, str]:
    """
    This is the same function as `find_library_root` but it also returns the path to the library also
    See `find_library_root` for documentation on usage

    Returns
    ------'
    library_root : str
        Path to the library root
    library_path : str
        Path to the library found
    """
    if path_suffixes is None:
        path_suffixes = ["bin/lib", "lib", "bin", "bin/wsf_plugins", "wsf_plugins"]
    if is_lib_good is None:
        def is_lib_good(_):
            return True

    if hints:
        if "PATH" not in hints:
            hints["PATH"] = []

        # add in environment variable path if it exists
        env_var_name = hints["ENV"] if hints and "ENV" in hints else name.upper() + "_ROOT"
        if os.getenv(env_var_name) is not None:
            hints["PATH"].append(os.environ[env_var_name])

        # add location relative to python exe this will be the virtual environment root
        hints["PATH"].append(pathlib.Path(pathlib.PurePath(sys.executable, "../..")).resolve())

    # # first try the find_library function
    # if find_library(name):
    #     library_root, lib_path = _find_library_impl(name, is_lib_good)
    #     if library_root:
    #         return library_root, lib_path

    # search paths provided in hints
    for library_root in hints["PATH"]:
        if os.name == 'nt':
            result, path = locate_file(f'{name}*.dll', library_root, path_suffixes)
        else:
            result, path = locate_file([f'{name}*.so', f'lib{name}*.so'], library_root, path_suffixes)
        if result and is_lib_good(library_root):
            return library_root, path
    raise NotADirectoryError(f"Library root location could not be found for '{name}', pass additional hints."
                             f" Current hints are: {hints['PATH']}")


# this function has been split out from the find_library_root and is meant to only be used by it
def _find_library_impl(name: str, is_lib_good: typing.Callable[[str], bool]):
    from ctypes import Structure, c_void_p, c_char_p, CDLL, c_int, byref, cast, POINTER
    # adapted from https://stackoverflow.com/questions/35682600/get-absolute-path-of-shared-library-in-python
    # linkmap structure, we only need the second entry
    class LINKMAP(Structure):
        _fields_ = [("l_addr", c_void_p), ("l_name", c_char_p)]

    libc = CDLL(find_library(name))
    libdl = CDLL(find_library('dl'))

    dlinfo = libdl.dlinfo
    dlinfo.argtypes = c_void_p, c_int, c_void_p
    dlinfo.restype = c_int

    # gets typecasted later, I dont know how to create a ctypes struct pointer instance
    lmptr = c_void_p()

    # 2 equals RTLD_DI_LINKMAP, pass pointer by reference
    dlinfo(libc._handle, 2, byref(lmptr))

    # typecast to a linkmap pointer and retrieve the name.
    abspath = cast(lmptr, POINTER(LINKMAP)).contents.l_name

    lib_file = abspath.decode('utf-8')

    if pathlib.Path(lib_file).parent.name == "wsf_plugins":
        library_root = pathlib.Path(lib_file).parent.parent.parent
    elif pathlib.Path(lib_file).parent.name == "lib":
        library_root = pathlib.Path(lib_file).parent.parent
    else:
        raise ValueError
    if is_lib_good(library_root):
        return library_root, lib_file
    return None, None


# noinspection SpellCheckingInspection
def find_library_headers(library_root: str = None, headers: typing.List[str] = None,
                         subfolders: typing.List[str] = None,
                         glob: GlobList = ('**/*.h')) -> HeaderList:
    """
    Searches for header files

    Parameters
    ----------
    library_root
        Root location where library headers and shared library can be found, see `find_library_root`
    headers: optional
        List header file(s), if None, uses subfolder w/glob
    subfolders: optional
        Ignored if headers is defined

        Provides a list of subfolders to append to `f"{library_root}/include/` and will
        include all .h files when `glob` default is used
    glob: optional
        Ignored if headers is defined

        Works with `subfolders` argument to help filter header file selection
        defaults to ('**/*.h')

    Returns
    -------
    HeaderList
        List of header files

    Notes
    -----
    You must use `headers` or `subfolders`/`glob`
    """
    if headers:
        header_list = [pathlib.Path(library_root, "include", h) for h in headers]
        for header in header_list:
            if not header.exists():
                raise FileNotFoundError(f"File does not exist: {header}")

        return header_list
    elif subfolders:
        header_list = []
        header_paths = [pathlib.Path(library_root, "include", dir) for dir in subfolders]
        for h_path in header_paths:
            for g in glob:
                header_list += list(h_path.glob(g))

        if not header_list:
            error_msg = "\n" + "\n".join(str(h) for h in header_paths)
            raise FileNotFoundError(f"Could not find headers in following paths: {error_msg}")

        return sorted(header_list)

    raise RuntimeError("find_library_headers must be called with either headers or subfolder defined")


def locate_file(possible_file_names: typing.Union[str, typing.List[str]], root_dir: str,
                path_suffixes: typing.Union[None, typing.List[str]] = None) -> typing.Tuple[bool, str]:
    """
    Locate a file using the `root_dir` passed in, all `possible_file_names` passed in and appends the `path_suffixes` to the
    `root_dir` when searching

    Parameters
    ----------
    possible_file_names : Union[str,List[str]]
        a list of all possible file names to search for. Only one has to be found and not all of them
        This can also accept just a single file being passed in instead of a list
        possible_file_names supports globbing expressions
    root_dir : str
        root directory to search
    path_suffixes : Union[None,List[str]]
        if set append it will add these path_suffixes to the search path

    Returns
    -------
    bool
        bool result where if true the file was located
    str
        string representation of the path to the located file. Empty is not found
    """
    if isinstance(possible_file_names, str):
        file_names = [possible_file_names]
    else:
        file_names = possible_file_names
    search_paths: typing.List[str] = [pathlib.Path(root_dir)]
    for path_suffix in path_suffixes:
        search_paths.append(os.path.join(root_dir, path_suffix))
    for search_path in search_paths:
        for file_name in file_names:
            for found_file in pathlib.Path(search_path).glob(file_name):
                return True, str(found_file)
    return False, ""


def load_library(libname: str, headers: str, postfix: str = "", library_root: str = "") -> \
        typing.Tuple['cffi.api.FFI', 'FFILibrary']:
    """
    Loads library and creates FFI and LIB objects
    Parameters
    ----------
    libname
        Name of library
    headers
        All headers in single string that is compliant w/pycparser library
    postfix
        Postfix attached to library name, e.g. AFSIM uses `ln4m64` to describe linux gcc 4 on 64-bit
    library_root
        The root of the library which will be checked if the dlopen fails
    Returns
    -------
    cffi.api.FFI
        FFI object
    FFILibrary
        Library to call C functions in shared library (.so/.dll)
    """
    FFI = cffi.FFI()
    FFI.cdef(headers)

    # if the passed in libname is an absolute path to the library then just try and load that
    if os.path.isabs(libname) and os.path.isfile(libname):
        absolute_lib_path = libname
    else:
        # else try and load the library using the default lib names and also try and locate the absolute path to the lib
        # so we try and handle loading libs that cannot be loaded by just libname
        if os.name == 'nt':
            lib_names = [f'{libname}{postfix}*.dll', f'{libname}{postfix}_d.dll']
        else:
            lib_names = [f'{libname}{postfix}*.so', f'lib{libname}{postfix}.so']
        path_prefixes = ["bin/lib", "lib", "bin", "bin/wsf_plugins", "wsf_plugins"]
        result, absolute_lib_path = locate_file(lib_names, library_root, path_prefixes)

        if not result:
            raise ValueError(
                f"load_library failed to find {libname}. Looked in the root path of {library_root} and sub "
                f"folders of {path_prefixes} for files with the following names {lib_names}")

    try:
        LIB = FFI.dlopen(absolute_lib_path)
        return FFI, LIB
    except OSError:
        if os.name == 'nt':
            raise ValueError(f"load_library failed on FFI.dlopen when called on {absolute_lib_path}. This is usually "
                             f"due to all libraries not being part of the PATH environment variable. "
                             f"PATH=${os.getenv('PATH')}")
        else:
            raise ValueError(
                f"load_library failed on FFI.dlopen when called on {absolute_lib_path}. This is usually due"
                f"to all libraries not being part of the LD_LIBRARY_PATH environment variable. "
                f"LD_LIBRARY_PATH=${os.getenv('LD_LIBRARY_PATH')}")


class InterfaceFFI(metaclass=abc.ABCMeta):
    """
    Functions to assist interaction w/CFFI

    Notes
    -----
    See afsim_interface.AfsimFFI for example usage
    """
    CPointer = typing.TypeVar('CPointer')

    _LIBNAME = None

    # Must define following class attributes and properties below
    LIB = None
    FFI = None

    _instance_cache = weakref.WeakValueDictionary()

    def __init__(self):
        self._children = weakref.WeakValueDictionary()

    def _reset(self, *args, **kwargs):
        """
        Method used to free underlying allocated memory
        """
        raise NotImplementedError

    def reset(self):
        try:
            self._reset()
        except NotImplementedError:
            ...

    def __del__(self):
        self.reset()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()

    def get_ptr(self):
        if hasattr(self, "_ptr"):
            return self._ptr
        else:
            return None

    def _add_child(self, obj):
        addr = self.get_obj_address(obj._ptr)
        self._children[addr] = obj

    def _reset_children(self):
        keys = list(self._children.keys())[::1]
        for k in keys:
            # log.debug(f"remove_child {k}")
            v = self._children.pop(k, None)
            if v:
                v._reset()

    def get_obj_address(self, obj: typing.Any):
        """
        Get address of object

        Parameters
        ----------
        obj
            Python obejct
        Returns
        -------
        str
            as hex
        """
        return hex(id(obj)) if obj else None

    @classmethod
    def from_ptr(cls, ptr: "InterfaceFFI.CPointer"):
        obj = InterfaceFFI._instance_cache.get(ptr)
        if obj is not None and type(obj) is cls:
            return obj
        obj = cls()
        obj._ptr = ptr
        InterfaceFFI._instance_cache[ptr] = obj
        return obj

    @classmethod
    @abc.abstractmethod
    def get_headers(cls):
        raise RuntimeError("Abstract property that needs to be defined in subclass")

    @classmethod
    def get_libname(cls):
        return cls._LIBNAME

    @classmethod
    def _is_null(cls, pointer):
        return cls.FFI.NULL == pointer

    @classmethod
    def to_str(cls, cdata_str):
        return cls.FFI.string(cdata_str).decode()

    @classmethod
    def ndarray_ptr(cls, ndarray: np.ndarray):
        ctype = "double"
        if ndarray.dtype == np.float32:
            ctype = "float"
        if ndarray.dtype == int:
            ctype = "int"

        return cls.FFI.cast(f"{ctype} *", ndarray.ctypes.data)

    @classmethod
    def to_c_list(cls, pylist: typing.Union[typing.List, typing.Tuple]):
        """
        Helper method to convert python lists to c-style lists e.g. char**

        Parameters
        ----------
        pylist


        Returns
        -------

        """
        clist = None
        cdata_type = "char"

        if pylist:
            el0 = pylist[0]
            if isinstance(el0, str):
                cdata_type = "char"
            else:
                raise ValueError("List type is currently supported")

            list_items = [cls.FFI.new(f"{cdata_type}[]", i) for i in pylist]

            if cdata_type == "char":
                # add nullptr to end of list
                list_items = list_items.append(cls.FFI.cast(f"{cdata_type}*", 0))
        else:
            list_items = [cls.FFI.cast(f"{cdata_type}*", 0)]

        return cls.FFI.new(f"{cdata_type} *[]", list_items)
