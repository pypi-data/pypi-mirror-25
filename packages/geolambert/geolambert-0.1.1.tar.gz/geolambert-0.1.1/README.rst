.. -*- mode: rst -*-

|Travis|_ |Python27|_ |Python35|_

.. |Travis| image:: https://travis-ci.org/chengs/geolambert-python.svg?branch=master
.. _Travis: https://travis-ci.org/chengs/geolambert-python

.. |Python27| image:: https://img.shields.io/badge/python-2.7-blue.svg
.. _Python27: https://badge.fury.io/py/geolambert

.. |Python35| image:: https://img.shields.io/badge/python-3.5-blue.svg
.. _Python35: https://badge.fury.io/py/geolambert

.. |PyPi| image:: https://badge.fury.io/py/geolambert.svg
.. _PyPi: https://badge.fury.io/py/geolambert


geolambert-python
=================

geolambert-python is a Python library and provides functions to covert 
geographical corrdinates from LambertIIe/Lambert93 systems to WGS84 using
IGN Algorithms. C codes (`lambert.c <geolambert/clambert/lambert.c>`_, `lambert.h <geolambert/clambert/lambert.h>`_) come from `yageek/lambert <https://github.com/yageek/lambert>`_.

Website: https://github.com/chengs/geolambert-python/

Usage
------------

>>> from geolambert import lambert93_to_wgs84, lambertIIe_to_wgs84
>>> lambert93_to_wgs84(668832.5384, 6950138.7285)
(2.5686536326051743, 49.649610985851474)
>>> lambertIIe_to_wgs84(73150, 2396665)
(-4.780198557157784, 48.354052821116824)



Installation
------------

Dependencies
~~~~~~~~~~~~

geolambert-python requires:

- Python (>= 2.7 or >= 3.3)

For development, cython>=0.26.1 is required.

User installation
~~~~~~~~~~~~~~~~~

To install geolambert-python using ``pip`` ::

    pip install geolambert

To install geolambert-python from source ::

    git clone https://github.com/chengs/geolambert-python/
    cd geolambert-python
    python setup.py install
    
or install with compling codes using `Cython <http://cython.org/#download>`_ ::

    python setup.py install --cython
    
Alternatives
------------

- C++: https://github.com/yageek/lambert
- Jave: https://github.com/yageek/lambert-java
- Python: https://github.com/yageek/lambert-python
- Python: https://pypi.python.org/pypi/pyproj + PROJ.4
