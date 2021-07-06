from __future__ import annotations
from typing import Optional, Type, Any, Dict, Tuple, Union, List, Callable
import pathlib
import cffi
from cffi import FFI


class UnitsFFI:
    FFI: Optional[FFI] = None
    LIB: Optional = None

    def __init__(self) -> None:
        if UnitsFFI.LIB:
            return
        cur_file_path = pathlib.Path(__file__).parent.resolve()
        install_path = cur_file_path.joinpath("../units_install")
        units_include_path = install_path.joinpath("include/units/units.h").absolute()
        lib_path = install_path.joinpath("bin/units.dll").absolute()
        UnitsFFI.FFI = cffi.FFI()
        header_str = ""
        with open(units_include_path, 'r') as file:
            for line in file.readlines():
                if line.startswith("   "):
                    header_str += line
        UnitsFFI.FFI.cdef(header_str)
        UnitsFFI.LIB = UnitsFFI.FFI.dlopen(str(lib_path))


class WrapperBase:
    def __init__(self, *args, c_create: UnitsFFI.FFI.CType, ptr: Optional[UnitsFFI.FFI.CType] = None):
        self.ptr_dict: Dict[Type, UnitsFFI.FFI.CType] = {}
        self.__originator = ptr is None
        if self.__originator:
            # if we are originator create pointer and store delete function
            self.ptr_dict[self.__class__] = c_create(*args)
            delete_method_name = f"{self.__class__.__name__}_Delete"
            delete_method_method = UnitsFFI.LIB.__getattr__(delete_method_name)
            self.__delete_func: UnitsFFI.FFI.CType = delete_method_method
        else:
            self.ptr_dict[self.__class__] = ptr
        # create ptrs to base classes to handle multi inheritance
        for base_class in self.__class__.__bases__:
            self.__add_base_class_ptrs(self.__class__, base_class)

    def __add_base_class_ptrs(self, cur_class: type, base_class: type):
        if base_class == WrapperBase:
            return
        # example Vec3_AsX(Vec3* self)
        cast_method_name = f"{cur_class.__name__}_As{base_class.__name__}"
        cast_method = UnitsFFI.LIB.__getattr__(cast_method_name)
        self.ptr_dict[base_class] = cast_method(self.get_c_pointer(cur_class))
        for base_type in base_class.__bases__:
            self.__add_base_class_ptrs(base_class, base_type)

    def __del__(self):
        # only delete pointer if we created the pointer ourselves in the __init__ call
        if self.__originator:
            self.__delete_func(self.ptr_dict[self.__class__])
        self.ptr_dict.clear()
        self.__originator = False

    def get_c_pointer(self, class_type: Type) -> UnitsFFI.FFI.CType:
        return self.ptr_dict[class_type]


class X(WrapperBase):
    def __init__(self, ptr=None, x: Optional[int] = None) -> None:
        if x is not None:
            WrapperBase.__init__(self, x, c_create=UnitsFFI.LIB.X_X_1, ptr=ptr)
        else:
            WrapperBase.__init__(self, c_create=UnitsFFI.LIB.X_X, ptr=ptr)

    @property
    def x(self) -> int:
        return UnitsFFI.LIB.X_GetX(self.get_c_pointer(X))

    @x.setter
    def x(self, value: int):
        UnitsFFI.LIB.X_SetX(self.get_c_pointer(X), value)

    def print(self) -> None:
        UnitsFFI.LIB.X_Print(self.get_c_pointer(X))


class Y(WrapperBase):
    def __init__(self, ptr=None, y: Optional[int] = None) -> None:
        if y is not None:
            WrapperBase.__init__(self, y, c_create=UnitsFFI.LIB.Y_Y_1, ptr=ptr)
        else:
            WrapperBase.__init__(self, c_create=UnitsFFI.LIB.Y_Y, ptr=ptr)

    @property
    def y(self) -> int:
        return UnitsFFI.LIB.Y_GetY(self.get_c_pointer(Y))

    @y.setter
    def y(self, value: int):
        UnitsFFI.LIB.Y_SetY(self.get_c_pointer(Y), value)

    def print(self):
        UnitsFFI.LIB.Y_Print(self.get_c_pointer(Y))


class Z(WrapperBase):
    def __init__(self, ptr=None, z: Optional[int] = None) -> None:
        if z is not None:
            WrapperBase.__init__(self, z, c_create=UnitsFFI.LIB.Z_Z_1, ptr=ptr)
        else:
            WrapperBase.__init__(self, c_create=UnitsFFI.LIB.Z_Z, ptr=ptr)

    @property
    def z(self) -> int:
        return UnitsFFI.LIB.Z_GetZ(self.get_c_pointer(Z))

    @z.setter
    def z(self, value: int):
        UnitsFFI.LIB.Z_SetZ(self.get_c_pointer(Z), value)

    def print(self):
        UnitsFFI.LIB.Z_Print(self.get_c_pointer(Z))


class Vec3(X, Y, Z):

    def __init__(self, ptr=None, x: Optional[int] = None, y: Optional[int] = None, z: Optional[int] = None) -> None:
        if x is not None and y is not None and z is not None:
            WrapperBase.__init__(self, x, y, z, c_create=UnitsFFI.LIB.Vec3_Vec3_1, ptr=ptr)
        else:
            WrapperBase.__init__(self, c_create=UnitsFFI.LIB.Vec3_Vec3, ptr=ptr)

    def get_vec3(self) -> Tuple[int, int, int]:
        buffer_array = UnitsFFI.FFI.new("int[3]")
        buffer_ptr = UnitsFFI.FFI.cast("int *", buffer_array)
        UnitsFFI.LIB.Vec3_GetVec3(self.get_c_pointer(Vec3), buffer_ptr, buffer_ptr + 1, buffer_ptr + 2)
        vec_tuple = buffer_array[0], buffer_array[1], buffer_array[2]
        return vec_tuple

    def set_vec3(self, x: int, y: int, z: int) -> None:
        UnitsFFI.LIB.Vec3_SetVec3(self.get_c_pointer(Vec3), x, y, z)

    vec3 = property(get_vec3)


class Vec4(Vec3):
    def __init__(self, ptr=None) -> None:
        WrapperBase.__init__(self, c_create=UnitsFFI.LIB.Vec4_Vec4, ptr=ptr)

    def get_d(self) -> int:
        return UnitsFFI.LIB.Vec4_GetD(self.get_c_pointer(Vec4))

    def set_d(self, value: int):
        UnitsFFI.LIB.Vec4_SetD(self.get_c_pointer(Vec4), value)


class GlobalMethods:

    @staticmethod
    def sum(x: X, y: Y, z: Z) -> int:
        return UnitsFFI.LIB.Units_Sum(x.get_c_pointer(X), y.get_c_pointer(Y), z.get_c_pointer(Z))

    @staticmethod
    def zero_y(y: Y):
        UnitsFFI.LIB.Units_Zero_Y(y.get_c_pointer(Y))
