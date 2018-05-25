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

import helpers
import webpage as wp
import crawler as cw
import thread_manager as tm


class TestPageMethods(unittest.TestCase):
    """Tests the behaviour of the WebPage class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.domain = "www.epocacosmeticos.com.br"
        self.domain_page = wp.WebPage(self.domain)
        self.domain_urls = self.domain_page.child_urls

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
        page = self.domain_page

        self.assertTrue(page.child_urls)
        self.assertEqual(page.domain, self.domain)

        # Verifies that there are no duplicate child pages
        self.assertEqual(len(page.child_urls), len(set(page.child_urls)))

        # Verifies that there are no child pages from different domains
        diff_domain_children = [
            child for child in page.child_urls
            if helpers.get_domain(child) != page.domain
        ]
        self.assertFalse(diff_domain_children)

    def test_valid_target_page(self):
        """Tests if a valid target url yields a full target page."""
        route = "/hypnose-eau-de-toilette-lancome-perfume-feminino/p"
        url = helpers.get_url(self.domain, route)
        page = wp.WebPage(url)

        self.assertTrue(page.title)
        self.assertTrue(page.domain)
        self.assertTrue(page.valid_target)
        self.assertEqual(page.domain, self.domain)

    def test_invalid_target_page(self):
        """Tests if an invalid target url yields an invalid target page."""
        route = "/ganhe-brindes"
        url = helpers.get_url(self.domain, route)
        page = wp.WebPage(url)

        self.assertTrue(page.title)
        self.assertTrue(page.domain)
        self.assertFalse(page.valid_target)
        self.assertEqual(page.target_name, page._INVALID_TARGET)

    def test_free_memory(self):
        """Tests 'free' method to dump unused memory"""
        page = self.domain_page
        page.free()
        self.assertTrue(len(page._child_urls) == 0)
        self.assertTrue(len(page._soup) == 0)


class TestCrawlerLogic(unittest.TestCase):
    """Tests the core logic of the crawler."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        domain = "https://www.epocacosmeticos.com.br"
        self.crawler = cw.Crawler(
            domain, req_limit=10, greedy=False,
            indentify_target=lambda page: page.valid_target)
        self.crawler.run(10)

    def test_crawler_basics(self):
        """Tests the basic patterns expected on this simple crawler result."""
        crawler = self.crawler
        self.assertTrue(len(crawler.visited_urls) > 0)
        self.assertTrue(len(crawler.inner_urls) > 0)
        self.assertTrue(len(crawler.other_pages) > 0)

    def test_export_csv(self):
        """Tests csv is correctly exported given a list of pages."""
        filename = "test.csv"
        self.crawler.export_csv(filename)

        filepath = os.path.join(os.pardir, filename)
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)
        self.assertFalse(os.path.exists(filepath))

    def test_get_unvisited_urls(self):
        """Tests method to retrieve the unvisited URLs."""
        page = self.crawler.root_page
        unvisited = self.crawler._get_unvisited_urls(page.child_urls)
        self.assertTrue(unvisited.isdisjoint(self.crawler.visited_urls))
        self.assertTrue(unvisited.isdisjoint(self.crawler.invalid_urls))

    def test_thread_manager(self):
        operations = ["op{}".format(i) for i in range(6)]
        dummy = DummyThreadingTester(operations, sleeptime=0.1)

        t0 = time.time()
        manager = tm.ThreadingManager(dummy, 1)
        manager.manage(operations, "task")

        t1 = time.time()
        manager = tm.ThreadingManager(dummy, 3)
        manager.manage(operations, "task")

        t2 = time.time()
        manager = tm.ThreadingManager(dummy, 6)
        manager.manage(operations, "task")
        t3 = time.time()

        self.assertGreater(t1-t0, t2-t1)
        self.assertGreater(t2-t1, t3-t2)


class DummyThreadingTester(object):
    """Dummy class to test the threading manager."""

    def __init__(self, operations, sleeptime=1):
        self.operations = operations
        self.sleeptime = sleeptime

    def task(self, queue):
        """Dummy task, sleeps for a few seconds"""
        time.sleep(self.sleeptime)


if __name__ == "__main__":
    unittest.main()
