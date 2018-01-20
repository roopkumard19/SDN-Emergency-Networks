
# -*- coding: utf-8 -*-

u'''N-vector-based ellipsoidal geodetic (lat-/longitude) and cartesion
(x/y/z) classes L{LatLon}, L{Ned}, L{Nvector} and L{Cartesian} and
functions L{meanOf} and L{toNed}.

Pure Python implementation of n-vector-based geodetic (lat-/longitude)
methods by I{(C) Chris Veness 2011-2016} published under the same MIT
Licence**, see U{http://www.movable-type.co.uk/scripts/latlong-vectors.html}'

These classes and functions work with: (a) geodesic (polar) lat-/longitude
points on the earth's surface and (b) 3-D vectors used as n-vectors
representing points on the earth's surface or vectors normal to the plane
of a great circle.

See Kenneth Gade, "A Non-singular Horizontal Position Representation",
The Journal of Navigation (2010), vol 63, nr 3, pp 395-417.  Also at
U{http://www.navlab.net/Publications/A_Nonsingular_Horizontal_Position_Representation.pdf}.

@newfield example: Example, Examples
'''

from datum import Datum, Datums
from dms import F_D, toDMS
from ellipsoidalBase import CartesianBase, LatLonEllipsoidalBase
from nvector import NorthPole, LatLonNvectorBase, \
                    Nvector as NvectorBase, sumOf
from utils import EPS, degrees90, degrees360, cbrt, fdot, fStr, \
                  hypot, hypot3, radians
from vector3d import Vector3d

from math import asin, atan2, cos, sin, sqrt

# all public contants, classes and functions
__all__ = ('Cartesian', 'LatLon', 'Ned', 'Nvector',  # classes
           'meanOf', 'toNed')  # functions
__version__ = '18.01.14'


class LatLon(LatLonNvectorBase, LatLonEllipsoidalBase):
    '''An n-vector-based ellipsoidal L{LatLon} point.

       @example:

       >>> from ellipsoidalNvector import LatLon
       >>> p = LatLon(52.205, 0.119)  # height=0, datum=Datums.WGS84
    '''
    _Nv  = None  #: (INTERNAL) Cache toNvector (L{Nvector}).
#   _v3d = None  #: (INTERNAL) Cache toVector3d (L{Vector3d}).
    _r3  = None  #: (INTERNAL) Cache _rotation3 (3-Tuple L{Nvector}s).

    def _rotation3(self):
        '''(INTERNAL) Build the rotation matrix from n-vector
           coordinate frame axes.
        '''
        if self._r3 is None:
            nv = self.toNvector()  # local (n-vector) coordinate frame

            d = nv.negate()  # down (opposite to n-vector)
            e = NorthPole.cross(nv, raiser='pole').unit()  # east (pointing perpendicular to the plane)
            n = e.cross(d)  # north (by right hand rule)

            self._r3 = n, e, d  # matrix rows
        return self._r3

    def _update(self, updated):
        '''(INTERNAL) Clear caches if updated.
        '''
        if updated:  # reset caches
            if self._Nv:
                self._Nv._fromll = None
                self._Nv = None
            self._r3 = None
            LatLonNvectorBase._update(self, updated)
            LatLonEllipsoidalBase._update(self, updated)

