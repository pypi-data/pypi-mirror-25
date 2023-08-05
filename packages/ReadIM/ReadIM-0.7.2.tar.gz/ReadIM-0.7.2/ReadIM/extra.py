from __future__ import division, print_function, absolute_import

__metaclass__ = type



from . import core
import os
import ctypes
import numpy as np
import inspect
import glob
import copy


__all__ = [ 'BunchMappable', 'ScaleTypeAlt', 'BufferTypeAlt', 'obj2dict',
            'createBuffer', 'get_Buffer_andAttributeList', 'newBuffer',
            'load_AttributeList', 'buffer_as_array', 'buffer_mask_as_array',
            'att2dict', 'DestroyAttributeListSafe']

class BunchMappable():
    """
    An object for iterative access to a mappable object. The keys must always
    be alpha_numeric
    """
    def __init__(self, mappable, immutable=False, str2num=None, parent=None, key=None):
        """str2num can be a method for converting strings to numbers.
        val = str2num(val). Not the converter must return values even if it cannot convert.
        """
        self._parent    = parent
        self._key       = key
        self._immutable = immutable


        super(BunchMappable, self).__setattr__('_mappable', mappable)

        if hasattr(mappable, 'items'):
            for key,val in list(mappable.items()):
                if key.find('_') == 0:
                    continue #Skip intended hidden files
                if hasattr(val, 'items'):
                    self.__dict__[key] = self.__class__(val, immutable=immutable,
                                          str2num=str2num, parent=self, key=key)
                else:
                    if str2num is None:
                        self.__dict__[key] = val
                    else:
                        self.__dict__[key] = str2num(val)


    def __repr__(self):
        return repr(self._mappable)

    def __str__(self):
        rep = ''
        for key, val in list(self.__dict__.items()):
            rep = rep + key + '\n'
        return '\n'.join(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __getattr__(self, name):
        return self[name] # just force a __getitem__ type error

    def __getitem__(self, key):

        if key in self.__dict__:
            return self.__dict__[key]

        else: # Get some info before raising an error
            parent = self
            depth = 0
            keys = [key]
            while hasattr(parent, '_parent'):
                depth += 1
                keys.append(getattr(parent,'_key', ''))
                parent = parent._parent or parent._mappable

            description = getattr(parent, 'filename', None) or repr(parent)
            keys.pop(-1)
            raise KeyError('"{0}" is missing from:"{1}" (depth={2})'.format(
                            '->'.join(reversed(keys)), description, depth))


    def __iter__(self):
        for key in sorted(self._mappable.keys()):
            yield key

    def __setattr__(self,name, value):
        if name in ['_immutable', '_key', '_parent']:
            super(BunchMappable, self).__setattr__(name,value)
        elif self._immutable:
            raise AttributeError('This Object is immutable')
        else:

            if name in self._mappable:
                self._mappable[name] = value
                try:
                    object.__setattr__(self, name, value)
                except AttributeError:
                    pass

    def get(self, key, arg=None):
        if key in self.__dict__:
            return self[key]
        else:
            return arg


class ScaleTypeAlt(BunchMappable):
    def __init__(self, scale):
        mappings = dict(
                    description = str(scale.description),
                    factor      = float(scale.factor),
                    offset      = float(scale.offset),
                    unit        = str(scale.unit),
                    )
        super(ScaleTypeAlt, self).__init__(mappings)

class BufferTypeAlt(BunchMappable):
    """ bufferType designed to replicate davis buffer type so that it is free of swig
    """

    def __init__(self, buff, DestroyBuffer = True, immutable=False,
                    str2num=None, parent=None, key=None):

        if isinstance(buff, dict):
            mappings= copy.deepcopy(buff)

        else:
            mappings = dict(
                        image_sub_type = int(buff.image_sub_type),
                        nf = int(buff.nf),
                        nx = int(buff.nx),
                        ny = int(buff.ny),
                        nz = int(buff.nz),
                        isFloat = int(buff.isFloat),
                        vectorGrid = int(buff.vectorGrid),
                        scaleX = ScaleTypeAlt(buff.scaleX).__dict__,
                        scaleY = ScaleTypeAlt(buff.scaleY).__dict__,
                        scaleI = ScaleTypeAlt(buff.scaleI).__dict__,
                        totalLines = int(buff.totalLines)
                        )

        super(BufferTypeAlt, self).__init__(mappings, immutable=immutable, str2num=str2num)

        # cleanup
        if (type(buff) == core.BufferType) and DestroyBuffer:
            core.DestroyBuffer(buff)

def obj2dict(obj, d):
    """
    Iteratively maps all obj.__dict__.items() into a dictionary.

    Parameters
    ----------
        obj: object
            f the obj as a nested dictionary of the same structure

    Returns
    -------
        dic: dict
    """
    for key, val in list(obj.__dict__.items()):
        if hasattr(val, '__dict__'):
            d[key] = {}
            obj2dict(val,d[key])
        # no hidden objects
        elif not key.find('_') == 0:
            d[key]=val


def createBuffer(buff, new=True):

    """
    Creates a new buffer in memory using buff details.

    Parameters
    ----------
    buff: BufferType | BufferTypeAlt
        Buffer to create

    Returns
    -------
    buffer: BufferType
        A new buffer in memory
        must be destroyed using ReadIM.core.DestroyBuffer
    error_code: int
        Error code corresponds to ReadIM.ERROR_CODES
    """

    if new or isinstance(buff, BufferTypeAlt):
        b = core.BufferType()
    else:
        b=buff

    b.nx = buff.nx
    b.ny = buff.ny
    b.nz = buff.nz
    b.nf = buff.nf
    b.isFloat = buff.isFloat
    b.vectorGrid = buff.vectorGrid
    b.image_sub_type = buff.image_sub_type
    error_code = core.CreateBuffer(b, b.nx ,b.ny, b.nz, b.nf,
                        b.isFloat, b.vectorGrid, b.image_sub_type)

    #transfer buffer info from v. Useful for writing files.
    for a in buff.__dict__:
        if a.find('scale') == 0:
            for aa in ['description','unit','factor','offset']:
                exec('b.%s.%s=buff.%s.%s'%tuple([a,aa]*2))

    return b, error_code

def get_Buffer_andAttributeList(filename, buff=None, atts=None):
    """
    Load 'filename' and return buffer and attribute list.

    Parameters
    ----------
    filename: str
        path to IM7 or VC7 file.
    buff: BufferType
        buffer to load into
    attts: AttributeList
        attribute list to load into

    Returns
    -------
    buff: BufferType
    atts: AttributeList
    out: (M, N) ndarray
        Will have shape of (len(data), len(widths)).

    Notes
    -----
        buff and atts must be destroyed manually.
        using ReadIM.core.DestroyBuffer and  ReadIM.core.DestroyAttributeList2

    """

    if not os.path.isfile(filename): raise IOError('file not found %s' %filename)

    if buff is None: buff = core.BufferType()
    if atts is None: atts = core.AttributeList()

    try:
        err = core.ReadSpec2(filename, buff, atts)
    except:
        core.DestroyBuffer(buff)

    if True:
        if err == core.IMREAD_ERR_FILEOPEN: raise IOError('File not found')
        elif err == core.IMREAD_ERR_HEADER: raise IOError('Error in header')
        elif err == core.IMREAD_ERR_FORMAT: raise IOError('Error in format')
        elif err == core.IMREAD_ERR_DATA:   raise IOError('Error while reading data')
        elif err == core.IMREAD_ERR_MEMORY: raise IOError('Error out of memory')
        elif err > 0: raise IOError('Unkown Error code: %s' % err)

    return buff, atts

def newBuffer(  window ,nx=None, ny=None, vectorGrid=24,
                image_sub_type=core.BUFFER_FORMAT_VECTOR_2D,
                frames=1, alternate_buff=True, scaleIoffset=0,
                scaleIfactor=1):
    """
    Create a new Buffer using a window to describe the extents.

    A new buffer will be created. By default a BufferTypeAlt will be returned
    otherwise a standard BufferType will be returned (not buffer will need to
    be destroyed).

    Parameters
    ----------
     window : 2x2 list
        [(x,y),(x,y)] --> [top left, bottom right]
     nx: int
        Number of columns
     ny: int
        Number of rows
     vectorGrid: int
        Reduction of nx * ny /vectorGrid (for BufferType vectors only)
     image_sub_type: int
        One of the following
         -11: 'BUFFER_FORMAT_RGB_32',
         -10: 'BUFFER_FORMAT_RGB_MATRIX',
         -6: 'BUFFER_FORMAT_FLOAT_VALID',
         -5: 'BUFFER_FORMAT_DOUBLE',
         -4: 'BUFFER_FORMAT_WORD',
         -3: 'BUFFER_FORMAT_FLOAT',
         -2: 'BUFFER_FORMAT_MEMPACKWORD',
         -1: 'BUFFER_FORMAT__NOTUSED',
         0: 'BUFFER_FORMAT_IMAGE',
         1: 'BUFFER_FORMAT_VECTOR_2D_EXTENDED',
         2: 'BUFFER_FORMAT_VECTOR_2D',
         3: 'BUFFER_FORMAT_VECTOR_2D_EXTENDED_PEAK',
         4: 'BUFFER_FORMAT_VECTOR_3D',
         5: 'BUFFER_FORMAT_VECTOR_3D_EXTENDED_PEAK'
     frames: int
        number of frames
    alternate_buffer: Bool
        The return object is by default a BufferTypeAlternate. Setting this to
        False will return a BufferType which must be destroyed after use to avoid
        memory issues.
        ReadIM.core.DestroyBuffer
    scaleIfactor: float
        Scale factor for intensity.
    scaleIoffset: float
        Offset for intensity.


    Returns
    -------
    buff: BufferTypeAlt | BufferType


    """

    if not nx:
        nx = window[1][0] - window[0][0]
    if not ny:
        ny = window[0][1] - window[1][1]

    buff = core.BufferType()

    buff.image_sub_type = int(image_sub_type)
    buff.nx = int(nx)
    buff.ny = int(ny) # * compN[buff.image_sub_type]
    buff.nz = 1
    buff.nf = int(frames)
    buff.isFloat = 1
    buff.vectorGrid = int(vectorGrid)

    buff.scaleX.offset = float(window[0][0])
    buff.scaleY.offset = float(window[0][1])
    buff.scaleX.factor = float(window[1][0] - buff.scaleX.offset)/nx/vectorGrid
    buff.scaleY.factor = float(window[1][1] - buff.scaleY.offset)/ny/vectorGrid
    buff.scaleI.offset = float(scaleIoffset)
    buff.scaleI.factor = float(scaleIfactor)

    if alternate_buff:
        buff = BufferTypeAlt(buff)

    return buff

def load_AttributeList(atts={}):
    """
    Load a dictionary of attributes into an AttributeList object.

    Parameters
    ----------
    atts : {attribute:value}
        Attributes

    Returns
    -------
    out: AttributeList


    Notes
    -----

     AttributeList needs to eventually be destroyed (otherwise memory leaks)
     core.DestroyAttributeList2(Attatttributesxt)
    """
    attlist = core.AttributeList()
    a = attlist

    for key in atts:
        a.next  = core.AttributeList()
        a       = a.next
        a.name  = key
        val = atts[key]

##        if '\udcb5' in val: # fix non-compliant symbols
##            val = val.replace('\udcb5', '\xb5')

        a.value = val

    return attlist

def buffer_as_array(buff):

    """
    Make an nd_array interface to buff.

    If the buffer is of type BufferTypeAlt then the buffer will  be
    created in memory.


    Parameters
    ----------
        buff: BufferType or BufferTypeAlt
            In the case of BufferTypeAlt the buffer will be created and returned

    Returns
    -------
        ndarray: of shape (components, buff.ny, buff.nx)
                where components =
                        core.GetVectorComponents(buff.image_sub_type) * buff.nf
                        for vectors and buff.nf for images

        buffer: BufferType

    """

    if type(buff) is BufferTypeAlt:
        buff, err = createBuffer(buff)

    if buff.wordArray:
        typ = ctypes.POINTER( ctypes.c_ushort)
        ba = buff.wordArray
    elif buff.floatArray:
        typ = ctypes.POINTER( ctypes.c_float)
        ba = buff.floatArray
    else:
        raise MemoryError('No buffer available')

    try:
        # python 3
        obj = ba.__int__()
    except(AttributeError):
        # python 2
        obj = ba.__long__()

    pA = ctypes.cast( obj, typ)

    if buff.image_sub_type > 0:
        components = core.GetVectorComponents(buff.image_sub_type)
    else:
        components = 1 # for images at the moment
    components *= buff.nf
    a = np.ctypeslib.as_array(pA,(components, buff.ny, buff.nx)) #updated 22/5/11
    return a, buff

def buffer_mask_as_array(buff):

    """
    Make an nd_array interface to mask of the buffer (DaVis V8).

    If the buffer is of type BufferTypeAlt then the buffer will  be
    created in memory.


    Parameters
    ----------
        buff: BufferType or BufferTypeAlt
            In the case of BufferTypeAlt the buffer will be created and returned

    Returns
    -------
    array, buff = np.array([components*nf,nx,ny]), core.BufferType
    where: components = core.GetVectorComponents(buff.image_sub_type) * buff.nf

    Note: It is necessary to destroy buff manually with core.DestroyBuffer(buff)
        followed by del(array) is necessary
    """

    if type(buff) is BufferTypeAlt:
        buff, err = createBuffer_davis(buff)

    if buff.bMaskArray:

        try:
            # python 3
            obj = buff.bMaskArray.__int__()
        except(AttributeError):
            # python 2
            obj = buff.bMaskArray.__long__()

        pA = ctypes.cast( obj, ctypes.POINTER( ctypes.c_bool))
        a = np.ctypeslib.as_array(pA,(buff.nf,buff.ny,buff.nx)) #updated 22/5/11
    else:
        a = None
    return a, buff

def att2dict(att):
    """
    Convert an Attribute list to a dictionary

    Parameters
    ----------
    att: AttributeList

    Returns
    ----------
    attribute dictionairy : {Attribute:Value}

    """
    out = {}
    attn = att.next
    while attn:
        val = attn.value
        if '\udcb5' in val: # fix non-compliant symbols
            val = val.replace('\udcb5', '\xb5')
        out[attn.name] = val
        attn = attn.next
    return out


def DestroyAttributeListSafe(att):
    if att.next:
        core.DestroyAttributeList2(att.next)


def get_sample_folder():
    folder = os.path.dirname(inspect.getfile(BunchMappable))
    folder = os.path.join(folder, 'sample_files')
    assert os.path.isdir(folder), 'Sample files not found!'
    return folder

def get_sample_image_filenames():
    ptn = get_sample_folder()
    ptn = os.path.join(ptn, '*.im7')
    return glob.glob(ptn)

def get_sample_vector_filenames():
    ptn = get_sample_folder()
    ptn = os.path.join(ptn, '*.vc7')
    return glob.glob(ptn)
