# Filename: setup.py
# Author: Weiyang Wang <wew168@ucsd.edu>
# Description: setup utility for the usb1208fs python library.
#              Based on Warren Jaspers' C drivers.
#              Referenced Guillaume Lepert's python wrapper for USB26xx series.

from setuptools import setup, Extension, find_packages
from distutils.command.sdist import sdist as _sdist

import numpy

classifiers = [
    "Development Status :: 5 - Production/Stable",
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: C',
    'Programming Language :: Cython',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering'
]

cmdclass = { }

class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        cythonize(['usb1208fs/usb1208fs.pyx'])
        _sdist.run(self)

cmdclass['sdist'] = sdist

try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
    usb1208fs = Extension("usb1208fs",
            sources = ["usb1208fs/usb1208fs.c"],
            library_dirs = ['usb1208fs','/usr/local/lib'],
            include_dirs = ['usb1208fs', numpy.get_include(), \
                '/usr/lib64/python/site-packages/Cython/Includes'],
            libraries = ['usb-1.0', 'mccusb', 'hidapi-libusb', 'm', 'c'])
else:
    use_cython = True
    usb1208fs = Extension("usb1208fs",
                sources = ["usb1208fs/usb1208fs.pyx"],
                library_dirs = ['usb1208fs','/usr/local/lib'],
                include_dirs = ['usb1208fs', numpy.get_include(), \
                    '/usr/lib64/python/site-packages/Cython/Includes'],
                libraries = ['usb-1.0', 'mccusb', 'hidapi-libusb', 'm', 'c'])
    cmdclass.update({ 'build_ext': build_ext })


setup(
    name = 'usb1208fs',
    version = '0.2.0r0',
    description = "Python drivers for Measurement Computing USB1208FS on linux",
    author = 'Weiyang Wang',
    author_email = 'wew168@ucsd.edu',
    url = 'https://github.com/Flasew/pyusb1208fs',
    long_description = """Python wrapper of the C-driver of MCC USB1208FS data acquisition card written by Warren Jaspers.

    Functionality includes analog/digital input/output, analog input/output scans, counter, etc.
    See Warren Jaspers' C-library for more details.

    This module is mostly just a python wrapper of the original C-driver; some object-orientated
    concepts and python list support were added for a more user-friendly interface.

    This module requires Warren Jaspers' C drivers to be already installed (see ftp://lx10.tx.ncsu.edu/pub/Linux/drivers/USB/)
    """,
    cmdclass = cmdclass,
    #packages = find_packages(),
    #include_package_data=True,
    zip_safe = False,
    ext_modules = cythonize(usb1208fs) if use_cython else usb1208fs,
    install_requires = ['numpy'],
    platforms=['linux'],
    classifiers = classifiers
)



