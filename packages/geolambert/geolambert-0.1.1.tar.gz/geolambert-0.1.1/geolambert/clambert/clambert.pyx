# cython wrapper of https://github.com/yageek/lambert

cdef extern from "lambert.c":
    ctypedef enum YGLambertZone:
        LAMBERT_I=0
        LAMBERT_II=1
        LAMBERT_III=2
        LAMBERT_IV=3
        LAMBERT_II_E=4
        LAMBERT_93=5


    ctypedef enum CoordUnit:
        DEGREE, GRAD, RADIAN, METER

    ctypedef struct YGPoint:
        double x
        double y
        double z
        CoordUnit unit

    YGPoint YGPointConvertWGS84(YGPoint point, YGLambertZone zone)
    YGPoint YGPointToDegree(YGPoint pt)


cdef YGPoint _YGMeterPoint(double x, double y, double z):
    return YGPoint(x=x, y=y, z=z, unit=CoordUnit.METER)


def xyToWgs84(double x, double y, YGLambertZone system):
    lambert_point = _YGMeterPoint(x,y,0.)
    gps_point = YGPointToDegree(YGPointConvertWGS84(lambert_point, system))
    return gps_point.x, gps_point.y