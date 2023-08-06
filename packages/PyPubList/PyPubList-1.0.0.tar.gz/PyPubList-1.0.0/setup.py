"""
Setup script for PyPubList
"""

from distutils.core import setup

setup(name = "PyPubList",
      version = "1.0.0",
      description = "Python tool to generate publication lists for JSPS KAKENHI applications",
      author = "Akira Okumura",
      author_email = "oxon@mac.com",
      url = 'https://github.com/akira-okumura/PyPubList/',
      license = 'BSD License',
      platforms = ['MacOS :: MacOS X', 'POSIX'],
      py_modules = ["publist"],
      classifiers = ['Topic :: Scientific/Engineering :: Astronomy',
                     'Topic :: Scientific/Engineering :: Physics',
                     'Development Status :: 5 - Production/Stable',
                     'Programming Language :: Python']
      )
