- find better way to not need to use named arguments when calling non default ctors
- push up to github
- remove need to call UtilFFI()
- better way for handling owning pointer such as from_ptr
- find way to capture std::cout in python for testing print
- find better way to make this code not as duplicate:
```python
        if z is not None:
            WrapperBase.__init__(self, z, c_create=UnitsFFI.LIB.Z_Z_1, ptr=ptr)
        else:
            WrapperBase.__init__(self, c_create=UnitsFFI.LIB.Z_Z, ptr=ptr)
```