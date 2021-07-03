  typedef struct X X;
   typedef struct Y Y;
   typedef struct Z Z;
   typedef struct Vec3 Vec3;
   typedef struct Vec4 Vec4;

   X* X_Create();
   void  X_Destroy(X* self);
   int X_GetX(X* self);
   void X_SetX(X* self, int aX);
   void X_Print(X* self);

   Y* Y_Create();
   void Y_Destroy(Y* self);
   int Y_GetY(Y* self);
   void Y_SetY(Y* self, int aY);

   void Y_Print(Y* self);

   Z* Z_Create();
   void Z_Destroy(Z* self);
   int Z_GetZ(Z* self);
   void Z_SetZ(Z* self, int aZ);
   void Z_Print(Z* self);

   Vec3* Vec3_Create();
   void Vec3_Destroy(Vec3* self);
   X* Vec3_AsX(Vec3* self);
   Y* Vec3_AsY(Vec3* self);
   Z* Vec3_AsZ(Vec3* self);
   void Vec3_GetVec3(Vec3* self, int* aX, int* aY, int* aZ);
   void Vec3_SetVec3(Vec3* self, int aX, int aY, int aZ);
   void Vec3_Print(Vec3* self);
