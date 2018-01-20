
# -*- coding: utf-8 -*-

u'''Classes L{Datum}, L{Ellipsoid} and L{Transform} and registries thereof.

Pure Python implementation of geodesy tools for ellipsoidal earth models,
including datums and ellipsoid parameters for different geographic coordinate
systems and methods for converting between them and to cartesian coordinates.
Transcribed from JavaScript originals by I{(C) Chris Veness 2005-2016} and
published under the same MIT Licence**, see U{http://www.movable-type.co.uk/
scripts/geodesy/docs/latlon-ellipsoidal.js.html}.

Historical geodetic datums: a latitude/longitude point defines a geographic
location on or above/below the earth’s surface, measured in degrees from
the equator and the International Reference Meridian and meters above the
ellipsoid, and based on a given datum.  The datum is based on a reference
ellipsoid and tied to geodetic survey reference points.

Modern geodesy is generally based on the WGS84 datum (as used for instance
by GPS systems), but previously various reference ellipsoids and datum
references were used.

The UK Ordnance Survey National Grid References are still based on the
otherwise historical OSGB36 datum, q.v. Ordnance Survey 'A guide to
coordinate systems in Great Britain' Section 6 U{http://www.ordnancesurvey
.co.uk/docs/support/guide-coordinate-systems-great-britain.pdf} and also
U{http://www.ordnancesurvey.co.uk/blog/2014/12/2}.

@newfield example: Example, Examples

@var Datums.BD72: Datum(name='BD72', ellipsoid=Ellipsoids.Intl1924, transform=Transforms.BD72)
@var Datums.DHDN: Datum(name='DHDN', ellipsoid=Ellipsoids.Bessel1841, transform=Transforms.DHDN)
@var Datums.ED50: Datum(name='ED50', ellipsoid=Ellipsoids.Intl1924, transform=Transforms.ED50)
@var Datums.GRS80: Datum(name='GRS80', ellipsoid=Ellipsoids.GRS80, transform=Transforms.WGS84)
@var Datums.Irl1975: Datum(name='Irl1975', ellipsoid=Ellipsoids.AiryModified, transform=Transforms.Irl1975)
@var Datums.Krassovski1940: Datum(name='Krassovski1940', ellipsoid=Ellipsoids.Krassovski1940, transform=Transforms.Krassovski1940)
@var Datums.Krassowsky1940: Datum(name='Krassowsky1940', ellipsoid=Ellipsoids.Krassowsky1940, transform=Transforms.Krassowsky1940)
@var Datums.MGI: Datum(name='MGI', ellipsoid=Ellipsoids.Bessel1841, transform=Transforms.MGI)
@var Datums.NAD27: Datum(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)
@var Datums.NAD83: Datum(name='NAD83', ellipsoid=Ellipsoids.GRS80, transform=Transforms.NAD83)
@var Datums.NTF: Datum(name='NTF', ellipsoid=Ellipsoids.Clarke1880IGN, transform=Transforms.NTF)
@var Datums.OSGB36: Datum(name='OSGB36', ellipsoid=Ellipsoids.Airy1830, transform=Transforms.OSGB36)
@var Datums.Potsdam: Datum(name='Potsdam', ellipsoid=Ellipsoids.Bessel1841, transform=Transforms.Bessel1841)
@var Datums.Sphere: Datum(name='Sphere', ellipsoid=Ellipsoids.Sphere, transform=Transforms.WGS84)
@var Datums.TokyoJapan: Datum(name='TokyoJapan', ellipsoid=Ellipsoids.Bessel1841, transform=Transforms.TokyoJapan)
@var Datums.WGS72: Datum(name='WGS72', ellipsoid=Ellipsoids.WGS72, transform=Transforms.WGS72)
@var Datums.WGS84: Datum(name='WGS84', ellipsoid=Ellipsoids.WGS84, transform=Transforms.WGS84)

@var Ellipsoids.Airy1830: Ellipsoid(name='Airy1830', a=6377563.396, b=6356256.909, f_=299.3249646, f=0.003340851, e=0.081673374, e2=0.00667054, e22=0.006715335, n=0.00167322, R=6370461.233666666, Rm=6366901.239881964, R2=6370459.654589442, R3=6370453.309866445, Rr=6366914.608805893)
@var Ellipsoids.AiryModified: Ellipsoid(name='AiryModified', a=6377340.189, b=6356034.448, f_=299.3249646, f=0.003340851, e=0.081673374, e2=0.00667054, e22=0.006715335, n=0.00167322, R=6370238.275333334, Rm=6366678.406194146, R2=6370236.696361165, R3=6370230.351810658, Rr=6366691.774649803)
@var Ellipsoids.Australia1966: Ellipsoid(name='Australia1966', a=6378160, b=6356774.719, f_=298.25, f=0.003352892, e=0.08182018, e2=0.006694542, e22=0.006739661, n=0.001679261, R=6371031.573, Rm=6367458.38162583, R2=6371029.982388151, R3=6371023.591178183, Rr=6367471.848433915)
@var Ellipsoids.Bessel1841: Ellipsoid(name='Bessel1841', a=6377397.155, b=6356078.963, f_=299.152815351, f=0.003342773, e=0.081696831, e2=0.006674372, e22=0.006719219, n=0.001674185, R=6370291.091000001, Rm=6366729.136345566, R2=6370289.510187287, R3=6370283.158276026, Rr=6366742.520324086)
@var Ellipsoids.CPM1799: Ellipsoid(name='CPM1799', a=6375738.7, b=6356671.92557493, f_=334.39, f=0.00299052, e=0.077279343, e2=0.005972097, e22=0.006007977, n=0.001497499, R=6369383.108524977, Rm=6366198.174663714, R2=6369381.8434158, R3=6369376.762470212, Rr=6366208.881847335)
@var Ellipsoids.Clarke1866: Ellipsoid(name='Clarke1866', a=6378206.4, b=6356583.8, f_=294.978698214, f=0.003390075, e=0.082271854, e2=0.006768658, e22=0.006814785, n=0.001697916, R=6370998.866666667, Rm=6367385.921655473, R2=6370997.240632997, R3=6370990.706598808, Rr=6367399.689168951)
@var Ellipsoids.Clarke1880: Ellipsoid(name='Clarke1880', a=6378249.145, b=6356514.86954978, f_=293.465, f=0.003407561, e=0.0824834, e2=0.006803511, e22=0.006850116, n=0.001706689, R=6371004.386516593, Rm=6367372.733858579, R2=6371002.743669633, R3=6370996.141916499, Rr=6367386.643979664)
@var Ellipsoids.Clarke1880IGN: Ellipsoid(name='Clarke1880IGN', a=6378249.2, b=6356515, f_=293.466021294, f=0.00340755, e=0.082483257, e2=0.006803488, e22=0.006850092, n=0.001706683, R=6371004.466666666, Rm=6367372.826648208, R2=6371002.823831111, R3=6370996.22212394, Rr=6367386.736672513)
@var Ellipsoids.Clarke1880Mod: Ellipsoid(name='Clarke1880Mod', a=6378249.145, b=6356514.96582849, f_=293.4663, f=0.003407546, e=0.082483218, e2=0.006803481, e22=0.006850086, n=0.001706681, R=6371004.418609496, Rm=6367372.782080163, R2=6371002.775777077, R3=6370996.174082516, Rr=6367386.692077904)
@var Ellipsoids.Delambre1810: Ellipsoid(name='Delambre1810', a=6376428, b=6355957.92616372, f_=311.5, f=0.003210273, e=0.080063974, e2=0.00641024, e22=0.006451596, n=0.001607717, R=6369604.642054573, Rm=6366184.735554905, R2=6369603.184197493, R3=6369597.327390675, Rr=6366197.076842674)
@var Ellipsoids.Engelis1985: Ellipsoid(name='Engelis1985', a=6378136.05, b=6356751.32272154, f_=298.2566, f=0.003352818, e=0.081819276, e2=0.006694394, e22=0.006739511, n=0.001679224, R=6371007.807573847, Rm=6367434.70891814, R2=6371006.217070852, R3=6370999.826135725, Rr=6367448.175078915)
@var Ellipsoids.Everest1969: Ellipsoid(name='Everest1969', a=6377295.664, b=6356094.667915, f_=300.8017, f=0.003324449, e=0.081472981, e2=0.006637847, e22=0.006682202, n=0.001664992, R=6370228.665305, Rm=6366686.341077896, R2=6370227.101785341, R3=6370220.819516171, Rr=6366699.578394239)
@var Ellipsoids.Fisher1968: Ellipsoid(name='Fisher1968', a=6378150, b=6356768.33724438, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371022.77908146, Rm=6367450.193774211, R2=6371021.189037351, R3=6371014.799950343, Rr=6367463.656043012)
@var Ellipsoids.GEM10C: Ellipsoid(name='GEM10C', a=6378137, b=6356752.31424783, f_=298.2572236, f=0.003352811, e=0.081819191, e2=0.00669438, e22=0.006739497, n=0.00167922, R=6371008.771415944, Rm=6367435.679717519, R2=6371007.180919358, R3=6371000.790010039, Rr=6367449.145823942)
@var Ellipsoids.GRS67: Ellipsoid(name='GRS67', a=6378160, b=6356774.516, f_=298.247167427, f=0.003352924, e=0.081820568, e2=0.006694605, e22=0.006739725, n=0.001679277, R=6371031.505333333, Rm=6367458.279955242, R2=6371029.914708731, R3=6371023.523359839, Rr=6367471.747019209)
@var Ellipsoids.GRS80: Ellipsoid(name='GRS80', a=6378137, b=6356752.314140347, f_=298.257222101, f=0.003352811, e=0.081819191, e2=0.00669438, e22=0.006739497, n=0.00167922, R=6371008.771380115, Rm=6367435.679663688, R2=6371007.180883513, R3=6371000.789974131, Rr=6367449.145770246)
@var Ellipsoids.Helmert1906: Ellipsoid(name='Helmert1906', a=6378200, b=6356818.16962789, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371072.723209296, Rm=6367500.10989561, R2=6371071.133152724, R3=6371064.744015628, Rr=6367513.572269944)
@var Ellipsoids.IERS1989: Ellipsoid(name='IERS1989', a=6378136, b=6356751.302, f_=298.257, f=0.003352813, e=0.081819221, e2=0.006694385, e22=0.006739502, n=0.001679222, R=6371007.767333333, Rm=6367434.673581903, R2=6371006.176906484, R3=6370999.785917024, Rr=6367448.139705879)
@var Ellipsoids.IERS1992TOPEX: Ellipsoid(name='IERS1992TOPEX', a=6378136.3, b=6356751.61659215, f_=298.257223563, f=0.003352811, e=0.081819191, e2=0.00669438, e22=0.006739497, n=0.00167922, R=6371008.072197382, Rm=6367434.980890662, R2=6371006.481700973, R3=6371000.090792353, Rr=6367448.446995611)
@var Ellipsoids.IERS2003: Ellipsoid(name='IERS2003', a=6378136.6, b=6356751.85797165, f_=298.25642, f=0.00335282, e=0.081819301, e2=0.006694398, e22=0.006739515, n=0.001679225, R=6371008.352657217, Rm=6367435.251531576, R2=6371006.762152168, R3=6371000.371208764, Rr=6367448.71770978)
@var Ellipsoids.Intl1924: Ellipsoid(name='Intl1924', a=6378388, b=6356911.946, f_=297, f=0.003367003, e=0.08199189, e2=0.00672267, e22=0.00676817, n=0.001686341, R=6371229.315333334, Rm=6367640.919007843, R2=6371227.711270464, R3=6371221.265832124, Rr=6367654.499992855)
@var Ellipsoids.Intl1967: Ellipsoid(name='Intl1967', a=6378157.5, b=6356772.2, f_=298.24961539, f=0.003352896, e=0.081820233, e2=0.00669455, e22=0.00673967, n=0.001679263, R=6371029.066666666, Rm=6367455.872106339, R2=6371027.476083895, R3=6371021.084827519, Rr=6367469.33894366)
@var Ellipsoids.Krassovski1940: Ellipsoid(name='Krassovski1940', a=6378245, b=6356863.01877305, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371117.67292435, Rm=6367545.034404869, R2=6371116.08285656, R3=6371109.693674386, Rr=6367558.496874185)
@var Ellipsoids.Krassowsky1940: Ellipsoid(name='Krassowsky1940', a=6378245, b=6356863.01877305, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371117.67292435, Rm=6367545.034404869, R2=6371116.08285656, R3=6371109.693674386, Rr=6367558.496874185)
@var Ellipsoids.Maupertuis1738: Ellipsoid(name='Maupertuis1738', a=6397300, b=6363806.28272251, f_=191, f=0.005235602, e=0.102194876, e2=0.010443793, e22=0.010554017, n=0.002624672, R=6386135.42757417, Rm=6380531.163818629, R2=6386131.541448465, R3=6386115.886282292, Rr=6380564.130113637)
@var Ellipsoids.Mercury1960: Ellipsoid(name='Mercury1960', a=6378166, b=6356784.28360711, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371038.76120237, Rm=6367466.166933062, R2=6371037.171154275, R3=6371030.782051236, Rr=6367479.629235634)
@var Ellipsoids.Mercury1968Mod: Ellipsoid(name='Mercury1968Mod', a=6378150, b=6356768.33724438, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371022.77908146, Rm=6367450.193774211, R2=6371021.189037351, R3=6371014.799950343, Rr=6367463.656043012)
@var Ellipsoids.NWL1965: Ellipsoid(name='NWL1965', a=6378145, b=6356759.76948868, f_=298.25, f=0.003352892, e=0.08182018, e2=0.006694542, e22=0.006739661, n=0.001679261, R=6371016.58982956, Rm=6367443.406891448, R2=6371014.999254003, R3=6371008.60802666, Rr=6367456.873667615)
@var Ellipsoids.OSU86F: Ellipsoid(name='OSU86F', a=6378136.2, b=6356751.51693008, f_=298.2572236, f=0.003352811, e=0.081819191, e2=0.00669438, e22=0.006739497, n=0.00167922, R=6371007.972310026, Rm=6367434.88105977, R2=6371006.381813641, R3=6370999.990905124, Rr=6367448.347164505)
@var Ellipsoids.OSU91A: Ellipsoid(name='OSU91A', a=6378136.3, b=6356751.6165948, f_=298.2572236, f=0.003352811, e=0.081819191, e2=0.00669438, e22=0.006739497, n=0.00167922, R=6371008.072198267, Rm=6367434.98089199, R2=6371006.481701856, R3=6371000.090793238, Rr=6367448.446996935)
@var Ellipsoids.Plessis1817: Ellipsoid(name='Plessis1817', a=6376523, b=6355862.93325557, f_=308.64, f=0.003240021, e=0.080433474, e2=0.006469544, e22=0.006511671, n=0.001622639, R=6369636.31108519, Rm=6366184.585664447, R2=6369634.826085826, R3=6369628.859996674, Rr=6366197.15710669)
@var Ellipsoids.SGS85: Ellipsoid(name='SGS85', a=6378136, b=6356751.30156878, f_=298.257, f=0.003352813, e=0.081819221, e2=0.006694385, e22=0.006739502, n=0.001679222, R=6371007.767189593, Rm=6367434.673365931, R2=6371006.176690875, R3=6370999.785772962, Rr=6367448.13949045)
@var Ellipsoids.SoAmerican1969: Ellipsoid(name='SoAmerican1969', a=6378160, b=6356774.71919531, f_=298.25, f=0.003352892, e=0.08182018, e2=0.006694542, e22=0.006739661, n=0.001679261, R=6371031.573065103, Rm=6367458.38172365, R2=6371029.982485807, R3=6371023.591243432, Rr=6367471.848531487)
@var Ellipsoids.Sphere: Ellipsoid(name='Sphere', a=6371008.771415, b=6371008.771415, f_=0, f=0, e=0, e2=0, e22=0, n=0, R=6371008.771415, Rm=6371008.771415, R2=6371008.771415, R3=6371008.771415, Rr=6371008.771415)
@var Ellipsoids.SphereAuthalic: Ellipsoid(name='SphereAuthalic', a=6371000, b=6371000, f_=0, f=0, e=0, e2=0, e22=0, n=0, R=6371000, Rm=6371000, R2=6371000, R3=6371000, Rr=6371000)
@var Ellipsoids.SpherePopular: Ellipsoid(name='SpherePopular', a=6378137, b=6378137, f_=0, f=0, e=0, e2=0, e22=0, n=0, R=6378137, Rm=6378137, R2=6378137, R3=6378137, Rr=6378137)
@var Ellipsoids.Struve1860: Ellipsoid(name='Struve1860', a=6378298.3, b=6356657.14266956, f_=294.73, f=0.003392936, e=0.082306499, e2=0.00677436, e22=0.006820565, n=0.001699351, R=6371084.580889854, Rm=6367468.527348378, R2=6371082.952089875, R3=6371076.406914177, Rr=6367482.318324657)
@var Ellipsoids.WGS60: Ellipsoid(name='WGS60', a=6378165, b=6356783.28695944, f_=298.3, f=0.00335233, e=0.081813334, e2=0.006693422, e22=0.006738525, n=0.001678979, R=6371037.762319813, Rm=6367465.168610634, R2=6371036.172271968, R3=6371029.783169931, Rr=6367478.630911095)
@var Ellipsoids.WGS66: Ellipsoid(name='WGS66', a=6378145, b=6356759.76948868, f_=298.25, f=0.003352892, e=0.08182018, e2=0.006694542, e22=0.006739661, n=0.001679261, R=6371016.58982956, Rm=6367443.406891448, R2=6371014.999254003, R3=6371008.60802666, Rr=6367456.873667615)
@var Ellipsoids.WGS72: Ellipsoid(name='WGS72', a=6378135, b=6356750.52, f_=298.26, f=0.003352779, e=0.081818811, e2=0.006694318, e22=0.006739434, n=0.001679205, R=6371006.84, Rm=6367433.78276368, R2=6371005.249530816, R3=6370998.858745317, Rr=6367447.24861499)
@var Ellipsoids.WGS84: Ellipsoid(name='WGS84', a=6378137, b=6356752.31425, f_=298.257223563, f=0.003352811, e=0.081819191, e2=0.00669438, e22=0.006739497, n=0.00167922, R=6371008.771416667, Rm=6367435.679718607, R2=6371007.180920884, R3=6371000.790010764, Rr=6367449.145825027)

@var Transforms.BD72: Transform(name='BD72', tx=106.86863, ty=-52.29778, tz=103.72389, rx=-0.0, ry=-0.0, rz=-0.00001, s=1.2727, s1=1.0, sx=-0.33657, sy=-0.45696, sz=-1.84218)
@var Transforms.Bessel1841: Transform(name='Bessel1841', tx=-582, ty=-105, tz=-414, rx=-0.00001, ry=-0.0, rz=0.00001, s=-8.3, s1=0.99999, sx=-1.04, sy=-0.35, sz=3.08)
@var Transforms.Clarke1866: Transform(name='Clarke1866', tx=8, ty=-160, tz=-176, rx=0, ry=0, rz=0, s=0, s1=1, sx=0, sy=0, sz=0)
@var Transforms.DHDN: Transform(name='DHDN', tx=-591.28, ty=-81.35, tz=-396.39, rx=0.00001, ry=-0.0, rz=-0.00001, s=-9.82, s1=0.99999, sx=1.477, sy=-0.0736, sz=-1.458)
@var Transforms.ED50: Transform(name='ED50', tx=89.5, ty=93.8, tz=123.1, rx=0, ry=0, rz=0.0, s=-1.2, s1=1.0, sx=0, sy=0, sz=0.156)
@var Transforms.Irl1965: Transform(name='Irl1965', tx=-482.53, ty=130.596, tz=-564.557, rx=0.00001, ry=0.0, rz=0.0, s=-8.15, s1=0.99999, sx=1.042, sy=0.214, sz=0.631)
@var Transforms.Irl1975: Transform(name='Irl1975', tx=-482.53, ty=130.596, tz=-564.557, rx=-0.00001, ry=-0.0, rz=-0.0, s=-1.1, s1=1.0, sx=-1.042, sy=-0.214, sz=-0.631)
@var Transforms.Krassovski1940: Transform(name='Krassovski1940', tx=-24, ty=123, tz=94, rx=-0.0, ry=0.0, rz=0.0, s=-2.423, s1=1.0, sx=-0.02, sy=0.26, sz=0.13)
@var Transforms.Krassowsky1940: Transform(name='Krassowsky1940', tx=-24, ty=123, tz=94, rx=-0.0, ry=0.0, rz=0.0, s=-2.423, s1=1.0, sx=-0.02, sy=0.26, sz=0.13)
@var Transforms.MGI: Transform(name='MGI', tx=-577.326, ty=-90.129, tz=-463.92, rx=0.00002, ry=0.00001, rz=0.00003, s=-2.423, s1=1.0, sx=5.137, sy=1.474, sz=5.297)
@var Transforms.NAD27: Transform(name='NAD27', tx=8, ty=-160, tz=-176, rx=0, ry=0, rz=0, s=0, s1=1, sx=0, sy=0, sz=0)
@var Transforms.NAD83: Transform(name='NAD83', tx=1.004, ty=-1.91, tz=-0.515, rx=0.0, ry=0.0, rz=0.0, s=-0.0015, s1=1.0, sx=0.0267, sy=0.00034, sz=0.011)
@var Transforms.NTF: Transform(name='NTF', tx=-168, ty=-60, tz=320, rx=0, ry=0, rz=0, s=0, s1=1, sx=0, sy=0, sz=0)
@var Transforms.OSGB36: Transform(name='OSGB36', tx=-446.448, ty=125.157, tz=-542.06, rx=-0.0, ry=-0.0, rz=-0.0, s=20.4894, s1=1.00002, sx=-0.1502, sy=-0.247, sz=-0.8421)
@var Transforms.TokyoJapan: Transform(name='TokyoJapan', tx=148, ty=-507, tz=-685, rx=0, ry=0, rz=0, s=0, s1=1, sx=0, sy=0, sz=0)
@var Transforms.WGS72: Transform(name='WGS72', tx=0, ty=0, tz=-4.5, rx=0, ry=0, rz=0.0, s=-0.22, s1=1.0, sx=0, sy=0, sz=0.554)
@var Transforms.WGS84: Transform(name='WGS84', tx=0, ty=0, tz=0, rx=0, ry=0, rz=0, s=0, s1=1, sx=0, sy=0, sz=0)

'''

