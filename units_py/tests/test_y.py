from _cffi_backend import CType

from units import UnitsFFI, Y

def test_y_ctor_default():
    ctor1: Y = Y()
    assert ctor1.y == 0


def test_x_ctor_1():
    ctor1: Y = Y(y=10)
    assert ctor1.y == 10
#
#
# def test_x_property():
#     x_object: X = X(x=10)
#     x_object.x = 5
#     assert x_object.x == 5
#     x_object.x = -10
#     assert x_object.x == -10
#
#
# def test_owning_ptr_ctor():
#     original: X = X(x=10)
#     shallow_copy: X = X(ptr=original.get_c_pointer(X))
#     assert original.get_c_pointer(X) == shallow_copy.get_c_pointer(X)
#     assert shallow_copy.x == 10
#     original.x = 5
#     assert shallow_copy.x == 5
#     shallow_copy.x = -10
#     assert original.x == -10