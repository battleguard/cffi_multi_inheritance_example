from typing import Optional, Type, Any, Dict, Tuple

import cffi
from cffi import FFI


class UtilFFI:
    FFI: Optional[FFI] = None
    LIB: Optional = None

    def __init__(self) -> None:
        if UtilFFI.LIB:
            return
        UtilFFI.FFI = cffi.FFI()
        with open('units.h', 'r') as file:
            headers = file.read()
            # headers = headers.replace("Y*", "void*")
            # headers = headers.replace("X*", "void*")
            # headers = headers.replace("Z*", "void*")
            # headers = headers.replace("Vec3*", "void*")
        UtilFFI.FFI.cdef(headers)
        UtilFFI.LIB = UtilFFI.FFI.dlopen('units.dll')

    @staticmethod
    def init_ptr(function, ptr):
        if ptr is None:
            return True, function()
        return False, ptr


class X(UtilFFI):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self.__originator, self.__ptr = UtilFFI.init_ptr(UtilFFI.LIB.X_Create, ptr)

    def __del__(self):
        if self.__originator:
            UtilFFI.LIB.X_Destroy(self.__ptr)
        self.__ptr = None
        self.__originator = False

    def is_x_originator(self):
        return self.__originator

    def get_x_cptr(self):
        return self.__ptr

    def get_x(self) -> int:
        return UtilFFI.LIB.X_GetX(self.__ptr)

    def set_x(self, value: int):
        return UtilFFI.LIB.X_SetX(self.__ptr, value)

    def print(self):
        UtilFFI.LIB.X_Print(self.__ptr)


class Y(UtilFFI):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self.__originator, self.__ptr = UtilFFI.init_ptr(UtilFFI.LIB.Y_Create, ptr)

    def __del__(self):
        if self.__originator:
            UtilFFI.LIB.Y_Destroy(self.__ptr)
        self.__ptr = None
        self.__originator = False

    def is_y_originator(self):
        return self.__originator

    def get_y_cptr(self):
        return self.__ptr

    def get_y(self) -> int:
        return UtilFFI.LIB.Y_GetY(self.__ptr)

    def set_y(self, value: int):
        return UtilFFI.LIB.Y_SetY(self.__ptr, value)

    def print(self):
        UtilFFI.LIB.Y_Print(self.__ptr)


class Z(UtilFFI):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self.__originator, self.__ptr = UtilFFI.init_ptr(UtilFFI.LIB.Z_Create, ptr)

    def __del__(self):
        if self.__originator:
            UtilFFI.LIB.Z_Destroy(self.__ptr)
        self.__ptr = None
        self.__originator = False

    def is_z_originator(self):
        return self.__originator

    def get_z_cptr(self):
        return self.__ptr

    def get_z(self) -> int:
        return UtilFFI.LIB.Z_GetZ(self.__ptr)

    def set_z(self, value: int):
        return UtilFFI.LIB.Z_SetZ(self.__ptr, value)

    def print(self):
        UtilFFI.LIB.Z_Print(self.__ptr)


class Vec3(X, Y, Z):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self.__originator, self.__ptr = UtilFFI.init_ptr(UtilFFI.LIB.Vec3_Create, ptr)
        X.__init__(self, UtilFFI.LIB.Vec3_AsX(self.__ptr))
        Y.__init__(self, UtilFFI.LIB.Vec3_AsY(self.__ptr))
        Z.__init__(self, UtilFFI.LIB.Vec3_AsZ(self.__ptr))

    def __del__(self):
        if self.__originator:
            UtilFFI.LIB.Vec3_Destroy(self.__ptr)
        self.__ptr = None
        self.__originator = False

    def is_vec3_originator(self):
        return self.__originator

    def get_vec3_cptr(self):
        return self.__ptr

    def get_vec3(self) -> Tuple[int, int, int]:
        buffer_array = UtilFFI.FFI.new("int[3]")
        buffer_ptr = UtilFFI.FFI.cast("int *", buffer_array)
        UtilFFI.LIB.Vec3_GetVec3(self.__ptr, buffer_ptr, buffer_ptr + 1, buffer_ptr + 2)
        vec_tuple = buffer_array[0], buffer_array[1], buffer_array[2]
        return vec_tuple

    def set_vec3(self, x: int, y: int, z: int) -> None:
        UtilFFI.LIB.Vec3_SetVec3(self.__ptr, x, y, z)

    def print(self):
        UtilFFI.LIB.Vec3_Print(self.__ptr)


class GlobalMethods:

    @staticmethod
    def sum(x: X, y: Y, z: Z) -> int:
        print(x.__class__)
        print(y.__class__)
        print(z.__class__)
        temp = UtilFFI.LIB.Units_Sum
        return UtilFFI.LIB.Units_Sum(x.get_x_cptr(), y.get_y_cptr(), z.get_z_cptr())

    @staticmethod
    def zero_y(y: Y):
        UtilFFI.LIB.Units_Zero_Y(y.get_y_cptr())


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
    # test_x()
    # test_y()
    # test_z()
    test_vec3()
    # FFI: FFI = cffi.FFI()
    # with open('units.h', 'r') as file:
    #     headers = file.read()
    #     headers = headers.replace("Y*", "void*")
    #     headers = headers.replace("X*", "void*")
    #     headers = headers.replace("Z*", "void*")
    #     headers = headers.replace("Vec3*", "void*")
    # FFI.cdef(headers)
    # LIB = FFI.dlopen('units.dll')

    # temp = LIB.X_Create()
    # LIB.X_SetX(temp, int(10))
    # print(LIB.X_GetX(temp))

    # vec3 = LIB.Vec3_Create()
    # LIB.Vec3_SetVec3(vec3,10,20,30)
    # LIB.Vec3_Print(vec3)
    # LIB.X_Print(LIB.Vec3_AsX(vec3))
    # LIB.Y_Print(vec3)
    # LIB.Z_Print(vec3)

    # y_ptr = LIB.Vec3_AsY(vec3)
    # z_ptr = LIB.Vec3_AsZ(vec3)
    #
    # print(LIB.X_GetX(vec3))
    # print(LIB.Y_GetY(y_ptr))
    # print(LIB.Z_GetZ(z_ptr))