#     def crossTrackDistanceTo(self, start, end, radius=R_M):
#         '''Return the (signed) distance from this point to the great
#            circle defined by a start point and an end point or bearing.
#
#            @param start: Start point of great circle path (L{LatLon}).
#            @param end: End point of great circle path (L{LatLon}) or
#                        initial bearing (in compass degrees) at the
#                        start point.
#            @keyword radius: Optional, mean earth radius (meter).
#
#            @return: Distance to great circle, negative if to left or
#                     positive if to right of path (scalar).
#
#            @raise TypeError: The start or end point is not L{LatLon}.
#
#            @example:
#
#            >>> p = LatLon(53.2611, -0.7972)
#
#            >>> s = LatLon(53.3206, -1.7297)
#            >>> b = 96.0
#            >>> d = p.crossTrackDistanceTo(s, b)  # -305.7
#
#            >>> e = LatLon(53.1887, 0.1334)
#            >>> d = p.crossTrackDistanceTo(s, e)  # -307.5
#         '''
#         self.others(start, name='start')
#
#         if isscalar(end):  # gc from point and bearing
#             gc = start.greatCircle(end)
#         else:  # gc by two points
#             gc = start.toNvector().cross(end.toNvector())
#
#         # (signed) angle between point and gc normal vector
#         v = self.toNvector()
#         a = gc.angleTo(v, vSign=v.cross(gc))
#         if a < 0:
#             a = -PI_2 - a
#         else:
#             a =  PI_2 - a
#         return a * float(radius)

    def deltaTo(self, other):
        '''Calculate the NED delta from this to an other point.

           The delta is returned as a North-East-Down (NED) vector.

           Note, this is a linear delta, unrelated to a geodesic
           on the ellipsoid.  The points need not be defined on
           the same datum.

           @param other: The other point (L{LatLon}).

           @return: Delta of this point (L{Ned}).

           @raise TypeError: The other point is not L{LatLon}.

           @raise ValueError: If ellipsoids are incompatible.

           @example:

           >>> a = LatLon(49.66618, 3.45063)
           >>> b = LatLon(48.88667, 2.37472)
           >>> delta = a.deltaTo(b)  # [N:-86126, E:-78900, D:1069]
           >>> d = delta.length  # 116807.681 m
           >>> b = delta.bearing  # 222.493°
           >>> e = delta.elevation  # -0.5245°
        '''
        self.ellipsoids(other)  # throws TypeError and ValueError

        n, e, d = self._rotation3()
        # get delta in cartesian frame
        dc = other.toCartesian().minus(self.toCartesian())
        # rotate dc to get delta in n-vector reference
        # frame using the rotation matrix row vectors
        return Ned(dc.dot(n), dc.dot(e), dc.dot(d))

#     def destination(self, distance, bearing, radius=R_M, height=None):
#         '''Return the destination point after traveling from this
#            point the given distance on the given initial bearing.
#
#            @param distance: Distance traveled (same units as the
#                             given earth radius.
#            @param bearing: Initial bearing (compass degrees).
#            @keyword radius: Optional, mean earth radius (meter).
#            @keyword height: Optional height at destination point,
#                             overriding default (meter or same unit
#                             as radius).
#
#            @return: Destination point (L{LatLon}).
#
#            @example:
#
#            >>> p = LatLon(51.4778, -0.0015)
#            >>> q = p.destination(7794, 300.7)
#            >>> q.toStr()  # '51.5135°N, 000.0983°W' ?
#         '''
#         r = float(distance) / float(radius)  # angular distance in radians
#         # great circle by starting from this point on given bearing
#         gc = self.greatCircle(bearing)
#
#         v1 = self.toNvector()
#         x = v1.times(cos(r))  # component of v2 parallel to v1
#         y = gc.cross(v1).times(sin(r))  # component of v2 perpendicular to v1
#
#         v2 = x.plus(y).unit()
#         return v2.toLatLon(height=self.height if height is None else height)

    def destinationNed(self, delta):
        '''Calculate the destination point using the supplied NED delta
           from this point.

           @param delta: Delta from this to the other point in the
                         local tangent plane (LTP) of this point (L{Ned}).

           @return: Destination point (L{Cartesian}).

           @raise TypeError: The delta is not L{Ned}.

           @example:

           >>> a = LatLon(49.66618, 3.45063)
           >>> delta = toNed(116807.681, 222.493, -0.5245)  # [N:-86126, E:-78900, D:1069]
           >>> b = a.destinationNed(delta)  # 48.88667°N, 002.37472°E

           @JSname: I{destinationPoint}.
        '''
        if not isinstance(delta, Ned):
            raise TypeError('type(%s) not %s.%s' % ('delta',
                             Ned.__module__, Ned.__name__))

        n, e, d = self._rotation3()
        # convert NED delta to standard Vector3d in coordinate frame of n-vector
        dn = delta.toVector3d().to3xyz()
        # rotate dn to get delta in cartesian (ECEF) coordinate
        # reference frame using the rotation matrix column vectors
        dc = Cartesian(fdot(dn, n.x, e.x, d.x),
                       fdot(dn, n.y, e.y, d.y),
                       fdot(dn, n.z, e.z, d.z))

        # apply (cartesian) delta to this Cartesian to
        # obtain destination point as cartesian
        v = self.toCartesian().plus(dc)  # the plus() gives a plain vector

        return v.toLatLon(datum=self.datum, LatLon=self.classof)  # Cartesian(v.x, v.y, v.z).toLatLon(...)

