from units import UnitsFFI, Vec3, Z


def test_vec3_default_ctor():
    default_ctor: Vec3 = Vec3()
    assert default_ctor.x == 0
    assert default_ctor.y == 0
    assert default_ctor.z == 0
    assert default_ctor.get_vec3() == (0, 0, 0)


def test_vec3_default_ctor2():
    ctor_1: Vec3 = Vec3(x=10, y=20, z=30)
    assert ctor_1.x == 10
    assert ctor_1.y == 20
    assert ctor_1.z == 30
    assert ctor_1.vec3 == (10, 20, 30)


def test_vec3_default_ctor2_test2():
    ctor_1: Vec3 = Vec3(x=0, y=10, z=0)
    assert ctor_1.x == 0
    assert ctor_1.y == 10
    assert ctor_1.z == 0
    assert ctor_1.vec3 == (0, 10, 0)


def test_vec3_setter():
    vec3: Vec3 = Vec3()
    vec3.set_vec3(10, 20, 30)
    assert vec3.vec3 == (10, 20, 30)


def test_x_y_z_setters():
    vec3: Vec3 = Vec3()
    vec3.x = 10
    vec3.y = 20
    vec3.z = 30
    assert vec3.vec3 == (10, 20, 30)


def test_casting_down():
    vec3: Vec3 = Vec3(x=10, y=20, z=30)
    z: Z = vec3
    assert z.z == 30
    z_shallow: Z = Z(ptr=vec3.get_c_pointer(Z))
    assert z_shallow.z == 30
    vec3.z = 10
    assert z_shallow.z == 10
