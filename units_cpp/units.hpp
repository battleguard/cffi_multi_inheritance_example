#ifndef UNITS_HPP
#define UNITS_HPP

#include <iostream>

struct X
{
   virtual ~X() = default;
   int mX{0};
   virtual void Print() { std::cout << "X::mX=" << mX << std::endl; }
};

struct Y
{
   virtual ~Y() = default;
   int mY{ 0 };
   virtual void Print() { std::cout << "Y::mY=" << mY << std::endl; }
};

struct Z
{
   virtual ~Z() = default;
   int mZ{ 0 };
   virtual void Print() { std::cout << "Y::mZ=" << mZ << std::endl; }
};

struct Vec3 :  X, Y, Z
{
   Vec3(int aX, int aY, int aZ)
   {
      mX = aX;
      mY = aY;
      mZ = aZ;
   }

   Vec3() = default;

   void Print() override
   {
      std::cout << "Vec3::mX=" << mX << " mY=" << mY << " mZ=" << mZ << std::endl;
   }
};

// testing static functions and passing in base classes
inline int Sum(const X& aX, const Y& aY, const Z& aZ)
{
   return aX.mX + aY.mY + aZ.mZ;
}

inline void Zero_Y(Y& aValue)
{
   aValue.mY = 0;
}


// struct Vec4 : Vec3
// {
//    Vec4(int aX, int aY, int aZ, int aD)
//       : Vec3(aX, aY, aZ), mD(aD) 
//    {
//       mZ = aZ;
//    }
//    int mD{ 0 };
//    void Print() override
//    {
//       std::cout << "Vec4::mX=" << mX << " mY=" << mY << " mZ=" << mZ
//                 << " mD=" << mD << "\n";
//    }
// };

#endif // UNITS_HPP