#     def distanceTo(self, other):
#         '''Compute the distance from this to an other point.
#
#            @param other: The other point (L{LatLon}).
#
#            @return: Distance (meter).
#
#            @raise TypeError: The other point is not L{LatLon}.
#
#            @example:
#
#            >>> p = LatLon(52.205, 0.119)
#            >>> q = LatLon(48.857, 2.351);
#            >>> d = p.distanceTo(q)  # 404300
#         '''
#         self.others(other)
#
#         v1 = self.toNvector()
#         v2 = other.toNvector()
#         return v1.angleTo(v2) * self.datum.ellipsoid.R

#     def distanceTo(self, other, radius=R_M):
#         '''Compute the distance from this to an other point.
#
#            @param other: The other point (L{LatLon}).
#            @keyword radius: Optional, mean earth radius (meter).
#
#            @return: Distance (meter, same units as I{radius}).
#
#            @raise TypeError: The other point is not L{LatLon}.
#
#            @example:
#
#            >>> p = LatLon(52.205, 0.119)
#            >>> q = LatLon(48.857, 2.351);
#            >>> d = p.distanceTo(q)  # 404300
#         '''
#         self.others(other)
#
#         v1 = self.toVector3d()
#         v2 = other.toVector3d()
#         return v1.angleTo(v2) * float(radius)

    def equals(self, other, eps=None):
        '''Compare this point with an other point.

           @param other: The other point (L{LatLon}).
           @keyword eps: Optional margin (float).

           @return: True if points are identical, including
                    datum and height (bool).

           @raise TypeError: The other point is not L{LatLon}.

           @example:

           >>> p = LatLon(52.205, 0.119)
           >>> q = LatLon(52.205, 0.119)
           >>> e = p.equals(q)  # True
        '''
        return LatLonEllipsoidalBase.equals(self, other, eps=eps) and \
                            abs(self.height - other.height) < EPS and \
                            self.datum == other.datum

#     def greatCircle(self, bearing):
#         '''Return the great circle heading on the given bearing
#            from this point.
#
#            Direction of vector is such that initial bearing vector
#            b = c × p, where p is representing this point.
#
#            @param bearing: Bearing from this point (compass degrees).
#
#            @return: N-vector representing great circle (L{Nvector}).
#
#            @example:
#
#            >>> p = LatLon(53.3206, -1.7297)
#            >>> g = p.greatCircle(96.0)
#            >>> g.toStr()  # '(-0.794, 0.129, 0.594)'
#         '''
#         b, a = self.to2ab()
#         c = radians(bearing)
#
#         ca, sa = cos(a), sin(a)
#         cb, sb = cos(b), sin(b)
#         cc, sc = cos(c), sin(c)
#
#         return Nvector(sa * cc - ca * sb * sc,
#                       -ca * cc - sa * sb * sc,
#                        cb * sc)

#     def initialBearingTo(self, other):
#         '''Return the initial bearing (forward azimuth) from this
#            to an other point.
#
#            @param other: The other point (L{LatLon}).
#
#            @return: Initial bearing in compass degrees (degrees360).
#
#            @raise TypeError: The other point is not L{LatLon}.
#
#            @example:
#
#            >>> p1 = LatLon(52.205, 0.119)
#            >>> p2 = LatLon(48.857, 2.351)
#            >>> b = p1.bearingTo(p2)  # 156.2
#
#            @JSname: I{bearingTo}.
#         '''
#         self.others(other)
#
#         v1 = self.toNvector()
#         v2 = other.toNvector()
#
#         gc1 = v1.cross(v2)  # gc through v1 & v2
#         gc2 = v1.cross(_NP3)  # gc through v1 & North pole
#
#         # bearing is (signed) angle between gc1 & gc2
#         return degrees360(gc1.angleTo(gc2, vSign=v1))
#
#     bearingTo = initialBearingTo  # for backward compatibility

    def intermediateTo(self, other, fraction, height=None):
        '''Return the point at given fraction between this and
           an other point.

           @param other: The other point (L{LatLon}).
           @param fraction: Fraction between both points ranging from
                            0 = this point to 1 = other point (float).
           @keyword height: Optional height, overriding the fractional
                            height (meter).

           @return: Intermediate point (L{LatLon}).

           @raise TypeError: The other point is not L{LatLon}.

           @example:

           >>> p = LatLon(52.205, 0.119)
           >>> q = LatLon(48.857, 2.351)
           >>> p = p.intermediateTo(q, 0.25)  # 51.3721°N, 000.7073°E

           @JSname: I{intermediatePointTo}.
        '''
        self.others(other)

        i = other.toNvector().times(fraction).plus(
             self.toNvector().times(1 - fraction))

        if height is None:
            h = self._havg(other, f=fraction)
        else:
            h = height
        return i.toLatLon(height=h, LatLon=self.classof)  # Nvector(i.x, i.y, i.z).toLatLon(...)

    def toCartesian(self):
        '''Convert this (geodetic) point to (geocentric x/y/z)
           cartesian coordinates.

           @return: Cartesian instance (L{Cartesian} x/y/z in meter
                    from the earth center).
        '''
        x, y, z = self.to3xyz()  # ellipsoidalBase.LatLonEllipsoidalBase
        return Cartesian(x, y, z)  # this ellipsoidalNvector Cartesian

    def toNvector(self):  # note: replicated in LatLonNvectorSpherical
        '''Convert this point to an L{Nvector} normal to the
           earth's surface.

           @return: N-vector representing this point (L{Nvector}).

           @example:

           >>> p = LatLon(45, 45)
           >>> n = p.toNvector()
           >>> n.toStr()  # [0.50, 0.50, 0.70710]
        '''
        if self._Nv is None:
            x, y, z, h = self.to4xyzh()  # nvector.LatLonNvectorBase
            self._Nv = Nvector(x, y, z, h=h, datum=self.datum, ll=self)
        return self._Nv

