from __future__ import annotations
from typing import Optional, Type, Any, Dict, Tuple, Union, List, Callable
import pathlib
import cffi
from cffi import FFI


class UtilFFI:
    FFI: Optional[FFI] = None
    LIB: Optional = None

    def __init__(self) -> None:
        if UtilFFI.LIB:
            return
        install_path = pathlib.Path("../build/wsf_install")
        units_include_path = install_path.joinpath("include/units/units.h").absolute()
        lib_path = install_path.joinpath("bin/units.dll").absolute()
        UtilFFI.FFI = cffi.FFI()
        header_str = ""
        with open(units_include_path, 'r') as file:
            for line in file.readlines():
                if line.startswith("   "):
                    header_str += line
        UtilFFI.FFI.cdef(header_str)
        UtilFFI.LIB = UtilFFI.FFI.dlopen(str(lib_path))


class WrapperBase:
    def __init__(self, c_create: Callable, delete_func: Callable, ptr=None):
        self.ptr_dict: Dict[Type, Any] = {}
        self.__originator = ptr is None
        if self.__originator:
            # if we are originator create pointer and store delete function
            self.ptr_dict[self.__class__] = c_create()
            self.__delete_func: Callable = delete_func
        else:
            self.ptr_dict[self.__class__] = ptr

    def __del__(self):
        # only delete pointer if we created the pointer ourselves in the __init__ call
        if self.__originator:
            self.__delete_func(self.ptr_dict[self.__class__])
        self.ptr_dict.clear()
        self.__originator = False

    def get_c_pointer(self, class_type: Type):
        return self.ptr_dict[class_type]


class X(WrapperBase):
    def __init__(self, ptr=None) -> None:
        WrapperBase.__init__(self, UtilFFI.LIB.X_Create, UtilFFI.LIB.X_Destroy, ptr)

    def get_x(self) -> int:
        return UtilFFI.LIB.X_GetX(self.get_c_pointer(X))

    def set_x(self, value: int):
        return UtilFFI.LIB.X_SetX(self.get_c_pointer(X), value)

    def print(self):
        UtilFFI.LIB.X_Print(self.get_c_pointer(X))


class Y(WrapperBase):
    def __init__(self, ptr=None) -> None:
        WrapperBase.__init__(self, UtilFFI.LIB.Y_Create, UtilFFI.LIB.Y_Destroy, ptr)

    def get_y(self) -> int:
        return UtilFFI.LIB.Y_GetY(self.get_c_pointer(Y))

    def set_y(self, value: int):
        return UtilFFI.LIB.Y_SetY(self.get_c_pointer(Y), value)

    def print(self):
        UtilFFI.LIB.Y_Print(self.get_c_pointer(Y))


class Z(WrapperBase):
    def __init__(self, ptr=None) -> None:
        WrapperBase.__init__(self, UtilFFI.LIB.Z_Create, UtilFFI.LIB.Z_Destroy, ptr)

    def get_z(self) -> int:
        return UtilFFI.LIB.Z_GetZ(self.get_c_pointer(Z))

    def set_z(self, value: int):
        return UtilFFI.LIB.Z_SetZ(self.get_c_pointer(Z), value)

    def print(self):
        UtilFFI.LIB.Z_Print(self.get_c_pointer(Z))


class Vec3(X, Y, Z):

    def __init__(self, ptr=None) -> None:
        WrapperBase.__init__(self, UtilFFI.LIB.Vec3_Create, UtilFFI.LIB.Vec3_Destroy, ptr)
        self.ptr_dict[X] = UtilFFI.LIB.Vec3_AsX(self.get_c_pointer(Vec3))
        self.ptr_dict[Y] = UtilFFI.LIB.Vec3_AsY(self.get_c_pointer(Vec3))
        self.ptr_dict[Z] = UtilFFI.LIB.Vec3_AsZ(self.get_c_pointer(Vec3))

    def get_vec3(self) -> Tuple[int, int, int]:
        buffer_array = UtilFFI.FFI.new("int[3]")
        buffer_ptr = UtilFFI.FFI.cast("int *", buffer_array)
        UtilFFI.LIB.Vec3_GetVec3(self.get_c_pointer(Vec3), buffer_ptr, buffer_ptr + 1, buffer_ptr + 2)
        vec_tuple = buffer_array[0], buffer_array[1], buffer_array[2]
        return vec_tuple

    def set_vec3(self, x: int, y: int, z: int) -> None:
        UtilFFI.LIB.Vec3_SetVec3(self.get_c_pointer(Vec3), x, y, z)

    def print(self):
        UtilFFI.LIB.Vec3_Print(self.get_c_pointer(Vec3))


class GlobalMethods:

    @staticmethod
    def sum(x: X, y: Y, z: Z) -> int:
        print(x.__class__)
        print(y.__class__)
        print(z.__class__)
        return UtilFFI.LIB.Units_Sum(x.get_c_pointer(X), y.get_c_pointer(Y), z.get_c_pointer(Z))

    @staticmethod
    def zero_y(y: Y):
        UtilFFI.LIB.Units_Zero_Y(y.get_c_pointer(Y))


def test_y():
    test_y = Y()
    test_y.set_y(20)
    print(test_y.get_y())
    test_y.print()


def test_x():
    testX = X()
    testX.set_x(10)
    print(testX.get_x())
    testX.print()


def test_z():
    test_z = Z()
    test_z.set_z(30)
    print(test_z.get_z())
    test_z.print()


def test_vec3():
    temp_vec3 = Vec3()
    temp_vec3.print()
    temp_vec3.set_x(10)
    temp_vec3.set_y(20)
    temp_vec3.set_z(30)
    print(temp_vec3.get_x())
    print(temp_vec3.get_y())
    print(temp_vec3.get_z())
    temp_vec3.set_vec3(3, 4, 5)
    print(temp_vec3.get_vec3())
    print(temp_vec3.get_x())
    print(temp_vec3.get_y())
    print(temp_vec3.get_z())
    temp_vec3.print()
    result: int = GlobalMethods.sum(temp_vec3, temp_vec3, temp_vec3)
    print("Sum: ", result)
    GlobalMethods.zero_y(temp_vec3)
    temp_vec3.print()


if __name__ == '__main__':
    UtilFFI()
    temp: Vec3 = Vec3()
    temp.set_vec3(10, 20, 30)
    GlobalMethods.zero_y(temp)
    print(temp.get_vec3())
    print(temp.get_c_pointer(class_type=Vec3))
    print(temp.get_c_pointer(class_type=X))
    print(temp.get_c_pointer(class_type=Y))
    print(temp.get_c_pointer(class_type=Z))
    test_x()
    test_y()
    test_z()
    test_vec3()
