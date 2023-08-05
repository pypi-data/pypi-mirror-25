from setuptools import setup, Extension
import sys

with open('README.rst', 'r') as f:
    readme = f.read()

setup_args = {
    'name': 'geolambert',
    'version': '0.1.1',
    'packages': ['geolambert'],
    'description': 'A Python library and provides functions to covert geographical corrdinates from LambertIIe/Lambert93 systems to WGS84',
    'long_description': readme,
    'author': 'chengs',
    'author_email': 'cgs.sjtu@gmail.com',
    'url': 'https://github.com/chengs/geolambert-python',
    'license': 'LGPL',
    'classifiers': (
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    )
}

if '--cython' in sys.argv:
    del sys.argv[sys.argv.index('--cython')]

    from Cython.Distutils import build_ext
    from Cython.Build import cythonize

    setup_args['ext_modules'] = cythonize(
        [Extension('geolambert.clambert', ["geolambert/clambert/clambert.pyx"])])
    setup_args['cmdclass'] = {'build_ext': build_ext}
else:
    setup_args['ext_modules'] = [
        Extension('geolambert.clambert', ["geolambert/clambert/clambert.c"])]

setup(**setup_args)
