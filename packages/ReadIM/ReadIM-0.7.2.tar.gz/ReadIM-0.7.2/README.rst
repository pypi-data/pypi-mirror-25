Overview
========
ReadIM is a Python package to read and write DaVis Images and Vectors DaVis V8.
It contains C++ libraries provided by `LaVision GMBH <http://www.lavision.de/en/>`_
and a low level interface wrapper for Python.


Installation
============
The libraries have been compiled successfully on Windows platforms with 64-bit and 32-bit python.
Successfully installed with latest 32 and 64 bit versions of WinPython including:

2.7, 3.3 and 3.4
Do either:

>>> pip install ReadIM

If this fails you will need to compile yourself. Clone the source and run the following.

>>> python setup.py build install
>>> python setup.py test

If the test passes then all should be okay.


Usage
=====

To load a .vc7 file run::

    >>> vbuff, vatts   =  ReadIM.extra.get_Buffer_andAttributeList('filename.vc7')
    >>> v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)

similarly for a .im7 file run::

    >>> vbuff, vatts   =  ReadIM.extra.get_Buffer_andAttributeList('filename.im7')
    >>> v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)


Writing files
-------------
>>> atts = ReadIM.load_AttributeList({'attribute':'value'})
>>> ReadIM.WriteIM7('saved_file.im7', True, buff, atts.next)

Finally, memory cleanup is not automatic. To prevent memory leaks do the following:

>>> del(vbuff)
>>> ReadIM.DestroyBuffer(buff)
>>> ReadIM.DestroyAttributeListSafe(atts)


For higher level access to DaVis files the IM package is available at:
https://bitbucket.org/fleming79/im