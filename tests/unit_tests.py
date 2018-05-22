# -*- coding: utf-8 -*-
"""
Created on Sat May 19 08:34:48 2018

@author: Carlos
"""

import os
import sys
import time
import urllib
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../crawler")

import webpage as wp
import crawler as cw
import thread_manager as tm
from helpers import StringHelper as sh


class TestPageMethods(unittest.TestCase):
    """Tests the behaviour of the WebPage class"""

    _domain = "www.epocacosmeticos.com.br"

    def test_invalid_url(self):
        """Tests if an invalid url raises URLError"""
        invalid_url = "invalid"
        with self.assertRaises(urllib.error.URLError):
            wp.WebPage(invalid_url)

    def test_invalid_attribute(self):
        """Tests if an invalid attribute raises AttributeError"""
        with self.assertRaises(AttributeError):
            wp.WebPage(1)

    def test_valid_domain_page(self):
        """Tests if the domain page follows the expected standards"""
        page = wp.WebPage(self._domain)

        self.assertTrue(page.child_urls)
        self.assertEqual(page.domain, self._domain)

        # Verifies that there are no duplicate child pages
        self.assertEqual(len(page.child_urls), len(set(page.child_urls)))

        # Verifies that there are no child pages from different domains
        diff_domain_children = [
            child for child in page.child_urls
            if sh.get_domain(child) != page.domain
        ]
        self.assertFalse(diff_domain_children)

    def test_valid_product_page(self):
        """Tests if a valid product url yields a full product page object"""
        route = "/hypnose-eau-de-toilette-lancome-perfume-feminino/p"
        url = sh.get_url(self._domain, route)
        page = wp.WebPage(url)

        self.assertTrue(page.title)
        self.assertTrue(page.domain)
        self.assertTrue(page.is_product)
        self.assertEqual(page.domain, self._domain)

    def test_valid_non_product_page(self):
        """Tests if a valid non product url yields a non product page object"""
        route = "/ganhe-brindes"
        url = sh.get_url(self._domain, route)
        page = wp.WebPage(url)

        self.assertTrue(page.title)
        self.assertTrue(page.domain)
        self.assertFalse(page.is_product)
        self.assertEqual(page.product_name, page._INVALID_PRODUCT)


class TestCrawlerLogic(unittest.TestCase):
    """Tests the core logic of the crawler"""

    def test_export_csv(self):
        """Tests csv is correctly exported given a list of pages."""
        # Erase the csv after the test!
        raise NotImplementedError

    def test_get_unvisited(self):
        """Tests method to retrieve the unvisited URLs."""
        raise NotImplementedError

    def test_thread_manager(self):
        operations = ["op{}".format(i) for i in range(6)]
        dummy = DummyThreadingTester(operations, sleeptime=0.1)

        t0 = time.time()
        manager = tm.ThreadingManager(dummy, operations, 1, "task")
        manager.manage()

        t1 = time.time()
        manager = tm.ThreadingManager(dummy, operations, 3, "task")
        manager.manage()

        t2 = time.time()
        manager = tm.ThreadingManager(dummy, operations, 6, "task")
        manager.manage()
        t3 = time.time()

        self.assertGreater(t1-t0, t2-t1)
        self.assertGreater(t2-t1, t3-t2)


class DummyThreadingTester(object):
    """Dummy class to test the threading manager"""

    def __init__(self, operations, sleeptime=1):
        self.operations = operations
        self.sleeptime = sleeptime

    def task(self, queue):
        """Dummy task, sleeps for a few seconds"""
        operations = queue.get()
        for operation in operations:
            time.sleep(self.sleeptime)


if __name__ == "__main__":
    unittest.main()
