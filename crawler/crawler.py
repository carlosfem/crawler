# -*- coding: utf-8 -*-
"""
Created on Thu May 17 07:47:17 2018

@author: Carlos
"""


import gc
import time
import urllib.error

import webpage as wp
from helpers import CsvHelper


class Crawler(object):
    """Crawler docstring."""

    _garbage_collection = 300  # collects the garbage every 'n' visited pages
    _timeout = 10  # seconds before raising wp.TimeoutException

    def __init__(self, domain, visits_limit=1e4):
        self.root_page = wp.WebPage(domain)
        self.product_pages = {}
        self.other_pages = {}
        self.visited_urls = set()
        self.invalid_urls = set()
        self.visits_limit = visits_limit

        self._inner_urls = set()

    def export_csv(self, filename):
        """Export the results to a csv file."""
        CsvHelper.pages_to_csv(filename, self.product_pages.values())

    def run(self, recursive=True):
        """Run the crawling algorithm."""
        if recursive:
            self.recursive_crawl(self.root_page)
        else:
            self.iterative_crawl(self.root_page)

    def recursive_crawl(self, page):
        """Recursive function to find and store all pages within a domain.
        Args:
            page (WebPage): Page being crawled.
        Algorithm:
            1 - Fetch the non visited URLs and loop through them all;
            2 - Request and parse each URL, updating the sets and dicts;
            3 - Recursively call the function. Recursion ends on each node when
                the unvisited set is empty.
        """

        for url in self._get_unvisited(page.child_urls):

            if len(self.visited_urls) > self.visits_limit:
                raise KeyboardInterrupt
            if len(self.visited_urls) % self._garbage_collection == 0:
                gc.collect()

            self._handle_new_page(page, url, self.recursive_crawl)

    def iterative_crawl(self, page):
        """Iterative function to find and store all pages within a domain.
        Args:
            page (WebPage): Page being crawled.
        Algorithm:
            1 - Fetch the non visited URLs;
            2 - Outer loops runs until there are no unvisited URLs;
            3 - Clear the inner url set and loop through all non visited URLs;
            4 - Request and parse each URL, updating the sets and dicts;
            5 - Update the non visited URL set keep going with the outer loop.
        """

        unvisited = self._get_unvisited(page.child_urls)

        # Outer loop. Ends when there are no new non visited urls
        while len(unvisited) > 0:
            self._inner_urls = set()
            for url in unvisited:
                if len(self.visited_urls) > self.visits_limit:
                    return
                if len(self.visited_urls) % self._garbage_collection == 0:
                    gc.collect()
                self._handle_new_page(page, url, self._increment_inner_urls)

            unvisited = self._get_unvisited(self._inner_urls)
            print("There are {} URLs to visit on the next iteration".format(len(unvisited)))

    def _get_unvisited(self, urls):
        """set: Return the unvisited URLs among the ones given."""
        unvisited = set()
        for url in urls:
            if url not in self.visited_urls and url not in self.invalid_urls:
                unvisited.add(url)
        return unvisited

    def _handle_new_page(self, page, url, next_setp):
        """Handles the visit to a new page.
        Args:
            page (WebPage): current page in the outer loop.
            url (str): the url being requested.
            next_step (function): receives a WebPage object holds the
            instruction to move forward with the algorithm.
        """

        print("N: {}; URL: {}".format(len(self.visited_urls), url))
        self.visited_urls.add(url)

        try:
            new_page = wp.WebPage(url, parent_page=page, timeout=self._timeout)
            if new_page.is_product:
                self.product_pages[new_page.url] = new_page
            else:
                self.other_pages[new_page.url] = new_page

            next_setp(new_page)  # recursive call or set increment

        except (urllib.error.HTTPError, wp.TimeoutException) as e:
            self._on_timeout_exception(url, e)
        except urllib.error.URLError:
            self.invalid_urls.add(url)

    def _on_timeout_exception(self, url, exception, wait=60):
        """Event handler to deal with timeout events. It's important to wait
        for a few seconds after getting timed out on a request, because this
        could mean the domain might consider you a threat.
        """
        print(str(exception))
        time.sleep(wait)
        self.visited_urls.remove(url)

    def _increment_inner_urls(self, page):
        """Increment the inner url set (syntactic sugar)."""
        self._inner_urls |= set(page.child_urls)


if __name__ == "__main__":

#    t = time.time()
#
#    try:
#        domain = "https://www.epocacosmeticos.com.br"
#        crawler = Crawler(domain, visits_limit=100)
#        crawler.run(recursive=False)
#        crawler.export_csv("output")
#    except KeyboardInterrupt:
#        print("Crawling interrupted by the user!")
#
#    print("Process completed in {} seconds".format(time.time() - t))


    domain = "https://www.epocacosmeticos.com.br"
    page = wp.WebPage(domain)

    ## TESTE A EFICIENCIA DA _increment_inner_urls
