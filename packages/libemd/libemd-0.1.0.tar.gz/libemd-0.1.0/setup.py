"""
A library for empirical mode decomposition and it's variations.

libemd is an open-source Python library for the empirical mode
decomposition signal processing technique and it's variations.

Lots of other packages exist for EMD in Python. So why should you use
libemd?

  - libemd is an original Pythonic implementation of the algorithm. 
    Other existing libraries borrow heavily from unlicensed Matlab
    source code without attribution. libemd does not.

  - libemd has Cython implementations of the algorithms in its roadmap,
    specifically designed for use cases with high sampling frequencies
    that demand performance.

  - libemd ships with a permissive, compatible open-source license.
"""

import os
from distutils.core import setup


MAJOR = 0
MINOR = 1
REVISION = 0
VERSION = '{}.{}.{}'.format(MAJOR, MINOR, REVISION)

DOCLINES = __doc__.split('\n')

CLASSIFIERS = """
Development Status :: 2 - Pre-Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python :: 3.6
Operating System :: Unix

"""

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')


setup(
    name='libemd',
    packages=['libemd'],
    version=VERSION,
    description=DOCLINES[1],
    long_description='\n'.join(DOCLINES[3:]),
    license='BSD-2-Clause',
    author='Richard Berry',
    author_email='rjsberry@protonmail.com',
    url='https://github.com/rjsberry/libemd',
    download_url='https://github.com/rjsberry/libemd/archive/{}.tar.gz'.format(VERSION),
    platforms=['Linux', 'UNIX'],
    install_requires=['numpy', 'scipy'],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f]
)
