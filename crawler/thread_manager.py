# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:04:56 2018

@author: Carlos
"""

import queue
import threading
from helpers import ListHelper as lh


class ThreadingManager(object):
    """Manages threading with a queue (mocks a distributed architecture).
    Note:
        The manager  takes a processor object  that needs to perform calls on a
        list  and wait for  responses. This work is  splitted between a certain
        number of threads using a queue.
    Attributes:
        processor (object): processor object that performs the requests.
        elements (str): list of elements that feed the process.
        n_workers (int): number of threads to work on the downlodas.
        process_name (str): name of the request process.
    """

    def __init__(self, processor, elements, n_workers, process_name):
        self.processor = processor
        self.n_workers = n_workers
        self.elements = elements
        self.process = getattr(processor, process_name)

        # Queue variables
        self.queue = queue.Queue()
        self.thread_count = threading.active_count()

    def manage(self):
        """Manage the processing, splitting the task between the workres."""
        n_bundles = int(len(self.elements)/self.n_workers)
        bundles = list(lh.chunks(self.elements, n_bundles))

        for bundle in bundles:
            self.queue.put(bundle)
            worker = threading.Thread(target=self.process, args=(self.queue,))
            worker.start()

        while threading.active_count() > self.thread_count:
            pass