# make sure int division yields float quotient
from __future__ import division as _

from bases import Base, Named
from utils import R_M, cbrt, cbrt2, fdot, fStr, \
                  m2km, m2NM, m2SM, radians

from math import atanh, sqrt

R_M  = R_M        #: Mean, spherical earth radius (meter).
R_MA = 6378137.0  #: Equatorial earth radius (meter) WGS84, EPSG:3785.
R_MB = 6356752.0  #: Polar earth radius (meter) WGS84, EPSG:3785.
R_KM = m2km(R_M)  #: Mean, spherical earth radius (kilo meter).
R_NM = m2NM(R_M)  #: Mean, spherical earth radius (nautical miles).
R_SM = m2SM(R_M)  #: Mean, spherical earth radius (statute miles).
# See <http://www.edwilliams.org/avform.htm>,
# <http://www.dtic.mil/dtic/tr/fulltext/u2/a216843.pdf> and
# <http://github.com/nasa/MultiDop/blob/master/src/share/man/man3/geog_lib.3>
# based on International Standard Nautical Mile of 1,852 meter (1' latitude)
R_FM = 6371000.0  #: Former FAI Sphere earth radius (meter).
R_VM = 6366707.0194937  #: Aviation/Navigation earth radius (meter).
# R_?? = 6372797.560856   #: XXX some other earth radius?

