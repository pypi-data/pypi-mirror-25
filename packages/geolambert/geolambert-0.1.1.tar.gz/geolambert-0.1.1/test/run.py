import geolambert

def test():
    """
    >>> print("%.4f, %.4f" % geolambert.lambert93_to_wgs84(668832.5384, 6950138.7285))
    2.5687, 49.6496
    >>> print("%.4f, %.4f" % geolambert.lambert93_to_wgs84(668850, 6950151))
    2.5689, 49.6497
    >>> print("%.4f, %.4f" % geolambert.lambertIIe_to_wgs84(73150, 2396665))
    -4.7802, 48.3541
    """
    return True

if __name__ == '__main__':
    import doctest
    doctest.testmod(raise_on_error=True)