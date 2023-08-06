#! /usr/bin/env python

import os
import io
from distutils.core import setup, Extension
# from setuptools import setup, Extension
import numpy as np

# NOTE: to compile, run in the current directory
# python setup.py build_ext --inplace
# python setup.py develop

try:
    from Cython.Build import cythonize
    # from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


cmdclass = {}
ext_modules = []

here = os.path.abspath(os.path.dirname(__file__))
sourcefiles = ['linear_binning/linear_binning_impl.cpp',
               'linear_binning/linear_binning.pyx']
include_path = [np.get_include(), 'linear_binning']

if use_cython:
    extensions = \
        Extension("linear_binning.linear_binning",
                  sources=sourcefiles,
                  include_dirs=include_path,
                  language='c++')
else:
    sourcefiles[1] = sourcefiles[1].replace('.pyx', '.cpp')
    extensions = \
        Extension("linear_binning.linear_binning",
                  sources=sourcefiles,
                  include_dirs=include_path,
                  language='c++')


if use_cython:
    ext_modules += \
        cythonize(extensions, compiler_directives={'embedsignature': True,
                                                   'profile': True})
else:
    ext_modules += [extensions]

long_description = read('README.rst', 'CHANGES.txt')

setup(
    name="linear_binning",
    version='1.1.0',
    url='https://github.com/jhetherly/linear_binning',
    license='MIT',
    author='Jeff Hetherly',
    author_email='jeffrey.hetherly@gmail.com',
    platforms='any',
    description='Python function for performing a linear binning',
    long_description=long_description,
    install_requires=['numpy'],
    packages=['linear_binning'],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    include_dirs=[np.get_include(), 'linear_binning']
)