# all public contants, classes and functions
__all__ = ('R_MA', 'R_MB', 'R_KM', 'R_M', 'R_NM', 'R_SM', 'R_FM', 'R_VM',  # constants
           'Datum',  'Ellipsoid',  'Transform',  # classes
           'Datums', 'Ellipsoids', 'Transforms')  # enum-like
__version__ = '18.01.14'

division = 1 / 2  # double check int division, see utils.py
if not division:
    raise ImportError('%s 1/2 == %d' % ('division', division))
del division


class _Enum(dict, Named):
    '''(INTERNAL) Enum-like dict sub-class.
    '''
    def __init__(self, name):
        '''New Enum.

           @param name: Name (string).
        '''
        self._name = name

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError("%s.%s doesn't exist" % (self._name, attr))

    def __repr__(self):
        return '\n'.join('%s.%s: %r' % (self._name, n, v) for n, v in sorted(self.items()))

    def __str__(self):
        return self._name + ', '.join(sorted('.' + n for n in self.keys()))

    def _assert(self, **kwds):
        '''(INTERNAL) Check names against given names.
        '''
        for a, v in kwds.items():
            assert getattr(self, a) is v

    def unregister(self, name):
        '''Remove a registered instance.

           @param name: Name of the instance (string).

           @return: The unregistered instance.

           @raise NameError: No instance with that name.
        '''
        try:
            return dict.pop(self, name)
        except KeyError:
            raise NameError('no %s %r' % (self._name, name))


