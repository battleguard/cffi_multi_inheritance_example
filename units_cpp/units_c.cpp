#include "units.h"
#include "units.hpp"


X* X_X() { return new X(); }
X* X_X_1(int aX) { return new X(aX); }
void X_Delete(X* self) { delete self; }
int X_GetX(X* self) { return self->mX; }
void X_SetX(X* self, int aX) { self->mX = aX; }
void X_Print(X* self) { self->Print(); }


Y* Y_Y() { return new Y(); }
Y* Y_Y_1(int aY) { return new Y(aY); }
void Y_Delete(Y* self) { delete self; }
int Y_GetY(Y* self) { return self->mY; }
void Y_SetY(Y* self, int aY) { self->mY = aY; }
void Y_Print(Y* self) { self->Print(); }


Z* Z_Z() { return new Z(); }
Z* Z_Z_1(int aZ) { return new Z(aZ); }
void Z_Delete(Z* self) { delete self; }
int Z_GetZ(Z* self) { return self->mZ; }
void Z_SetZ(Z* self, int aZ) { self->mZ = aZ; }
void Z_Print(Z* self) { self->Print(); }


Vec3* Vec3_Vec3() { return new Vec3(); }
Vec3* Vec3_Vec3_1(int aX, int aY, int aZ) { return new Vec3(aX, aY, aZ); }
void Vec3_Delete(Vec3* self) { delete self; }
void Vec3_Print(Vec3* self) { self->Print(); }
X* Vec3_AsX(Vec3* self) { return static_cast<X*>(self); }
Y* Vec3_AsY(Vec3* self) { return static_cast<Y*>(self);}
Z* Vec3_AsZ(Vec3* self) { return static_cast<Z*>(self);}
void Vec3_GetVec3(Vec3* self, int* aX, int* aY, int* aZ)
{
   *aX = self->mX;
   *aY = self->mY;
   *aZ = self->mZ;
}
void Vec3_SetVec3(Vec3* self, int aX, int aY, int aZ)
{
   self->mX = aX;
   self->mY = aY;
   self->mZ = aZ;
}

Vec4* Vec4_Vec4() { return new Vec4(); }
Vec4* Vec4_Vec4_1(int aX, int aY, int aZ, int aD)
{
   return new Vec4(aX, aY, aZ, aD);
}
void  Vec4_Delete(Vec4* self) { delete self; }
int Vec4_GetD(Vec4* self) { return self->mD; }
void Vec4_SetD(Vec4* self, int aD) { self->mD = aD; }
Vec3* Vec4_AsVec3(Vec4* self) { return static_cast<Vec3*>(self); }


int Units_Sum(X* aX, Y* aY, Z* aZ)
{
   return Sum(*aX, *aY, *aZ);
}

void Units_Zero_Y(Y* aValue)
{
   return Zero_Y(*aValue);
}
