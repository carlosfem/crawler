# -*- coding: utf-8 -*-
"""
Created on Thu May 17 07:47:17 2018

@author: Carlos
"""


import gc
import time
import urllib.error

import helpers
import webpage as wp
from thread_manager import ThreadingManager


class Crawler(object):
    """Crawler docstring."""

    _garbage_collection = 300  # collects the garbage every 'n' visited pages
    _timeout = 10  # seconds before raising wp.TimeoutException

    def __init__(
            self, domain, visits_limit=1e4, greedy=False,
            indentity_target=lambda page: True):

        self.root_page = wp.WebPage(domain)
        self.target_pages = {}
        self.other_pages = {}
        self.visited_urls = set()
        self.invalid_urls = set()

        self.visits_limit = visits_limit
        self.greedy = greedy
        self.identify_target = indentity_target

        self._inner_urls = set()

    def export_csv(self, filename):
        """Export the results to a csv file."""
        helpers.pages_to_csv(filename, self.target_pages.values())

    def iterative_crawl(self, n_workers):
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

        unvisited = self._get_unvisited_urls(self.root_page.child_urls)
        while len(unvisited) > 0 and len(self.visited_urls) < self.visits_limit:
            self._inner_urls = set()
            manager = ThreadingManager(self, list(unvisited), n_workers, "_inner_loop")
            manager.manage()

            unvisited = self._get_unvisited_urls(self._inner_urls)
            #print("There are {} URLs to visit on the next iteration".format(len(unvisited)), end="")

    def _inner_loop(self, queue):
        """Runs the inner loop of the iterative process.
        Args:
            queue (Queue): used for threading.
        """
        unvisited = queue.get()
        for url in unvisited:
            if len(self.visited_urls) > self.visits_limit:
                return
            if len(self.visited_urls) % self._garbage_collection == 0:
                gc.collect()
            self._handle_new_page(url)

    def _handle_new_page(self, url):
        """Handles the visit to a new page.
        Args:
            url (str): the url being requested.
            next_step (function): receives a WebPage object holds the
            instruction to move forward with the algorithm.
        """

        #print("N: {}; URL: {}".format(len(self.visited_urls), url))
        self.visited_urls.add(url)

        try:
            new_page = wp.WebPage(url, timeout=self._timeout)
            if self.identify_target(new_page):
                self.target_pages[new_page.url] = new_page
            else:
                self.other_pages[new_page.url] = new_page
            self._inner_urls |= set(new_page.child_urls)

            if not self.greedy:
                new_page.free()  # frees memory after parsing

        except (urllib.error.HTTPError, wp.TimeoutException) as e:
            self._on_timeout_exception(url, e)
        except urllib.error.URLError:
            self.invalid_urls.add(url)

    def _on_timeout_exception(self, url, exception, wait=60):
        """Event handler to deal with timeout events. It's important to wait
        for a few seconds after getting timed out on a request, because this
        could mean the domain might consider you a threat.
        """
        #print(str(exception))
        time.sleep(wait)
        self.visited_urls.remove(url)

    def _get_unvisited_urls(self, urls):
        """set: Return the unvisited URLs among the ones given."""
        unvisited = set()
        for url in urls:
            if url not in self.visited_urls and url not in self.invalid_urls:
                unvisited.add(url)
        return unvisited


if __name__ == "__main__":

    t = time.time()

    try:
        domain = "https://www.epocacosmeticos.com.br"
        crawler = Crawler(domain, visits_limit=10, greedy=False,
                          indentity_target=lambda page: page.is_product)

        crawler.iterative_crawl(10)
        crawler.export_csv("output")
    except KeyboardInterrupt:
        print("Crawling interrupted by the user!")

    print("Process completed in {} seconds".format(time.time() - t))


# Crie uma funcionalidade para construir Paginas a partir do csv exportado
# Exporte algum arquivo com todas as informações necessárias para reconstruir o crawler e continuar de onde parou


#    domain = "https://www.epocacosmeticos.com.br"
#    page = wp.WebPage(domain)