Datums     = _Enum('Datums')      #: Registered datums (L{_Enum}).
Ellipsoids = _Enum('Ellipsoids')  #: Registered ellipsoids (L{_Enum}).
Transforms = _Enum('Transforms')  #: Registered transforms (L{_Enum}).


class _Based(Base, Named):
    '''(INTERNAL) Base class.
    '''
    def __ne__(self, other):
        '''Compare this and an other ellipsoid.

           @return: True if different (bool).
        '''
        return not self.__eq__(other)

    def _fStr(self, prec, *attrs, **others):
        '''(INTERNAL) Format.
        '''
        t = fStr([getattr(self, a) for a in attrs], prec=prec, sep=' ', ints=True)
        t = ['%s=%s' % (a, v) for a, v in zip(attrs, t.split())]
        if others:
            t += ['%s=%s' % (a, v) for a, v in sorted(others.items())]
        return ', '.join(['name=%r' % (self.name,)] + t)

    def _register(self, enum, name):
        '''(INTERNAL) Add this as enum.name.
        '''
        if name:
            self._name = name
            if name[:1].isalpha():
                if name in enum:
                    raise NameError('%s.%s exists' % (enum.name, name))
                enum[name] = self


def _Krueger6(n, *fs6):
    '''(INTERNAL) Compute the 6th-order Krüger Alpha or Beta
       series per Karney 2011, 'Transverse Mercator with an
       accuracy of a few nanometers', page 7, equations 35
       and 36, see <http://arxiv.org/pdf/1002.1417v3.pdf>.

       @param n: 3rd flatting (float).
       @param fs6: 6-Tuple of coefficent tuples.

       @return: 6th-Order Krüger (7-tuple, 1-origin).
    '''
    ns = [n]  # 3rd flattening: n, n**2, ... n**6
    for i in range(len(fs6) - 1):
        ns.append(ns[0] * ns[i])

    k6 = [0]  # 1-origin
    for fs in fs6:
        i = len(ns) - len(fs)
        k6.append(fdot(fs, *ns[i:]))

    return tuple(k6)


