# -*- coding: utf-8 -*-
"""
Created on Thu May 17 07:47:17 2018

@author: Carlos
"""


import time
import urllib.error

import helpers
import webpage as wp
from thread_manager import ThreadingManager


class Crawler(object):
    """Crawler docstring.
    Note:
        Foo
    Args:
        Bar
    """

    _timeout = 10  # seconds before raising wp.TimeoutException

    def __init__(
            self, domain, req_limit=1e4, greedy=False,
            indentify_target=lambda page: True, log_file="log_crawl"):

        # Initialize
        self.root_page = wp.WebPage(domain)
        self.target_pages = {}
        self.other_pages = {}
        self.visited_urls = set()
        self.invalid_urls = set()
        self.inner_urls = set()
        self.unvisited = set()
        self.manager = None

        # Crawl parameters
        self.req_limit = req_limit
        self.greedy = greedy
        self.identify_target = indentify_target
        self.log_file = log_file
        self.log_frequency = req_limit/10

    def export_csv(self, filename, only_targets=True):
        """Export the results to a csv file."""
        exported = self.target_pages.values()
        if not only_targets:
            exported = list(exported) + list(self.other_pages.values())
        helpers.pages_to_csv(filename, exported)

    def run(self, n_workers):
        """Iterative function to find and store all pages within a domain.
        Args:
            n_workers (int): number of workers executing the inner loop.
        Algorithm:
            1 - Fetch the non visited URLs;
            2 - Outer loops runs until there are no unvisited URLs;
            3 - Clear the inner url set and loop through all non visited URLs;
            4 - Request and parse each URL, updating the sets and dicts;
            5 - Update the non visited URL set keep going with the outer loop.
        """
        self.unvisited = self._get_unvisited_urls(self.root_page.child_urls)
        while len(self.unvisited) > 0 and len(self.visited_urls) < self.req_limit:
            try:
                self.inner_urls = set()
                self.manager = ThreadingManager(self, n_workers)
                self.manager.manage(list(self.unvisited), "_inner_loop")
                self.unvisited = self._get_unvisited_urls(self.inner_urls)
            except KeyboardInterrupt:
                self.manager.stop_all_workers()
                helpers.log_to_file("Crawling interrupted...", self.log_file)
                return

    def _inner_loop(self, url):
        """Runs the inner loop of the iterative process.
        Note:
            The loop is executed inside the threading manager. After retrieving
            the urls from the queue.
        Args:
            url (str): the url being requested.
        """

        self.visited_urls.add(url)
        if len(self.visited_urls) > self.req_limit:
            self.manager.stop_all_workers()
        if len(self.visited_urls) % self.log_frequency == 0:
            msg = "Visited pages: {}; Targets found {}; Running visits {}".format(
                len(self.visited_urls), len(self.target_pages), len(self.unvisited))
            helpers.log_to_file(msg, self.log_file)

        try:

            new_page = wp.WebPage(url, timeout=self._timeout)
            if self.identify_target(new_page):
                self.target_pages[new_page.url] = new_page
            else:
                self.other_pages[new_page.url] = new_page
            self.inner_urls |= set(new_page.child_urls)
            if not self.greedy:
                new_page.free()  # frees memory after parsing

        except (urllib.error.HTTPError, wp.TimeoutException) as e:
            self._on_timeout_exception(url, e)
        except urllib.error.URLError:
            self.invalid_urls.add(url)

    def _on_timeout_exception(self, url, exception, wait=60):
        """Event handler to deal with timeout events.
        Note:
            It's important to wait for a few seconds after getting timed out,
            trying the domain you are not a threat.
        """
        helpers.log_to_file(str(exception), self.log_file)
        time.sleep(wait)
        self.visited_urls.remove(url)

    def _get_unvisited_urls(self, urls):
        """set: Return the unvisited URLs among the ones given."""
        unvisited = set()
        for url in urls:
            if url not in self.visited_urls and url not in self.invalid_urls:
                unvisited.add(url)
        return unvisited  # sets are not subscriptable


if __name__ == "__main__":

    t = time.time()

    domain = "https://www.epocacosmeticos.com.br"
    crawler = Crawler(domain, req_limit=100, greedy=False,
                      indentify_target=lambda page: page.valid_target)
    crawler.run(10)
    crawler.export_csv("output", only_targets=False)

    helpers.log_to_file("Process completed in {} seconds".format(time.time() - t), "log_crawl")
