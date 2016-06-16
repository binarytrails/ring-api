from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

# generating shared library
setup(name='dring_cython',
      ext_modules = cythonize(Extension(
          'dring_cython', # library name
          sources=['wrappers/dring_cython.pyx',
              'callbacks/cb_client.cpp'],
          language='c++',
          extra_compile_args=['-std=c++11'],
          extra_link_args=['-std=c++11'],
          include_dirs = ['/usr/include/dring',
              'extra/hpp/', 'callbacks/', 'wrappers/'],
          libraries=['ring'],
      )),
      cmdclass = {'build_ext' : build_ext}
)
