# -*- coding: utf-8 -*-
"""
Created on Sat May 19 08:03:57 2018

@author: Carlos
"""

import bs4
import socket
import urllib.request

from decorators import Decorators
from helpers import StringHelper as sh


class TimeoutException(Exception):
    pass


class WebPage():
    """Holds the relevant information about the page.

    Attributes:
        url (str): url of the page, must be a valid url.
        timeout (float): time in seconds before timing out the request.
        parent_page (WebPage): previous page in the tree.
        product_tag (str): type of html tag that identifies the product.
        product_class (str): class of the html tag that identifies the product.

    Raises:
        URLError: If the url is invalid.
        HTTPError: If the request cannot be completed.
        AttributeError: If the url is not a string.
    """

    _INVALID_PRODUCT = "N/A"
    _AGENT = "Academic crawler 1.0 created by Carlos Monteiro. Strictly for python studies."

    def __init__(
            self, url, parent_page=None, product_tag="div",
            product_class="productName", timeout=2):

        self.url = sh.safe_url(url)
        self.parent_page = parent_page
        self.product_tag = product_tag
        self.product_class = product_class

        self._title = ""
        self._domain = ""
        self._product_name = ""
        self._child_urls = set()

        # Gets the response from the HTTP request and creates the bs4 parser
        request = urllib.request.Request(
            self.url, headers={"User-Agent": self._AGENT}
        )

        # Gets the response treating for potential timeouts
        try:
            response = urllib.request.urlopen(request, timeout=timeout)
            self._soup = bs4.BeautifulSoup(response, "html.parser")
        except socket.timeout:
            raise TimeoutException("Timeout occurred while requesting page.")

    @property
    @Decorators.initializer("_title")
    def title(self):
        """str: return the title of the page (first occurrence)."""
        self._title = self._soup.title.string
        return self._title

    @property
    @Decorators.initializer("_domain")
    def domain(self):
        """str: return the domain of the url."""
        self._domain = sh.get_domain(self.url)
        return self._domain

    @property
    @Decorators.initializer("_product_name")
    def product_name(self):
        """str: return the name of the product or an invalid product identifier
                if the name tag is not found.
        """
        div = self._soup.find(self.product_tag, {"class": self.product_class})
        self._product_name = self._INVALID_PRODUCT if div is None else div.text
        return self._product_name

    @property
    def is_product(self):
        """bool: return True if the page is a product page."""
        return self.product_name != self._INVALID_PRODUCT

    @property
    @Decorators.initializer("_child_urls")
    def child_urls(self):
        """list: return a list with all the child pages originated from the
                 same domain without duplicates. Excludes the parent page.
        """
        urls = [url["href"] for url in self._soup.find_all("a", href=True)]
        for url in urls:
            domain = sh.get_domain(url)
            if domain == self.domain:
                full_url = sh.safe_url(url)
            elif domain == "":
                full_url = sh.safe_url(self.domain + url)
            else:
                continue
            self._child_urls.add(full_url)
        return self._child_urls

    def __str__(self):
        """Overloads the 'str' method"""
        if self.is_product:
            rep = "Product Name: {}; Title: {}; URL: {}".format(
                self.product_name, self.title, self.url
            )
        else:
            rep = "Title: {}; URL: {}".format(self.title, self.url)
        return rep
