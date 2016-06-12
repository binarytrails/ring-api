from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

# generating shared library
setup(name='dring',
      ext_modules = cythonize(Extension(
          'dring',
          sources=['wrappers/dring.pyx',
              'cpp/callback_client.cpp',
              'cpp/callback_configurationmanager.cpp'],
          language='c++',
          extra_compile_args=['-std=c++11'],
          extra_link_args=['-std=c++11'],
          include_dirs = ['/usr/include/dring',
              'extra/hpp/', 'cpp/'],
          libraries=['ring'],
      )),
      cmdclass = {'build_ext' : build_ext}
)
