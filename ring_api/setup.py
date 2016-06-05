from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

# generating shared library
setup(name='dring',
      ext_modules = cythonize(Extension(
          'dring',
          ['wrappers/dring.pyx'],
          language='c++',
          extra_compile_args=['-std=c++11'],
          extra_link_args=['-std=c++11'],
          include_dirs = ['/usr/include/dring'],
          libraries=['ring'],
      )),
      cmdclass = {'build_ext' : build_ext}
)
