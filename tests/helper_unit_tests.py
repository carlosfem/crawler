# -*- coding: utf-8 -*-
"""
Created on Tue May 22 23:57:25 2018

@author: Carlos
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../crawler")

import helpers as h


class TestHelperFunctions(unittest.TestCase):
    """Tests the helper functions."""

    def test_safe_url_domain(self):
        """Tests the methods to return request safe URLs and domains."""
        http_string = "http://mydomain.com"
        https_string = "https://mydomain.com"
        no_protocol_string = "mydomain.com"

        self.assertEqual(h.safe_url(http_string), http_string)
        self.assertEqual(h.safe_url(https_string), https_string)
        self.assertEqual(h.safe_url(no_protocol_string), https_string)

        self.assertEqual(h.get_domain(http_string), no_protocol_string)
        self.assertEqual(h.get_domain(https_string), no_protocol_string)
        self.assertEqual(h.get_domain(no_protocol_string), no_protocol_string)

    def test_simple_string_helpers(self):
        """Tests the simple helper functions as adding extension and route."""
        domain = "mydomain.com"
        route = "/route"
        with_extension = "myfile.csv"
        without_extension = "myfile"

        self.assertEqual(h.get_url(domain, route), domain + route)
        self.assertEqual(h.add_extension(with_extension, ".csv"), with_extension)
        self.assertEqual(h.add_extension(without_extension, ".csv"), with_extension)

    def test_chunk_function(self):
        """Tests the function to split a collection into chunks."""
        list_ = [1, 2, 3, 4, 5, 6]
        chunk_bigger_then_len = list(h.chunks(list_, 7))
        chunk_half = list(h.chunks(list_, 3))
        chunk_zero = list(h.chunks(list_, 0))

        self.assertEqual(chunk_bigger_then_len[0], list_)
        self.assertEqual(chunk_half[0], [1, 2, 3])
        self.assertEqual(chunk_half[1], [4, 5, 6])
        self.assertEqual(len(chunk_zero), len(list_))

    def test_pickle_save_load_object(self):
        """Tests the methods to save and load objects using pickle."""
        files = ["file{}".format(i) for i in range(1, 6)]
        dummy1 = DummyPickleTester("dummy1", 1, files)
        dummy2 = DummyPickleTester("dummy2", 2, files, child=dummy1)

        h.save_object(dummy1, "dummy1")
        h.save_objects([dummy1, dummy2], "dummies")

        # Save
        file_dummy1 = "dummy1.pkl"
        file_dummies = "dummies.pkl"
        self.assertTrue(os.path.exists(file_dummy1))
        self.assertTrue(os.path.exists(file_dummies))

        # Load
        loaded_dummy = list(h.load_objects(file_dummy1))[0]
        loaded_dummies = list(h.load_objects(file_dummies))
        self.assertEqual(loaded_dummy, dummy1)
        self.assertEqual(loaded_dummies[0], dummy1)
        self.assertEqual(loaded_dummies[1], dummy2)

        # Cleanup
        os.remove(file_dummy1)
        os.remove(file_dummies)


class DummyPickleTester(object):
    """Dummy class to test the pickle functions."""
    def __init__(self, name, id_number, files, child=None):
        self.name = name
        self.id_number = id_number
        self.files = files
        self.child = child

    def __eq__(self, other):
        """Overrides the equality operator."""
        return (self.name == other.name and
                self.id_number == other.id_number and
                self.files == other.files and
                self.child == other.child)


if __name__ == "__main__":
    unittest.main()
