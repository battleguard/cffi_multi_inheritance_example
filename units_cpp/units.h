#ifndef UNITS_H
#define UNITS_H

extern "C"
{
   typedef struct X X;
   typedef struct Y Y;
   typedef struct Z Z;
   typedef struct Vec3 Vec3;
   typedef struct Vec4 Vec4;

   X* X_X();
   X* X_X_1(int aX);
   void  X_Delete(X* self);
   int X_GetX(X* self);
   void X_SetX(X* self, int aX);
   void X_Print(X* self);
   bool X_IsZero(X* self);

   Y* Y_Y();
   Y* Y_Y_1(int aY);
   void Y_Delete(Y* self);
   int Y_GetY(Y* self);
   void Y_SetY(Y* self, int aY);
   void Y_Print(Y* self);

   Z* Z_Z();
   Z* Z_Z_1(int aZ);
   void Z_Delete(Z* self);
   int Z_GetZ(Z* self);
   void Z_SetZ(Z* self, int aZ);
   void Z_Print(Z* self);

   Vec3* Vec3_Vec3();
   Vec3* Vec3_Vec3_1(int aX, int aY, int aZ);
   void Vec3_Delete(Vec3* self);
   X* Vec3_AsX(Vec3* self);
   Y* Vec3_AsY(Vec3* self);
   Z* Vec3_AsZ(Vec3* self);
   void Vec3_GetVec3(Vec3* self, int* aX, int* aY, int* aZ);
   void Vec3_SetVec3(Vec3* self, int aX, int aY, int aZ);

   Vec4* Vec4_Vec4();
   Vec4* Vec4_Vec4_1(int aX, int aY, int aZ, int aD);
   void  Vec4_Delete(Vec4* self);
   int Vec4_GetD(Vec4* self);
   void Vec4_SetD(Vec4* self, int aD);
   Vec3* Vec4_AsVec3(Vec4* self);

   // static methods
   int Units_Sum(X* aX, Y* aY, Z* aZ);
   void Units_Zero_Y(Y* aY);
}
#endif // UNITS_H
