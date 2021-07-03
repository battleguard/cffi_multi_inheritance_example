#include "units.h"
#include "units.hpp"


X* X_Create() { return new X(); }
void X_Destroy(X* self) { delete self; }
int X_GetX(X* self) { return self->mX; }
void X_SetX(X* self, int aX) { self->mX = aX; }
void X_Print(X* self) { self->Print(); }


Y* Y_Create() { return new Y(); }
void Y_Destroy(Y* self) { delete self; }
int Y_GetY(Y* self) { return self->mY; }
void Y_SetY(Y* self, int aY) { self->mY = aY; }
void Y_Print(Y* self) { self->Print(); }


Z* Z_Create() { return new Z(); }
void Z_Destroy(Z* self) { delete self; }
int Z_GetZ(Z* self) { return self->mZ; }
void Z_SetZ(Z* self, int aZ) { self->mZ = aZ; }
void Z_Print(Z* self) { self->Print(); }


Vec3* Vec3_Create() { return new Vec3(); }
void Vec3_Destroy(Vec3* self) { delete self; }
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

int Units_Sum(X* aX, Y* aY, Z* aZ)
{
   return Sum(*aX, *aY, *aZ);
}

void Units_Zero_Y(Y* aValue)
{
   return Zero_Y(*aValue);
}
