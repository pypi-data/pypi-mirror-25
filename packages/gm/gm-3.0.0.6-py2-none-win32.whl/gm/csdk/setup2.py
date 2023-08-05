# coding=utf-8
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("c_sdk",
                     ["c_sdk.pyx"],
                     language='c++',
                     include_dirs=['.'],
                     library_dirs=['./lib'],
                     libraries=['gm3-c']
                     )]

setup(
  name='c_sdk',
  cmdclass={'build_ext': build_ext},
  ext_modules=ext_modules,
)