#     def toVector3d(self):
#         '''Convert this point to a L{Vector3d} normal to the
#            earth's surface.
#
#            @return: Vector representing this point (L{Vector3d}).
#
#            @example:
#
#            >>> p = LatLon(45, 45)
#            >>> v = p.toVector3d()
#            >>> v.toStr()  # '(0.50, 0.50, 0.707)'
#         '''
#         if self._v3d is None:
#             x, y, z, _ = self.to4xyzh()  # nvector.LatLonNvectorBase
#             self._v3d = Vector3d(x, y, z)
#         return self._v3d


class Cartesian(CartesianBase):
    '''Extended to convert (geocentric) L{Cartesian} points to
       (ellipsoidal) L{Nvector} and n-vector-based geodetic L{LatLon}.
    '''
    _Nv = None  #: (INTERNAL) Cache toNvector (L{Nvector}).

    def _update(self, updated):
        '''(INTERNAL) Clear caches if updated.
        '''
        if updated:  # reset caches
            self._Nv = None
            CartesianBase._update(self, updated)

    def toLatLon(self, datum=Datums.WGS84, LatLon=LatLon):  # PYCHOK XXX
        '''Convert this (geocentric) cartesian (x/y/z) point to
           an (ellipsoidal) geodetic point on the specified datum.

           @keyword datum: Optional datum to use (L{Datum}).
           @keyword LatLon: Optional LatLon class for the point (L{LatLon}).

           @return: Ellipsoidal geodetic point (L{LatLon}).
        '''
        a, b, h = self.to3llh(datum)
        return LatLon(a, b, height=h, datum=datum)

    def toNvector(self, datum=Datums.WGS84):
        '''Convert this cartesian to an (ellipsoidal) n-vector.

           @keyword datum: Optional datum to use (L{Datum}).

           @return: The ellipsoidal n-vector (L{Nvector}).

           @raise ValueError: Cartesian origin.

           @example:

           >>> from ellipsoidalNvector import LatLon
           >>> c = Cartesian(3980581, 97, 4966825)
           >>> n = c.toNvector()  # (0.62282, 0.000002, 0.78237, +0.24)
        '''
        if self._Nv is None or datum != self._Nv.datum:
            E = datum.ellipsoid
            x, y, z = self.to3xyz()

            # Kenneth Gade eqn 23
            p = (x * x + y * y) * E.a2
            q = (z * z * E.e12) * E.a2
            r = (p + q - E.e4) / 6
            s = (p * q * E.e4) / (4 * r**3)
            t = cbrt(1 + s + sqrt(s * (2 + s)))

            u = r * (1 + t + 1 / t)
            v = sqrt(u * u + E.e4 * q)
            w = E.e2 * (u + v - q) / (2 * v)

            k = sqrt(u + v + w * w) - w
            if abs(k) < EPS:
                raise ValueError('%s: %r' % ('origin', self))
            e = k / (k + E.e2)
            d = e * hypot(x, y)

            t = hypot(d, z)
            if t < EPS:
                raise ValueError('%s: %r' % ('origin', self))
            h = (k + E.e2 - 1) / k * t

            s = e / t
            self._Nv = Nvector(x * s, y * s, z / t, h=h, datum=datum)
        return self._Nv


