from __future__ import print_function, absolute_import
if __name__ == '__main__':
    from clambert import xyToWgs84
else:
    from .clambert import xyToWgs84


def _docstring_example(x, y):
    """
    This is an example of Google style.

    Args:
        x: This is the first param.
        y: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """


def _check_input(x, y):
    if isinstance(x, int):
        x = x * 1.0
    if isinstance(y, int):
        y = y * 1.0

    assert isinstance(x, float)
    assert isinstance(y, float)

    return x, y


def lambert93_to_wgs84(x, y):
    # type (float, float) -> (float, float)
    """
    Covert a corrdinate (x,y) from Lambert 93 to WGS84 (lon/lat in radius).

    Args:
        x (float): easting
        y (float): northing 

    Returns:
        lat, lon (float, float): WGS84 corrdinate in radius
        
    >>> print("%.4f, %.4f" % lambert93_to_wgs84(668832.5384, 6950138.7285))
    2.5687, 49.6496
    >>> print("%.4f, %.4f" % lambert93_to_wgs84(668850, 6950151))
    2.5689, 49.6497
    """
    _x, _y = _check_input(x, y)
    lon, lat = xyToWgs84(x, y, 5) #LAMBERT_93=5
    return lon, lat

def lambertIIe_to_wgs84(x, y):
    # type (float, float) -> (float, float)
    """
    Covert a corrdinate (x,y) from Lambert II etendu to WGS84 (lon/lat in radius).

    Args:
        x (float): Easting
        y (float): Northing 

    Returns:
        lat, lon (float, float): WGS84 corrdinate in radius

    >>> print("%.4f, %.4f" % lambertIIe_to_wgs84(73150, 2396665))
    -4.7802, 48.3541
    """
    _x, _y = _check_input(x, y)
    # TODO: compute lon lat
    lon, lat = xyToWgs84(x, y, 4) #LAMBERT_II_E=4
    return lon, lat

if __name__ == '__main__':
    import doctest
    doctest.testmod(raise_on_error=True)