class Ellipsoid(_Based):
    '''Ellipsoid with semi-major, semi-minor axis, inverse flattening
       and a number of other pre-computed, frequently used values.
    '''
    a    = 0  #: Semi-major, equatorial axis (meter).
    b    = 0  #: Semi-minor, polar axis (meter): a * (f - 1) / f.
    # pre-computed, frequently used values
    a2   = 0  #: (1 / a**2)
    ab   = 1  #: (a / b) = 1 / (1 - f)
    e    = 0  #: 1st Eccentricity: sqrt(1 - (b / a)**2))
    e2   = 0  #: 1st Eccentricity squared: f * (2 - f) = 1 - (b / a)**2
    e4   = 0  #: e2**2
    e12  = 1  #: 1 - e2
    e22  = 0  #: 2nd Eccentricity squared: e2 / (1 - e2) = ab**2 - 1
    f    = 0  #: Flattening: (a - b) / a
    f_   = 0  #: Inverse flattening: a / (a - b) = 1 / f
    n    = 0  #: 3rd Flattening: f / (2 - f) = (a - b) / (a + b)
    # earth radii from <http://wikipedia.org/wiki/Earth_radius>
    R    = 0  #: Mean earth radius: (2 * a + b) / 3 per IUGG definition (meter)
    Rm   = 0  #: Mean earth radius: sqrt(a * b) (meter)
    R2   = 0  #: Authalic radius: sqrt((a**2 + b**2 * atanh(e) / e) / 2) (meter)
    R3   = 0  #: Volumetric radius: (a * a * b)**1/3 (meter)
    Rr   = 0  #: Rectifying radius: ((a**3/2 + b**3/2) / 2)**2/3 (meter)

    _A      = None  #: (INTERNAL) meridional radius
    _Alpha6 = None  #: (INTERNAL) 6th-order Krüger Alpha series
    _Beta6  = None  #: (INTERNAL) 6th-order Krüger Beta series
    _Mabcd  = None  #: (INTERNAL) OSGB meridional coefficients

    def __init__(self, a, b, f_, name=''):
        '''New ellipsoid.

           @param a: Semi-major, equatorial axis (meter).
           @param b: Semi-minor, polar axis (meter).
           @param f_: Inverse flattening: a / (a - b) (float >>> 1).
           @keyword name: Optional, unique name (string).

           @raise NameError: If ellipsoid name already exists.
        '''
        self.a = a = float(a)  # major half-axis in meter
        if not b:  # get b from a and f_
            self.b = b = a * (f_ - 1) / float(f_)
        else:  # get f_ from a and b if not spherical
            self.b = b = float(b)  # minor half-axis in meter
            if not f_ and a > b:
                f_ = a / (a - b)
        if f_ > 0 and a > b:
            self.f_ = f_ = float(f_)  # inverse flattening
            self.f  = f  = 1 / f_  # flattening
            self.n  = n  = f / (2 - f)  # 3rd flattening for utm
            self.e2 = e2 = f * (2 - f)  # 1st eccentricity squared
            self.e4 = e2 * e2  # for Nvector.Cartesian.toNvector
            self.e  = sqrt(e2)  # eccentricity for utm
            self.e12 = 1 - e2  # for Nvector.Cartesian.toNvector and utm
            self.e22 = e2 / (1 - e2)  # 2nd eccentricity squared
            self.ab = a / b  # for Nvector.toCartesian
            self.R = (2 * a + b) / 3  # per IUGG definition for WGS84
            self.Rm = sqrt(a * b)  # mean radius
            self.R2 = sqrt((a * a + b * b * atanh(self.e) / self.e) * 0.5)  # authalic radius
            self.R3 = cbrt(a * a * b)  # volumetric radius
            self.Rr = cbrt2((pow(a, 1.5) + pow(b, 1.5)) * 0.5)  # rectifying radius
        else:
            self.R = self.Rm = self.R2 = self.R3 = self.Rr = self.b = b = a
            f_ = f = n = 0
        self.a2 = 1 / (a * a)  # for Nvector.Cartesian.toNvector

        d = a - b
        self._ab_90 = d / 90  # for radiusAt below

        # some sanity checks to catch mistakes
        if d < 0 or min(a, b) < 1:
            raise AssertionError('%s: %s=%0.9f vs %s=%0.9f' % (name,
                                 'a', a, 'b', b))
        t = d / a
        if abs(f - t) > 1e-8:
            raise AssertionError('%s: %s=%.9e vs %s=%.9e' % (name,
                                 'f', f, '(a-b)/a', t))
        t = d / (a + b)
        if abs(n - t) > 1e-8:
            raise AssertionError('%s: %s=%.9e vs %s=%.9e' % (name,
                                 'n', n, '(a-b)/(a+b)', t))
        t = self.ab ** 2 - 1
        if abs(self.e22 - t) > 1e-8:
            raise AssertionError('%s: %s=%.9e vs %s=%.9e' % (name,
                                 'e22', self.e22, 'ab**2-1', t))

        self._register(Ellipsoids, name)

    def __eq__(self, other):
        '''Compare this and an other ellipsoid.

           @param other: The other ellipsoid (L{Ellipsoid}).

           @return: True if equal (bool).
        '''
        return self is other or (isinstance(other, Ellipsoid) and
                                 self.a == other.a and
                                 self.b == other.b)

    @property
    def A(self):
        '''Get the meridional radius (meter).
        '''
        if self._A is None:
            n = self.n
            n2_4 = n * n / 4
            n4_64 = n2_4 * n2_4 / 4
            n6_256 = n2_4 * n4_64
            # A = a / (1 + n) * (1 + n**2 / 4 + n**4 / 64 + n**6 / 256 +
            #                   n**8 * 25 / 16384 + n**10 * 49 / 65536)
            self._A = self.a / (1 + n) * (1 + n2_4 + n4_64 + n6_256)
        return self._A

    @property
    def Alpha6(self):
        '''Get the 6th-order Krüger Alpha series (7-tuple, 1-origin).
        '''
        if self._Alpha6 is None:
            self._Alpha6 = _Krueger6(self.n,
                # XXX i/i quotients require  from __future__ import division
                # n    n**2   n**3      n**4         n**5            n**6
                (1/2, -2/3,   5/16,    41/180,    -127/288,       7891/37800),
                     (13/48, -3/5,    557/1440,    281/630,   -1983433/1935360),  # PYCHOK expected
                            (61/240, -103/140,   15061/26880,   167603/181440),  # PYCHOK expected
                                   (49561/161280, -179/168,    6601661/7257600),  # PYCHOK expected
                                                (34729/80640, -3418889/1995840),  # PYCHOK expected
                                                            (212378941/319334400,))  # PYCHOK expected
        return self._Alpha6

    @property
    def Beta6(self):
        '''Get the 6th-order Krüger Beta series (7-tuple, 1-origin).
        '''
        if self._Beta6 is None:
            self._Beta6 = _Krueger6(self.n,
                # XXX i/i quotients require  from __future__ import division
                # n    n**2  n**3     n**4        n**5            n**6
                (1/2, -2/3, 37/96,   -1/360,    -81/512,      96199/604800),
                      (1/48, 1/15, -437/1440,    46/105,   -1118711/3870720),  # PYCHOK expected
                           (17/480, -37/840,   -209/4480,      5569/90720),  # PYCHOK expected
                                  (4397/161280, -11/504,    -830251/7257600),  # PYCHOK expected
                                              (4583/161280, -108847/3991680),  # PYCHOK expected
                                                          (20648693/638668800,))  # PYCHOK expected
        return self._Beta6

    def e2s2(self, s):
        '''Compute the norm sqrt(1 - e2 * s**2).

           @param s: S value (scalar).

           @return: Norm (float).
        '''
        return sqrt(1 - self.e2 * s * s)

    @property
    def isEllipsoidal(self):
        '''Check whether this model is ellipsoidal (bool).
        '''
        return self.a > self.R > self.b

    @property
    def isSpherical(self):
        '''Check whether this model is spherical (bool).
        '''
        return self.a == self.R == self.b

    @property
    def Mabcd(self):
        '''Get the OSGR meridional coefficients, Airy130 only (4-tuple).
        '''
        if self._Mabcd is None:
            n = self.n
            n2 = n * n
            n3 = n * n2
            # XXX i/i quotients require  from __future__ import division
            self._Mabcd = (fdot((1, n, n2, n3), 1, 1,  5/4, 5/4),
                           fdot(   (n, n2, n3), 3, 3, 21/8),
                           fdot(      (n2, n3), 15/8, 15/8),
                                   35/24 * n3)
        return self._Mabcd

    def radiusAt(self, lat):
        '''Approximate the ellipsoid radius at the given
           latitude in degrees by trivial interpolation.

           @param lat: Latitude (degrees90).

           @return: Radius at that latitude (meter).
        '''
        # r = major - (major - minor) * |lat| / 90
        return self.a - self._ab_90 * min(abs(lat), 90)

    def toStr(self, prec=9):  # PYCHOK expected
        '''Return this ellipsoid as a string.

           @keyword prec: Optional number of decimals, unstripped (int).

           @return: Ellipsoid attributes (string).
        '''
        return self._fStr(prec, 'a', 'b', 'f_', 'f', 'e', 'e2', 'e22',
                                'n', 'R', 'Rm', 'R2', 'R3', 'Rr')


