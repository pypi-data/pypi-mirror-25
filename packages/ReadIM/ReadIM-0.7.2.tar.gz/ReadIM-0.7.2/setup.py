#!/usr/bin/env python

"""
setup.py file readim

run python setup.py [operation]

operations
----------
swig    : Rerun swig. Not required unless changes to code.
build | install | bdist_wininst etc: typical build commands.
sdist : create a source distribution. (python setup.py sdist --formats=gztar)
test: run the test suite.


"""

version = '0.7.2'

long_description = """
Overview
========
ReadIM is a Python package to read and write DaVis Images and Vectors DaVis V8.
It contains C++ libraries provided by `LaVision GMBH <http://www.lavision.de/en/>`_
and a low level interface wrapper for Python.

Installation
============
The libraries have been compiled successfully on Windows platforms with 64-bit and 32-bit python.
You can install uising pip provided a compiler is available (built in to most common distributions).
The latest source is available here: https://bitbucket.org/fleming79/readim).

Higher level access is available using the package "IM" available here:
https://bitbucket.org/fleming79/im.
"""

from setuptools import setup, Extension

import subprocess, sys, os
import glob
import io


script_args = sys.argv[1:]

if script_args[0] == 'test':
    from numpy.testing import run_module_suite
# Remove the current directory so that ReadIM will load properly
    pth = sys.path.pop(0)
    testFileDir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ReadIM/tests'))
    assert os.path.isdir(testFileDir)
    sys.path.insert(0, testFileDir)

    import test_ReadIM
    run_module_suite('test_ReadIM', ['-f'])

elif script_args[0] == 'swig':
    try:
        args = ['swig', '-python','-c++' ,'-IReadIM/src','ReadIM/core.i']
        p= subprocess.check_call(args)
    except:
        print ('unable to run swig! is it installed?')

else:

    scs = ['ReadIMX.cpp', 'ReadIM7.cpp', 'swigExtras.cpp',
            'zlib/adler32.c','zlib/deflate.c','zlib/infcodes.c',
            'zlib/inflate.c','zlib/infutil.c', 'zlib/uncompr.c',
             'zlib/compress.c','zlib/infblock.c','zlib/inffast.c',
            'zlib/inftrees.c','zlib/trees.c','zlib/zutil.c']

    scs = ['ReadIM/src/'+s for s in scs]
    scs = ['ReadIM/core_wrap.cxx'] + scs
    for s in scs:
        assert os.path.isfile(s)

    extra_compile_args  =['-IReadIM/src']

    ReadIMX_module = Extension('ReadIM._core',
    # Auto SWIG doesn't work because the files are outputs 'core.py' to the current directory not ReadIM
    ##                            ['core.i'], swig_opts=['-c++', '-IReadIM/src'],
    # Manual SWIG
                                sources=scs,
                                extra_compile_args = extra_compile_args,
                                )

    description      = 'Read and write native DaVis images and vectors filetypes VC7 and IM7'

    setup (name = 'ReadIM',
            description = description,
           version      = version,
           author       = "Alan Fleming + LaVision",
           author_email =  'alanf@amc.edu.au',
           url          = 'https://bitbucket.org/fleming79/readim',
           ext_modules  = [ReadIMX_module],
           packages     = ['ReadIM'],
           package_data = {'ReadIM':['sample_files/*.*']},
           include_package_data = True,
           script_args          = script_args,

    long_description=long_description,

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords = 'IM7 VC7 DaVis LaVision FileIO PIV',
           )



