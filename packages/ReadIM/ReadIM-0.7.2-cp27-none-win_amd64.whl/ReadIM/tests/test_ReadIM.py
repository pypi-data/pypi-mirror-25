from __future__ import division, print_function, absolute_import

import ReadIM

import os
from numpy.testing import (TestCase, assert_almost_equal, assert_equal,
                           assert_, assert_raises, run_module_suite,
                           assert_allclose)

import shutil
from tempfile import mkdtemp

import glob
files = ReadIM.extra.get_sample_image_filenames() + \
                 ReadIM.extra.get_sample_vector_filenames()

class TestIM7(TestCase):

    def setUp(self):
        self.pth = os.getcwd()
        self.tempdir = mkdtemp()
        os.chdir(self.tempdir)

    def tearDown(self):
        os.chdir(self.pth)
        print (self.tempdir)
        shutil.rmtree(self.tempdir)
    def test_load_im(self):

        for f in files:

            buff, atts   =  ReadIM.extra.get_Buffer_andAttributeList(f)
            arr, buff2 = ReadIM.extra.buffer_as_array(buff)

            err_msg = 'Problem unpacking file to array {0}'.format(buff)

            if buff.image_sub_type <=0:
                components = 1
            else:
                components = ReadIM.core.GetVectorComponents(buff.image_sub_type)
            components *= buff.nf

            assert_equal(arr.shape, (components, buff.ny, buff.nx), err_msg)

            ReadIM.extra.att2dict(atts)

            ReadIM.DestroyBuffer(buff)
            ReadIM.DestroyAttributeListSafe(atts)



    def test_create_im7(self):

        window = [(0,10),(10,0)]
        for tp in ReadIM.BUFFER_FORMATS:
            buffAlt = ReadIM.newBuffer(window,3,3,2, tp, 2)
            buff, errorcode = ReadIM.createBuffer(buffAlt)

            err_msg = 'Error creating buffer'
            assert_equal(errorcode, 1, err_msg)
            # data
            arr  = ReadIM.buffer_as_array(buff)


            # monotonically increasing data
            for i in range(len(arr)):
                arr[i]

            attributes = dict(type=ReadIM.BUFFER_FORMATS[tp])

            atts = ReadIM.load_AttributeList(attributes)


            ReadIM.WriteIM7('packed_im{0}.im7'.format(tp), True, buff, atts.next)
            ReadIM.WriteIM7('not_packed_im{0}.im7'.format(tp), False, buff, atts.next)

            ReadIM.DestroyBuffer(buff)
            ReadIM.DestroyAttributeListSafe(atts)
    def test_bufferAlt(self):
        import numpy as np
        window = [(0,10),(10,0)]
        buffAlt = ReadIM.newBuffer(window,3,3,2)
        buffAlt.scaleX.offset = np.array(1)
        buffNew = ReadIM.BufferTypeAlt(buffAlt)
        assert not (buffAlt is buffNew)
        assert type(buffNew.scaleX.offset) is float, "{0}".format(type(buffAlt.scaleX.offset))
        pass


if __name__ == "__main__":
    test = TestIM7('test_bufferAlt')
    test.debug()
    run_module_suite(argv=['-f',])
