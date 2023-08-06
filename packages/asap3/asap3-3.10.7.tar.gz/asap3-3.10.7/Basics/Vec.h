// -*- C++ -*-
// Vec.h: Vectors in three-dimensional space, i.e. three doubles.
//
// Copyright (C) 2001-2011 Jakob Schiotz and Center for Individual
// Nanoparticle Functionality, Department of Physics, Technical
// University of Denmark.  Email: schiotz@fysik.dtu.dk
//
// This file is part of Asap version 3.
// Asap is released under the GNU Lesser Public License (LGPL) version 3.
// However, the parts of Asap distributed within the OpenKIM project
// (including this file) are also released under the Common Development
// and Distribution License (CDDL) version 1.0.
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// version 3 as published by the Free Software Foundation.  Permission
// to use other versions of the GNU Lesser General Public License may
// granted by Jakob Schiotz or the head of department of the
// Department of Physics, Technical University of Denmark, as
// described in section 14 of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// and the GNU Lesser Public License along with this program.  If not,
// see <http://www.gnu.org/licenses/>.

#ifndef _VEC_H
#define _VEC_H

#include "Asap.h"
#include <iostream>
using std::istream;
using std::ostream;

namespace ASAPSPACE {

/// A 3-vector useful for postions etc.

/// The only data is the three positions (and there are no virtual
/// functions), so the memory layout of an array of Vecs will be x0,
/// y0, z0, x1, y1, z1, x2, ...
///
/// Almost all operations are inline for speed.

class Vec
{
public:
  /// Dummy constructor needed by STL containers.
  Vec() {};
  /// Construct a 3-vector from three doubles.
  Vec(double x0, double x1, double x2);
  /// Dot product
  double operator*(const Vec& v) const;
  /// Multiplication with scalar
  Vec operator*(const double& s) const;
  friend Vec operator*(const double &s, const Vec v);
  /// Division with scalar
  Vec operator/(const double& s) const;
  /// Add two Vecs
  Vec operator+(const Vec& v) const;
  /// Subtract two Vecs
  Vec operator-(const Vec& v) const;
  /// Unary minus
  Vec operator-() const;
  /// Add a Vec to this one.
  Vec& operator+=(const Vec& v);
  /// Subtract a vec from this one.
  Vec& operator-=(const Vec& v);
  /// Multiply this vec with a scalar
  Vec& operator*=(double s);
  /// Divide this Vec with a scalar.
  Vec& operator/=(double s);
  /// Vec equality (bitwise!)
  bool operator==(const Vec &v) const;
  /// Vec inequality (bitwise!)
  bool operator!=(const Vec &v) const;  
  /// const indexing
  double operator[](int n) const;
  /// Non-const indexing
  double& operator[](int n);
  /// Cross product of two Vecs.
  friend Vec Cross(const Vec& v1, const Vec& v2);
  /// The length of a Vec
  friend double Length2(const Vec& v);
  /// Increment y with a times x.
  friend void Vaxpy(double a, const Vec& x, Vec& y);
  /// Print a Vec
  friend ostream& operator<<(ostream& out, const Vec& v);
  /// Read a Vec
  friend istream& operator>>(istream& in, Vec& v);
public:
  ///< The actual data.
  // Using an array would hinder vectorization by the Intel compiler.
  double x, y, z;
};

inline Vec::Vec(double x0, double x1, double x2)
{
  x = x0;
  y = x1;
  z = x2;
}

inline double Vec::operator*(const Vec& v) const
{
  return x * v.x + y * v.y + z * v.z;
}

inline Vec Vec::operator*(const double& s) const
{
  return Vec(s * x, s * y, s * z);
}

inline Vec operator*(const double &s, const Vec v)
{
  return Vec(s * v.x, s * v.y, s * v.z);
}

inline Vec Vec::operator/(const double& s) const
{
  return Vec(x / s, y / s, z / s);
}

inline Vec Vec::operator+(const Vec& v) const
{
  return Vec(x + v.x, y + v.y, z + v.z);
}

inline Vec Vec::operator-(const Vec& v) const
{
  return Vec(x - v.x, y - v.y, z - v.z);
}

inline Vec Vec::operator-() const
{
  return Vec(-x, -y, -z);
}

inline Vec& Vec::operator+=(const Vec& v)
{
  x += v.x; y += v.y; z += v.z;
  return *this;
}

inline Vec& Vec::operator-=(const Vec& v)
{
  x -= v.x; y -= v.y; z -= v.z;
  return *this;
}

inline Vec& Vec::operator*=(double s)
{
  x *= s; y *= s; z *= s;
  return *this;
}

inline Vec& Vec::operator/=(double s)
{
  x /= s; y /= s; z /= s;
  return *this;
}

inline bool Vec::operator==(const Vec &v) const
{
  return (x == v.x) && (y == v.y) && (z == v.z);
}

inline bool Vec::operator!=(const Vec &v) const
{
  return !(*this == v);
}
    
inline double Vec::operator[](int n) const
{
  return (&x)[n];
}

inline double& Vec::operator[](int n)
{
  return (&x)[n];
}

inline Vec Cross(const Vec& v1, const Vec& v2)
{
  return Vec(v1.y * v2.z - v1.z * v2.y,
             v1.z * v2.x - v1.x * v2.z,
             v1.x * v2.y - v1.y * v2.x);
}

inline void Vaxpy(double a, const Vec& x, Vec& y)
{
  y.x += a * x.x;
  y.y += a * x.y;
  y.z += a * x.z;
}

inline double Length2(const Vec& v)
{
  return v.x * v.x + v.y * v.y + v.z * v.z;
}

} // end namespace

#endif // _VEC_H

