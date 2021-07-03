from typing import Optional, Type, Any, Dict

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
            headers = headers.replace("Y*", "void*")
            headers = headers.replace("X*", "void*")
            headers = headers.replace("Z*", "void*")
            headers = headers.replace("Vec3*", "void*")
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
        self._originator, self._ptr = UtilFFI.init_ptr(UtilFFI.LIB.X_Create, ptr)

    def __del__(self):
        if self._originator:
            UtilFFI.LIB.X_Destroy(self._ptr)
        self._ptr = None
        self._originator = False

    def is_originator(self):
        return self._originator

    def get_c_pointer(self):
        return self._ptr

    def get_x(self) -> int:
        return UtilFFI.LIB.X_GetX(self._ptr)

    def set_x(self, value: int):
        return UtilFFI.LIB.X_SetX(self._ptr, value)

    def print(self):
        UtilFFI.LIB.X_Print(self._ptr)


class Y(UtilFFI):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self._originator, self._ptr = UtilFFI.init_ptr(UtilFFI.LIB.Y_Create, ptr)

    def __del__(self):
        if self._originator:
            UtilFFI.LIB.Y_Destroy(self._ptr)
        self._ptr = None
        self._originator = False

    def is_originator(self):
        return self._originator

    def get_c_pointer(self):
        return self._ptr

    def get_y(self) -> int:
        return UtilFFI.LIB.Y_GetY(self._ptr)

    def set_y(self, value: int):
        return UtilFFI.LIB.Y_SetY(self._ptr, value)

    def print(self):
        UtilFFI.LIB.Y_Print(self._ptr)


class Z(UtilFFI):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self._originator, self._ptr = UtilFFI.init_ptr(UtilFFI.LIB.Z_Create, ptr)

    def __del__(self):
        if self._originator:
            UtilFFI.LIB.Z_Destroy(self._ptr)
        self._ptr = None
        self._originator = False

    def is_originator(self):
        return self._originator

    def get_c_pointer(self):
        return self._ptr

    def get_z(self) -> int:
        return UtilFFI.LIB.Z_GetZ(self._ptr)

    def set_z(self, value: int):
        return UtilFFI.LIB.Z_SetZ(self._ptr, value)

    def print(self):
        UtilFFI.LIB.Z_Print(self._ptr)


class Vec3(X, Y, Z):
    def __init__(self, ptr=None) -> None:
        UtilFFI.__init__(self)
        self._originator, self._ptr = UtilFFI.init_ptr(UtilFFI.LIB.Vec3_Create, ptr)
        X.__init__(self, UtilFFI.LIB.Vec3_AsX(self._ptr))
        Y.__init__(self, UtilFFI.LIB.Vec3_AsY(self._ptr))
        Z.__init__(self, UtilFFI.LIB.Vec3_AsZ(self._ptr))

    def __del__(self):
        if self._originator:
            UtilFFI.LIB.Vec3_Destroy(self._ptr)
        self._ptr = None
        self._originator = False

    def is_originator(self):
        return self._originator

    def get_c_pointer(self):
        return self._ptr

    def print(self):
        UtilFFI.LIB.Vec3_Print(self._ptr)


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
