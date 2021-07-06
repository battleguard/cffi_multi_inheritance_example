from units import GlobalMethods, X, Y, Z, UnitsFFI, Vec3

def test_zero_y():
    y: Y = Y(y=10)
    assert y.y == 10
    GlobalMethods.zero_y(y)
    assert y.y == 0


def test_zero_vec3():
    vec3: Vec3 = Vec3(x=0, y=10, z=0)
    assert vec3.y == 10
    GlobalMethods.zero_y(vec3)
    assert vec3.y == 0


def test_sum():
    assert GlobalMethods.sum(X(x=10), Y(y=20), Z(z=30)) == 60


def test_sum_vec3():
    vec3: Vec3 = Vec3(x=10, y=20, z=30)
    assert GlobalMethods.sum(vec3, vec3, vec3) == 60