# <http://www.gnu.org/software/gama/manual/html_node/Supported-ellipsoids.html>
# <http://w3.energistics.org/archive/Epicentre/Epicentre_v3.0/DataModel/
#         LogicalDictionary/StandardValues/ellipsoid.html>
# <http://kb.osu.edu/dspace/handle/1811/77986>
Ellipsoids._assert(  # <http://wikipedia.org/wiki/Earth_ellipsoid>
    Airy1830       = Ellipsoid(6377563.396, 6356256.909,       299.3249646,   'Airy1830'),
    AiryModified   = Ellipsoid(6377340.189, 6356034.448,       299.3249646,   'AiryModified'),
    Australia1966  = Ellipsoid(6378160.0,   6356774.719,       298.25,        'Australia1966'),
    Bessel1841     = Ellipsoid(6377397.155, 6356078.963,       299.152815351, 'Bessel1841'),  # XXX 299.1528128
    Clarke1866     = Ellipsoid(6378206.4,   6356583.8,         294.978698214, 'Clarke1866'),
    Clarke1880     = Ellipsoid(6378249.145, 6356514.86954978,  293.465,       'Clarke1880'),
    Clarke1880Mod  = Ellipsoid(6378249.145, 6356514.96582849,  293.4663,      'Clarke1880Mod'),
    Clarke1880IGN  = Ellipsoid(6378249.2,   6356515.0,         293.466021294, 'Clarke1880IGN'),  # XXX confirm
    CPM1799        = Ellipsoid(6375738.7,   6356671.92557493,  334.39,        'CPM1799'),  # Comm. des Poids et Mesures
    Delambre1810   = Ellipsoid(6376428.0,   6355957.92616372,  311.5,         'Delambre1810'),  # Belgium
    Engelis1985    = Ellipsoid(6378136.05,  6356751.32272154,  298.2566,      'Engelis1985'),
    Everest1969    = Ellipsoid(6377295.664, 6356094.667915,    300.8017,      'Everest1969'),
    Fisher1968     = Ellipsoid(6378150.0,   6356768.33724438,  298.3,         'Fisher1968'),
    GEM10C         = Ellipsoid(6378137.0,   6356752.31424783,  298.2572236,   'GEM10C'),
    GRS67          = Ellipsoid(6378160.0,   6356774.516,       298.247167427, 'GRS67'),  # Lucerne
    GRS80          = Ellipsoid(6378137.0,   6356752.314140347, 298.257222101, 'GRS80'),  # ITRS, ETRS89
    Helmert1906    = Ellipsoid(6378200.0,   6356818.16962789,  298.3,         'Helmert1906'),
    IERS1989       = Ellipsoid(6378136.0,   6356751.302,       298.257,       'IERS1989'),
    IERS1992TOPEX  = Ellipsoid(6378136.3,   6356751.61659215,  298.257223563, 'IERS1992TOPEX'),  # IERS/TOPEX/Poseidon/McCarthy
    IERS2003       = Ellipsoid(6378136.6,   6356751.85797165,  298.25642,     'IERS2003'),
    Intl1924       = Ellipsoid(6378388.0,   6356911.946,       297.0,         'Intl1924'),  # aka Hayford
    Intl1967       = Ellipsoid(6378157.5,   6356772.2,         298.24961539,  'Intl1967'),  # New Int'l
    Krassovski1940 = Ellipsoid(6378245.0,   6356863.01877305,  298.3,         'Krassovski1940'),  # spelling
    Krassowsky1940 = Ellipsoid(6378245.0,   6356863.01877305,  298.3,         'Krassowsky1940'),  # spelling
    Maupertuis1738 = Ellipsoid(6397300.0,   6363806.28272251,  191.0,         'Maupertuis1738'),  # France
    Mercury1960    = Ellipsoid(6378166.0,   6356784.28360711,  298.3,         'Mercury1960'),
    Mercury1968Mod = Ellipsoid(6378150.0,   6356768.33724438,  298.3,         'Mercury1968Mod'),
    NWL1965        = Ellipsoid(6378145.0,   6356759.76948868,  298.25,        'NWL1965'),  # Naval Weapons Lab.
    OSU86F         = Ellipsoid(6378136.2,   6356751.51693008,  298.2572236,   'OSU86F'),
    OSU91A         = Ellipsoid(6378136.3,   6356751.6165948,   298.2572236,   'OSU91A'),
#   Plessis1817    = Ellipsoid(6397523.0,   6355863.0,         153.56512242,  'Plessis1817'),  # XXX incorrect?
    Plessis1817    = Ellipsoid(6376523.0,   6355862.93325557,  308.64,        'Plessis1817'),  # XXX IGN France 1972
    SGS85          = Ellipsoid(6378136.0,   6356751.30156878,  298.257,       'SGS85'),  # Soviet Geodetic System
    SoAmerican1969 = Ellipsoid(6378160.0,   6356774.71919531,  298.25,        'SoAmerican1969'),  # South American
    Struve1860     = Ellipsoid(6378298.3,   6356657.14266956,  294.73,        'Struve1860'),
    WGS60          = Ellipsoid(6378165.0,   6356783.28695944,  298.3,         'WGS60'),
    WGS66          = Ellipsoid(6378145.0,   6356759.76948868,  298.25,        'WGS66'),
    WGS72          = Ellipsoid(6378135.0,   6356750.52,        298.26,        'WGS72'),
    WGS84          = Ellipsoid(6378137.0,   6356752.31425,     298.257223563, 'WGS84'),  # GPS
    Sphere         = Ellipsoid(R_M,         R_M,                 0.0,         'Sphere'),  # pseudo
    SphereAuthalic = Ellipsoid(R_FM,        R_FM,                0.0,         'SphereAuthalic'),  # pseudo
    SpherePopular  = Ellipsoid(R_MA,        R_MA,                0.0,         'SpherePopular'),  # EPSG:3857 Spheroid
)