class Ned(object):
    '''North-Eeast-Down (NED), also known as Local Tangent Plane (LTP),
       is a vector in the local coordinate frame of a body.
    '''
    _bearing   = None  #: (INTERNAL) Cache bearing (compass degrees).
    _elevation = None  #: (INTERNAL) Cache elevation (degrees).
    _length    = None  #: (INTERNAL) Cache length (scalar).

    def __init__(self, north, east, down):
        '''New North-East-Down vector.

           @param north: North component in meter (scalar).
           @param east: East component in meter (scalar).
           @param down: Down component (normal to the surface
                        of the ellipsoid) in meter (scalar).

           @example:

           >>> from ellipsiodalNvector import Ned
           >>> delta = Ned(110569, 111297, 1936)
           >>> delta.toStr(prec=0)  #  [N:110569, E:111297, D:1936]
        '''
        self.north = north
        self.east  = east
        self.down  = down

    def __str__(self):
        return self.toStr()

    @property
    def bearing(self):
        '''Get the bearing of this NED vector in compass degrees (degrees360).
        '''
        if self._bearing is None:
            self._bearing = degrees360(atan2(self.east, self.north))
        return self._bearing

    @property
    def elevation(self):
        '''Get the elevation, tilt of this NED vector in degrees from
           horizontal, i.e. tangent to ellipsoid surface (degrees90).
        '''
        if self._elevation is None:
            self._elevation = -degrees90(asin(self.down / self.length))
        return self._elevation

    @property
    def length(self):
        '''Gets the length of this NED vector in meter (scalar).
        '''
        if self._length is None:
            self._length = hypot3(self.north, self.east, self.down)
        return self._length

    def to3ned(self):
        '''Return this NED vector as north/east/down components.

           @return: 3-Tuple (north, east, down) in (degrees).
        '''
        return self.north, self.east, self.down

    def toStr(self, prec=3, fmt='[%s]', sep=', '):  # PYCHOK expected
        '''Return a string representation of this NED vector.

           @keyword prec: Optional number of decimals, unstripped (int).
           @keyword fmt: Optional enclosing backets format (string).
           @keyword sep: Optional separator between NEDs (string).

           @return: This Ned as "[N:f, E:f, D:f]" (string).
        '''
        t3 = fStr(self.to3ned(), prec=prec, sep=' ').split()
        return fmt % (sep.join('%s:%s' % t for t in zip('NED', t3)),)

    def toStr2(self, prec=None, fmt='[%s]', sep=', '):  # PYCHOK expected
        '''Return a string representation of this NED vector as
           length, bearing and elevation.

           @keyword prec: Optional number of decimals, unstripped (int).
           @keyword fmt: Optional enclosing backets format (string).
           @keyword sep: Optional separator between NEDs (string).

           @return: This Ned as "[L:f, B:degrees360, E:degrees90]" (string).
        '''
        t3 = (fStr(self.length, prec=3 if prec is None else prec),
              toDMS(self.bearing, form=F_D, prec=prec, ddd=0),
              toDMS(self.elevation, form=F_D, prec=prec, ddd=0))
        return fmt % (sep.join('%s:%s' % t for t in zip('LBE', t3)),)

    def toVector3d(self):
        '''Return this NED vector as a 3-d vector3.

           @return: North, east, down vector (L{Vector3d}).
        '''
        return Vector3d(*self.to3ned())


_Nvll = LatLon(0, 0)  #: (INTERNAL) Reference instance (L{LatLon}).


