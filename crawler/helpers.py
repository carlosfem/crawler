# -*- coding: utf-8 -*-
"""
Created on Sat May 19 14:04:28 2018

@author: Carlos
"""

import os
import csv
import urllib


class StringHelper(object):

    @staticmethod
    def safe_url(url):
        """Always returns a url starting with 'https://'. and with the special
        characters properly quoted
        """
        if not (url.startswith("https://") or url.startswith("http://")):
            url = "https://" + url
        return urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")

    @staticmethod
    def get_domain(url):
        """Return the domain of the url, or an empty string."""
        url = StringHelper.safe_url(url)
        parsed_url = urllib.parse.urlparse(url)
        return parsed_url.netloc

    @staticmethod
    def get_url(domain, route):
        """Concatenates the domain with the route."""
        return domain + route

    @staticmethod
    def add_extension(name, extension):
        """Adds an extension to the name if necessary
        Example:
        >>> add_extension('myfile', '.csv')
        >>> 'myfile.csv'
        """
        return name if name.endswith(extension) else name + extension


class CsvHelper(object):

    @staticmethod
    def pages_to_csv(filename, pages, path=""):
        """Writes a csv file with information about the webpages.
        Raises PermissionError if the file is already open.
        """
        filename = StringHelper.add_extension(filename, ".csv")
        if not path:
            filename = os.path.join(os.pardir, filename)
        with open(filename, 'w', newline='') as myfile:
            wr = csv.writer(myfile)
            for page in pages:
                wr.writerow([str(page)])


class ListHelper(object):

    @staticmethod
    def chunks(list_, size):
        """Breaks a list into chunks of the same size."""
        size = 1 if size == 0 else size
        for i in range(0, len(list_), size):
            yield list_[i:i+size]


class GeneralHelper(object):

    @staticmethod
    def raiseException(exception):
        """Raises an exception, used to raise exceptions inline with lambda."""
        raise exception