class Transform(_Based):
    '''Helmert transformation.
    '''
    tx = 0  #: X translation (meter).
    ty = 0  #: Y translation (meter).
    tz = 0  #: Z translation (meter).

    rx = 0  #: X rotation (radians).
    ry = 0  #: Y rotation (radians).
    rz = 0  #: Z rotation (radians).

    s  = 0  #: Scale ppm (float).
    s1 = 1  #: Scale + 1 (float).

    sx = 0  #: X rotation (degree seconds).
    sy = 0  #: Y rotation (degree seconds).
    sz = 0  #: Z rotation (degree seconds).

    def __init__(self, name='', tx=0, ty=0, tz=0,
                                sx=0, sy=0, sz=0, s=0):
        '''New transform.

           @keyword name: Optional, unique name (string).
           @keyword tx: Optional X translation (meter).
           @keyword ty: Optional Y translation (meter).
           @keyword tz: Optional Z translation (meter).
           @keyword s: Optional scale ppm (float).
           @keyword sx: Optional X rotation (degree seconds).
           @keyword sy: Optional Y rotation (degree seconds).
           @keyword sz: Optional Z rotation (degree seconds).

           @raise NameError: If transform name already exists.
        '''
        if tx:
            self.tx = float(tx)
        if ty:
            self.ty = float(ty)
        if tz:
            self.tz = float(tz)
        if sx:  # secs to rads
            self.rx = radians(sx / 3600.0)
            self.sx = sx
        if sy:
            self.ry = radians(sy / 3600.0)
            self.sy = sy
        if sz:
            self.rz = radians(sz / 3600.0)
            self.sz = sz
        if s:
            self.s = float(s)
            self.s1 = s * 1.e-6 + 1  # normalize ppm to (s + 1)

        self._register(Transforms, name)

    def __eq__(self, other):
        '''Compare this and an other transform.

           @param other: The other transform (L{Transform}).

           @return: True if equal (bool).
        '''
        return self is other or (isinstance(other, Transform) and
                                 self.tx == other.tx and
                                 self.ty == other.ty and
                                 self.tz == other.tz and
                                 self.rx == other.rx and
                                 self.ry == other.ry and
                                 self.rz == other.rz and
                                 self.s  == other.s)

    def inverse(self, name=''):
        '''Return the inverse of this transform.

           @keyword name: Optional, unique name (string).

           @return: Inverse (Transform).

           @raise NameError: If transform name already exists.
        '''
        return Transform(name=name or (self.name + 'Inverse'),
                         tx=-self.tx, ty=-self.ty, tz=-self.tz,
                         sx=-self.sx, sy=-self.sy, sz=-self.sz, s=-self.s)

    def toStr(self, prec=5):  # PYCHOK expected
        '''Return this transform as a string.

           @keyword prec: Optional number of decimals, unstripped (int).

           @return: Transform attributes (string).
        '''
        return self._fStr(prec, 'tx', 'ty', 'tz',
                                'rx', 'ry', 'rz', 's', 's1',
                                'sx', 'sy', 'sz')

    def transform(self, x, y, z, inverse=False):
        '''Transform a (geocentric) Cartesian point, forward or inverse.

           @param x: X coordinate (meter).
           @param y: Y coordinate (meter).
           @param z: Z coordinate (meter).
           @keyword inverse: Optional direction, forward or inverse (bool).

           @return: 3-Tuple (x, y, z) transformed.
        '''
        if inverse:
            xyz = -1, -x, -y, -z
            _s1 = self.s1 - 2  # negative inverse: -(1 - s * 1.e-6)
        else:
            xyz =  1,  x,  y,  z
            _s1 = self.s1
        # x', y', z' = (.tx + x * .s1 - y * .rz + z * .ry,
        #               .ty + x * .rz + y * .s1 - z * .rx,
        #               .tz - x * .ry + y * .rx + z * .s1)
        return (fdot(xyz, self.tx,      _s1, -self.rz,  self.ry),
                fdot(xyz, self.ty,  self.rz,      _s1, -self.rx),
                fdot(xyz, self.tz, -self.ry,  self.rx,      _s1))


# <http://wikipedia.org/wiki/Helmert_transformation> from WGS84
Transforms._assert(
    BD72           = Transform('BD72', tx=106.868628, ty=-52.297783, tz=103.723893,
                     # <http://www.ngi.be/FR/FR4-4.shtm> ETRS89 == WG84
                     # <http://georepository.com/transformation_15929/BD72-to-WGS-84-3.html>
                                       sx=-0.33657,   sy= -0.456955, sz= -1.84218,
                                        s= 1.2727),
    Bessel1841     = Transform('Bessel1841', tx=-582.0,  ty=-105.0, tz=-414.0,
                                             sx=  -1.04, sy= -0.35, sz=   3.08,
                                              s=  -8.3),
    Clarke1866     = Transform('Clarke1866', tx=8, ty=-160, tz=-176),
    DHDN           = Transform('DHDN', tx=-591.28,  ty=-81.35,   tz=-396.39,
                                       sx=   1.477, sy= -0.0736, sz=  -1.458,
                                        s=  -9.82),  # Germany
    ED50           = Transform('ED50', tx=89.5, ty=93.8, tz=123.1,
                     # <http://geonet.esri.com/thread/36583> sz=-0.156
                     # <http://github.com/chrisveness/geodesy/blob/master/latlon-ellipsoidal.js>
                     # <http://www.gov.uk/guidance/oil-and-gas-petroleum-operations-notices#pon-4>
                                                         sz=  0.156, s=-1.2),
    Irl1965        = Transform('Irl1965', tx=-482.530, ty=130.596, tz=-564.557,
                                          sx=   1.042, sy=  0.214, sz=   0.631,
                                           s=  -8.15),
    Irl1975        = Transform('Irl1975', tx=-482.530, ty=130.596, tz=-564.557,
                     # XXX rotation signs may be opposite, to be checked
                                          sx=  -1.042, sy= -0.214, sz=  -0.631,
                                           s=  -1.1),
    Krassovski1940 = Transform('Krassovski1940', tx=-24.0,  ty=123.0,  tz=94.0,
                                                 sx= -0.02, sy=  0.26, sz= 0.13,
                                                  s= -2.423),  # spelling
    Krassowsky1940 = Transform('Krassowsky1940', tx=-24.0,  ty=123.0,  tz=94.0,
                                                 sx= -0.02, sy=  0.26, sz= 0.13,
                                                  s= -2.423),  # spelling
    MGI            = Transform('MGI', tx=-577.326, ty=-90.129, tz=-463.920,
                                      sx=   5.137, sy=  1.474, sz=   5.297,
                                       s=  -2.423),  # Austria
    NAD27          = Transform('NAD27', tx=8, ty=-160, tz=-176),
    NAD83          = Transform('NAD83', tx= 1.004,  ty=-1.910,   tz=-0.515,
                                        sx= 0.0267, sy= 0.00034, sz= 0.011,
                                         s=-0.0015),
    NTF            = Transform('NTF', tx=-168, ty= -60, tz=320),  # XXX verify
    OSGB36         = Transform('OSGB36', tx=-446.448,  ty=125.157,  tz=-542.060,
                                         sx=  -0.1502, sy= -0.2470, sz=  -0.8421,
                                          s=  20.4894),
    TokyoJapan     = Transform('TokyoJapan', tx=148, ty=-507, tz=-685),
    WGS72          = Transform('WGS72', tz=-4.5, sz=0.554, s=-0.22),
    WGS84          = Transform('WGS84'),  # unity
)


class Datum(_Based):
    '''Ellipsoid and transform parameters for an earth model.
    '''
    _ellipsoid = Ellipsoids.WGS84  #: (INTERNAL) Default ellipsoid (L{Ellipsoid}).
    _transform = Transforms.WGS84  #: (INTERNAL) Default transform (L{Transform}).

    def __init__(self, ellipsoid, transform=None, name=''):
        '''New datum.

           @param ellipsoid: The ellipsoid (L{Ellipsoid}).
           @keyword transform: Optional transform (L{Transform}).
           @keyword name: Optional, unique name (string).

           @raise NameError: If datum name already exists.

           @raise TypeError: If ellipsoid is not an L{Ellipsoid}
                             or transform is not a L{Transform}.
        '''
        self._ellipsoid = ellipsoid or Datum._ellipsoid
        if not isinstance(self.ellipsoid, Ellipsoid):
            raise TypeError('%s not an %s: %r' % ('ellipsoid', Ellipsoid.__name__, self.ellipsoid))

        self._transform = transform or Datum._transform
        if not isinstance(self.transform, Transform):
            raise TypeError('%s not a %s: %r' % ('transform', Transform.__name__, self.transform))

        self._register(Datums, name or self.transform.name or self.ellipsoid.name)

    def __eq__(self, other):
        '''Compare this and an other datum.

           @param other: The other datum (L{Datum}).

           @return: True if equal (bool)
        '''
        return self is other or (isinstance(other, Datum) and
                                 self.ellipsoid == other.ellipsoid and
                                 self.transform == other.transform)

    @property
    def ellipsoid(self):
        '''Get this datum's ellipsoid (L{Ellipsoid}).
        '''
        return self._ellipsoid

    @property
    def isEllipsoidal(self):
        '''Check whether this datum is ellipsoidal (bool).
        '''
        return self._ellipsoid.isEllipsoidal

    @property
    def isSpherical(self):
        '''Check whether this datum is spherical (bool).
        '''
        return self._ellipsoid.isSpherical

    def toStr(self, **unused):  # PYCHOK expected
        '''Return this datum as a string.

           @return: Datum attributes (string).
        '''
        t = []
        for a in ('ellipsoid', 'transform'):
            v = getattr(self, a)
            t.append('%s=%ss.%s' % (a, v.__class__.__name__, v.name))
        return ', '.join(['name=%r' % (self.name,)] + t)

    @property
    def transform(self):
        '''Get this datum's transform (L{Transform}).
        '''
        return self._transform