class Nvector(NvectorBase):
    '''An n-vector is a position representation using a (unit) vector
       normal to the earth ellipsoid.  Unlike lat-/longitude points,
       n-vectors have no singularities or discontinuities.

       For many applications, n-vectors are more convenient to work
       with than other position representations like lat-/longitude,
       earth-centred earth-fixed (ECEF) vectors, UTM coordinates, etc.

       Note commonality with L{sphericalNvector.Nvector}.
    '''
    _datum = Datums.WGS84  #: (INTERNAL) Datum (L{Datum}).

    def __init__(self, x, y, z, h=0, datum=None, ll=None):
        '''New n-vector normal to the earth's surface.

           @param x: X component (scalar).
           @param y: Y component (scalar).
           @param z: Z component (scalar).
           @keyword h: Optional height above model surface (meter).
           @keyword datum: Optional datum this n-vector is defined
                           within (L{Datum}).
           @keyword ll: Optional, original latlon (I{LatLon}).

           @raise TypeError: If datum is not a L{Datum}.

           @example:

           >>> from ellipsoidalNvector import Nvector
           >>> v = Nvector(0.5, 0.5, 0.7071, 1)
           >>> v.toLatLon()  # 45.0°N, 045.0°E, +1.00m
        '''
        NvectorBase.__init__(self, x, y, z, h=h, ll=ll)
        if datum:
            if not isinstance(datum, Datum):
                raise TypeError('%s invalid: %r' % ('datum', datum))
            self._datum = datum

    def copy(self):
        '''Copy this vector.

           @return: Copy (L{Nvector}).
        '''
        n = NvectorBase.copy(self)
        if self.datum != n.datum:
            n._datum = self._datum
        return n

    @property
    def datum(self):
        '''Get this n-vector's datum (L{Datum}).
        '''
        return self._datum

    def toLatLon(self, height=None, LatLon=LatLon):
        '''Convert this n-vector to an (ellipsoidal) geodetic point.

           @keyword height: Optional height, overriding the default
                            height (meter).
           @keyword LatLon: Optional LatLon class for the point (L{LatLon}).

           @return: Point equivalent to this n-vector (L{LatLon}).

           @example:

           >>> v = Nvector(0.5, 0.5, 0.7071)
           >>> p = v.toLatLon()  # 45.0°N, 45.0°E
        '''
        a, b, h = self.to3llh()

        if height is not None:
            h = height
        return LatLon(a, b, height=h, datum=self.datum)

    def toCartesian(self, Cartesian=Cartesian):
        '''Convert this n-vector to a cartesian point.

           @keyword Cartesian: Optional Cartesian class for the point (L{Cartesian}).

           @return: Cartesian equivalent to this n-vector (L{Cartesian}).

           @example:

           >>> v = Nvector(0.5, 0.5, 0.7071)
           >>> c = v.toCartesian()  # [3194434, 3194434, 4487327]
           >>> p = c.toLatLon()  # 45.0°N, 45.0°E
        '''
        E = self.datum.ellipsoid

        x, y, z, h = self.to4xyzh()
        # Kenneth Gade eqn (22)
        n = E.b / hypot3(x * E.ab, y * E.ab, z)
        r = E.ab * E.ab * n + h

        return Cartesian(x * r, y * r, z * (n + h))

    def unit(self):
        '''Normalize this vector to unit length.

           @return: Normalised vector (L{Nvector}).
        '''
        if self._united is None:
            u = NvectorBase.unit(self)
            if u.datum != self.datum:
                u._datum = self.datum
#           self._united = u._united = u
        return self._united


def meanOf(points, datum=Datums.WGS84, height=None, LatLon=LatLon):
    '''Compute the geographic mean of the supplied points.

       @param points: Array of points to be averaged (L{LatLon}[]).
       @keyword datum: Optional datum to use (L{Datum}).
       @keyword height: Optional height, overriding the mean height (meter).
       @keyword LatLon: Optional LatLon class for the mean point (L{LatLon}).

       @return: Point at geographic mean and mean height (L{LatLon}).

       @raise ValueError: Insufficient number of points.
    '''
    _, points = _Nvll.points(points, closed=False)
    # geographic mean
    m = sumOf(p.toNvector() for p in points)
    a, b, h = m.to3llh()

    if height is not None:
        h = height
    return LatLon(a, b, height=h, datum=datum)


def toNed(distance, bearing, elevation):
    '''Create an NED vector from distance, bearing and elevation
       (in local coordinate system).

       @param distance: NED vector length in meter (scalar).
       @param bearing: NED vector bearing in compass degrees (scalar).
       @param elevation: NED vector elevation in degrees from local
                         coordinate frame horizontal (scalar).

       @return: NED vector equivalent to distance, bearing and
                elevation (L{Ned}).

       @JSname: I{fromDistanceBearingElevation}.
    '''
    b, e = radians(bearing), radians(elevation)

    d = float(distance)
    dce = d * cos(e)

    return Ned(cos(b) * dce,
               sin(b) * dce,
              -sin(e) * d)

# **) MIT License
#
# Copyright (C) 2016-2018 -- mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
