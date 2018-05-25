# -*- coding: utf-8 -*-
"""
Created on Sat May 19 08:03:57 2018

@author: Carlos
"""

import bs4
import socket
import urllib.request

import helpers
from decorators import Decorators


class TimeoutException(Exception):
    pass


class WebPage():
    """Holds the relevant information about the page.

    Attributes:
        url (str): url of the page, must be a valid url.
        target_tag (str): type of html tag that identifies the target.
        target_class (str): class of the html tag that identifies the target.
        timeout (float): time in seconds before timing out the request.

    Raises:
        URLError: If the url is invalid.
        HTTPError: If the request cannot be completed.
        AttributeError: If the url is not a string.
    """

    _INVALID_TARGET = "N/A"
    _AGENT = "Academic crawler 1.0 created by Carlos Monteiro. Strictly for python studies."

    def __init__(
            self, url, target_tag="div",
            target_class="productName", timeout=2):

        self.url = helpers.safe_url(url)
        self.target_tag = target_tag
        self.target_class = target_class
        self.timeout = timeout

        self._soup = ""
        self._child_urls = set()

        div = self.soup.find(self.target_tag, {"class": self.target_class})

        self.title = self.soup.find("title").text
        self.domain = helpers.get_domain(self.url)
        self.target_name = self._INVALID_TARGET if div is None else div.text

        # dump
        del div

    def free(self):
        """Frees memory by reseting the _soup object and the child URLs"""
        self._child_urls.clear()
        self._soup = ""

    @property
    @Decorators.initializer("_soup")
    def soup(self):
        """BeautifulSoup: requests the URL and parse the html"""
        # Gets the response from the HTTP request and creates the bs4 parser
        request = urllib.request.Request(
            self.url, headers={"User-Agent": self._AGENT}
        )
        # Gets the response treating for potential timeouts
        try:
            response = urllib.request.urlopen(request, timeout=self.timeout)
            self._soup = bs4.BeautifulSoup(response, "html.parser")
        except socket.timeout:
            raise TimeoutException("Timeout occurred while requesting page.")
        return self._soup

    @property
    @Decorators.initializer("_child_urls")
    def child_urls(self):
        """list: return a list with all the child pages originated from the
                 same domain without duplicates. Excludes the parent page.
        """
        urls = [url["href"] for url in self.soup.find_all("a", href=True)]
        for url in urls:
            domain = helpers.get_domain(url)
            if domain == self.domain:
                self._child_urls.add(helpers.safe_url(url))
            elif domain == "":
                self._child_urls.add(helpers.safe_url(self.domain + url))
        return self._child_urls

    @property
    def valid_target(self):
        """bool: return True if the page matches the target specification."""
        return self.target_name != self._INVALID_TARGET

    def __str__(self):
        """Overloads the 'str' method"""
        if self.valid_target:
            rep = "Target Text: {}; Title: {}; URL: {}".format(
                self.target_name, self.title, self.url
            )
        else:
            rep = "Title: {}; URL: {}".format(self.title, self.url)
        return rep