# Datums with associated ellipsoid and Helmert transform parameters
# to convert from WGS84 into the given datum.  More are available at
# <http://earth-info.nga.mil/GandG/coordsys/datums/NATO_DT.pdf> and
# <XXX://www.fieldenmaps.info/cconv/web/cconv_params.js>.
Datums._assert(
    # Belgian Datum 1972, based on Hayford ellipsoid.
    # <http://nl.wikipedia.org/wiki/Belgian_Datum_1972>
    # <http://spatialreference.org/ref/sr-org/belge-1972-belgian-
    #         lambert-72-corrected-transformation-parameters/>
    BD72           = Datum(Ellipsoids.Intl1924, Transforms.BD72),
    # Germany <http://wikipedia.org/wiki/Bessel-Ellipsoid>
    #         <http://wikipedia.org/wiki/Helmert_transformation>
    DHDN           = Datum(Ellipsoids.Bessel1841, Transforms.DHDN),

    # <http://www.gov.uk/guidance/oil-and-gas-petroleum-operations-notices#pon-4>
    ED50           = Datum(Ellipsoids.Intl1924, Transforms.ED50),

    # <http://wikipedia.org/wiki/GRS_80>
    GRS80          = Datum(Ellipsoids.GRS80, Transforms.WGS84, name='GRS80'),

    # <http://osi.ie/OSI/media/OSI/Content/Publications/transformations_booklet.pdf>
    Irl1975        = Datum(Ellipsoids.AiryModified, Transforms.Irl1975),

    # Germany <http://wikipedia.org/wiki/Helmert_transformation>
    Krassovski1940 = Datum(Ellipsoids.Krassovski1940, Transforms.Krassovski1940),  # spelling
    Krassowsky1940 = Datum(Ellipsoids.Krassowsky1940, Transforms.Krassowsky1940),  # spelling

    # Austria <http://de.wikipedia.org/wiki/Datum_Austria>
    MGI            = Datum(Ellipsoids.Bessel1841, Transforms.MGI),

    # <http://wikipedia.org/wiki/Helmert_transformation>
    NAD27          = Datum(Ellipsoids.Clarke1866, Transforms.NAD27),

    # NAD83 (2009) == WGS84 - <http://www.uvm.edu/giv/resources/WGS84_NAD83.pdf>
    # (If you *really* must convert WGS84<->NAD83, you need more than this!)
    NAD83          = Datum(Ellipsoids.GRS80, Transforms.NAD83),

    #  Nouvelle Triangulation Francaise (Paris)  XXX verify
    NTF            = Datum(Ellipsoids.Clarke1880IGN, Transforms.NTF),

    # <http://www.ordnancesurvey.co.uk/docs/support/guide-coordinate-systems-great-britain.pdf>
    OSGB36         = Datum(Ellipsoids.Airy1830, Transforms.OSGB36),

    # Germany <http://wikipedia.org/wiki/Helmert_transformation>
    Potsdam        = Datum(Ellipsoids.Bessel1841, Transforms.Bessel1841, name='Potsdam'),

    # XXX psuedo-ellipsoids for spherical LatLon
    Sphere         = Datum(Ellipsoids.Sphere, Transforms.WGS84, name='Sphere'),

    # <http://www.geocachingtoolbox.com?page=datumEllipsoidDetails>
    TokyoJapan     = Datum(Ellipsoids.Bessel1841, Transforms.TokyoJapan),

    # <http://www.icao.int/safety/pbn/documentation/eurocontrol/eurocontrol%20wgs%2084%20implementation%20manual.pdf>
    WGS72          = Datum(Ellipsoids.WGS72, Transforms.WGS72),

    WGS84          = Datum(Ellipsoids.WGS84, Transforms.WGS84),
)


if __name__ == '__main__':

    for E in (Datums.WGS84.ellipsoid, Ellipsoids.Sphere, Ellipsoids.SpherePopular):
        e = (E.a - E.b) / (E.a + E.b) - E.n
        if E.f:
            f = 'f=1/%.10f' % (1 / E.f,)
        else:
            f = 'f=N/A'
        t = (E.toStr(prec=10),
            'A=%r, e=%.13e, %s, n=%.10f(%.10e)' % (E.A, E.e, f, E.n, e),
            'Alpha6=%r' % (E.Alpha6,),
            'Beta6=%r' % (E.Beta6,))
        print('\nEllipsoid.%s: %s' % (E.name, ',\n    '.join(t)))

    # __doc__ of this file
    for e in (Datums, Ellipsoids, Transforms):
        e = [''] + repr(e).split('\n')
        print('\n@var '.join(e))

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

# Ellipsoid.WGS84: name='WGS84', a=6378137, b=6356752.3142499998, f_=298.257223563, f=0.0033528107, e=0.0818191908, e2=0.00669438, e22=0.0067394967, R=6371008.7714166669, Rm=6367435.6797186071, R2=6371007.180920884, R3=6371000.7900107643, Rr=6367449.1458250266,
#        A=6367449.145823415, e=8.1819190842621e-02, f=1/298.2572235630, n=0.0016792204(-3.7914875232e-13),
#        Alpha6=(0, 0.0008377318206244698, 7.608527773572307e-07, 1.1976455033294527e-09, 2.4291706072013587e-12, 5.711757677865804e-15, 1.4911177312583895e-17),
#        Beta6=(0, 0.0008377321640579486, 5.905870152220203e-08, 1.6734826652839968e-10, 2.1647980400627059e-13, 3.7879780461686053e-16, 7.2487488906941545e-19)

# Ellipsoid.Sphere: name='Sphere', a=6371008.7714149999, b=6371008.7714149999, f_=0, f=0, e=0, e2=0, e22=0, R=6371008.7714149999, Rm=6371008.7714149999, R2=6371008.7714149999, R3=6371008.7714149999, Rr=6371008.7714149999,
#        A=6371008.771415, e=0.0000000000000e+00, f=N/A, n=0.0000000000(0.0000000000e+00),
#        Alpha6=(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
#        Beta6=(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# Ellipsoid.SpherePopular: name='SpherePopular', a=6378137, b=6378137, f_=0, f=0, e=0, e2=0, e22=0, R=6378137, Rm=6378137, R2=6378137, R3=6378137, Rr=6378137,
#        A=6378137.0, e=0.0000000000000e+00, f=N/A, n=0.0000000000(0.0000000000e+00),
#        Alpha6=(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
#        Beta6=(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
