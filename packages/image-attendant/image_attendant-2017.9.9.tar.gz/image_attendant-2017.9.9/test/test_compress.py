
from __future__ import division, print_function, unicode_literals

"""
Test Examples
=============


## Python Tests
self.assertTrue(value)
self.assertFalse(value)

self.assertGreater(first, second, msg=None)
self.assertGreaterEqual(first, second, msg=None)
self.assertLess(first, second, msg=None)
self.assertLessEqual(first, second, msg=None)

self.assertAlmostEqual(first, second, places=7, msg=None, delta=None)
self.assertNotAlmostEqual(first, second, places=7, msg=None, delta=None)

self.assertItemsEqual(actual, expected, msg=None)
self.assertSequenceEqual(seq1, seq2, msg=None, seq_type=None)
self.assertListEqual(list1, list2, msg=None)
self.assertTupleEqual(tuple1, tuple2, msg=None)
self.assertSetEqual(set1, set2, msg=None)
self.assertDictEqual(expected, actual, msg=None)

self.assertRaises(Exception, some_func, arg, arg_nother)


## Numpy Tests
np.testing...

assert_equal(actual, desired[, err_msg, verbose])   Raises an AssertionError if two objects are not equal.
assert_allclose(actual, desired[, rtol, ...])       Raises an AssertionError if two objects are not equal up to desired tolerance.

assert_almost_equal(actual, desired[, ...])         Raises an AssertionError if two items are not equal up to desired precision.
assert_approx_equal(actual, desired[, ...])         Raises an AssertionError if two items are not equal up to significant digits.
assert_array_almost_equal(x, y[, decimal, ...])     Raises an AssertionError if two objects are not equal up to desired precision.
assert_array_almost_equal_nulp(x, y[, nulp])        Compare two arrays relatively to their spacing.
assert_array_max_ulp(a, b[, maxulp, dtype])         Check that all items of arrays differ in at most N Units in the Last Place.
assert_array_equal(x, y[, err_msg, verbose])        Raises an AssertionError if two array_like objects are not equal.
assert_array_less(x, y[, err_msg, verbose])         Raises an AssertionError if two array_like objects are not ordered by less than.
assert_raises(exception_class, callable, ...)       Fail unless an exception of class exception_class is thrown by callable when invoked with arguments args and keyword arguments kwargs.
assert_raises_regex(exception_class, ...)           Fail unless an exception of class exception_class and with message that matches expected_regexp is thrown by callable when invoked with arguments args and keyword arguments kwargs.
assert_warns(warning_class, *args, **kwargs)        Fail unless the given callable throws the specified warning.
assert_string_equal(actual, desired)                Test if two strings are equal.

"""

import unittest
import os
import pathlib
import shutil

import numpy as np

import context
import image_attendant as imat

_path_module = pathlib.Path(__file__).parent.absolute()

#------------------------------------------------
def cleanup(files):
    cleaned = []

    # Kill the files.
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

            cleaned.append(f)

    # Kill the folders.
    for f in files:
        if os.path.isdir(f):
            shutil.rmtree(f)

            cleaned.append(f)

    return cleaned


#------------------------------------------------
class TestReadWrite(unittest.TestCase):
    def setUp(self):
        self.path_Lena = pathlib.Path(_path_module, 'Lena')
        self.path_data = pathlib.Path(_path_module, 'temp_data')

        if not self.path_data.is_dir():
            os.mkdir(self.path_data)

        self.clean = []
        self.clean.append('temp_data')

    def tearDown(self):
        cleanup(self.clean)


    def test_compress_png(self):
        files = self.path_Lena.glob('Lena*')
        for f in files:
            img_in = imat.read(f)

            buff = imat.compress(img_in, fmt='png')

            img_test = imat.decompress(buff)

            np.testing.assert_equal(img_in, img_test, str(f))

    def test_compress_tiff(self):
        files = self.path_Lena.glob('Lena*')
        for f in files:
            img_in = imat.read(f)

            buff = imat.compress(img_in, fmt='tiff')

            img_test = imat.decompress(buff)

            np.testing.assert_equal(img_in, img_test, str(f))

#------------------------------------------------

if __name__ == '__main__':
    unittest.main(verbosity=2)
