from setuptools import setup, find_packages
from setuptools.extension import Extension
from sys import platform
import os

USE_CYTHON = True

try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
except ImportError:
    USE_CYTHON = False

# Compile with full optimization
GCC_ARGS = ['-std=c++11', '-O3']
MSVC_ARGS = ['-Ox']

def cython_or_cpp(ext):
    # Specify the correct C++ compiler
    for e in ext:
        if platform.startswith('win32'):        # Windows
            e.extra_compile_args = MSVC_ARGS
        elif platform.startswith('darwin'):     # Mac OS X
            os.environ["CC"] = "clang++"
            e.extra_compile_args = GCC_ARGS
        else:                                   # Linux
            e.extra_compile_args = GCC_ARGS

    if USE_CYTHON:
        return cythonize(ext)
    else:
        for e in ext:        
            for i, j in enumerate(e.sources):
                e.sources[i] = j.replace('.pyx', '.cpp')
        return ext

extensions = cython_or_cpp([
    Extension(
        "csvmorph.parser",
        sources=["csvmorph/parser.pyx"],
        language="c++",
    ),
    Extension(
        "csvmorph.json_streamer",
        sources=["csvmorph/json_streamer.pyx"],
        language="c++",
    ),
])

# Enable creating Sphinx documentation
for ext in extensions:
    ext.cython_directives = {
        'embedsignature': True,
        'binding': True,
        'linetrace': True}

setup(
    name='csvmorph',
    version='1.0.1a2',
    description=('A blazing fast library for manipulating and peeking into '
                 'CSV files'),
    long_description=('(Currently in Pre-Alpha, AKA not very stable) A blazing fast C++ based library '
                      'for quickily manipulating and getting summary statistics from '
                      'CSV files. Intended for Python 3.'),
    url='https://github.com/vincentlaucsb/csvmorph/',
    author='Vincent La',
    author_email='vincela9@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    entry_points='''
        [console_scripts]
        csvpeek=csvmorph.cli:csvpeek
        csvsummary=csvmorph.cli:csvsummary
        csv2json=csvmorph.cli:csv2json
        json2csv=csvmorph.cli:json2csv
    ''',
    keywords='convert txt csv json text delimited',
    packages=find_packages(exclude=['setup', 'tests*']),
    ext_modules = cython_or_cpp(extensions),
    include_package_data=True
)