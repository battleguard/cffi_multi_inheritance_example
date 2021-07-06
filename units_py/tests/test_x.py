from _cffi_backend import CType, _CDataBase

from units import UnitsFFI, X

UnitsFFI()


def test_x_ctor_default():
    ctor1: X = X()
    assert ctor1.x == 0


def test_x_ctor_1():
    ctor1: X = X(x=10)
    assert ctor1.x == 10


def test_x_property():
    x_object: X = X(x=10)
    x_object.x = 5
    assert x_object.x == 5
    x_object.x = -10
    assert x_object.x == -10


def test_owning_ptr_ctor():
    original: X = X(x=10)
    shallow_copy: X = X(ptr=original.get_c_pointer(X))
    assert original.get_c_pointer(X) == shallow_copy.get_c_pointer(X)
    assert shallow_copy.x == 10
    original.x = 5
    assert shallow_copy.x == 5
    shallow_copy.x = -10
    assert original.x == -10


def test_x_print():
    X(x=10).print()


def test_reflection_on_ffi_methods():
    UnitsFFI()
    import ctypes
    from ctypes import cdll, Structure, c_int, c_double, c_uint

    method: _CDataBase = UnitsFFI.LIB.__getattr__("Vec3_Vec3_1")
    method_type: CType = UnitsFFI.FFI.typeof(method)
    # print(method_type.cname)
    # print(method_type.args)

    # import inspect
    # method_params: FullArgSpec = inspect.getfullargspec(method)
    # print(method_params)
