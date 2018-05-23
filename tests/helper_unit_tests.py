# -*- coding: utf-8 -*-
"""
Created on Tue May 22 23:57:25 2018

@author: Carlos
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../crawler")

import helpers


class TestHelperFunctions(unittest.TestCase):
    """Tests the helper functions."""
    pass


class DummyPickleTester(object):
    """Dummy class to test the pickle functions."""
    def __init__(self, name, id_number, files, dummy=None):
        self.name = name
        self.id_number = id_number
        self.files = files
        self.child = dummy

    def __str__(self):
        return "Dummy object; Name = {}; Id = {}".format(self.name, self.id_number)


if __name__ == "__main__":
    unittest.main()
