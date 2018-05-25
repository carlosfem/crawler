# -*- coding: utf-8 -*-
"""
Created on Sat May 19 14:04:28 2018

@author: Carlos
"""

import os
import csv
import pickle
import urllib
import logging


def safe_url(url):
    """Always returns a url starting with 'https://'. and with the special
    characters properly quoted
    """
    if not (url.startswith("https://") or url.startswith("http://")):
        url = "https://" + url
    return urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")


def get_domain(url):
    """Return the domain of the url, or an empty string."""
    url = safe_url(url)
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc


def get_url(domain, route):
    """Concatenates the domain with the route."""
    return domain + route


def add_extension(name, extension):
    """Adds an extension to the name if necessary
    Example:
    >>> add_extension('myfile', '.csv')
    >>> 'myfile.csv'
    """
    return name if name.endswith(extension) else name + extension


def chunks(list_, size):
    """Breaks a list into chunks of the same size."""
    size = 1 if size == 0 else size
    for i in range(0, len(list_), size):
        yield list_[i:i+size]


def pages_to_csv(filename, pages, path=""):
    """Writes a csv file with information about the webpages.
    Raises PermissionError if the file is already open.
    """
    filename = add_extension(filename, ".csv")
    if not path:
        filename = os.path.join(os.pardir, filename)
    else:
        filename = path + filename
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        for page in pages:
            wr.writerow([str(page)])


def get_debug_logger(name):
    """Createas a configured instance of a debug logger."""
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S")
        stream.setFormatter(formatter)
        logger.addHandler(stream)
    return logger


def save_objects(collection, filename):
    """Saves a collection of objects into a .pkl file using pickle."""
    filename = add_extension(filename, ".pkl")
    with open(filename, 'wb') as output:
        for obj in collection:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def save_object(obj, filename):
    """Saves an object into a .pkl file using pickle."""
    save_objects([obj], filename)


def load_objects(filename):
    """generator: Load a collection of objects from a .pkl file"""
    filename = add_extension(filename, ".pkl")
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
