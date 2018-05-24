# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:04:56 2018

@author: Carlos
"""

import queue
import threading

import helpers


class Task(threading.Thread):
    """Custom thread object to handle tasks executed iteratively over a queue.
    Attributes:
        process (function): task to be executed on the elements of the queue.
        queue (Queue): instance of the queue with the objects to process.
    """

    def __init__(self, process, queue):
        super().__init__()
        self.process = process
        self.queue = queue
        self._stop_event = threading.Event()

    def stop(self):
        """Sets the stop event to true. Used to stop running the thread."""
        self._stop_event.set()

    def run(self):
        """Runs the process with the next elements on queue."""
        operations = self.queue.get()
        for operation in operations:
            if self._stop_event.is_set():
                return
            self.process(operation)


class ThreadingManager(object):
    """Manages threading with a queue (mocks a distributed architecture).
    Note:
        The manager  takes a processor object  that needs to perform calls on a
        list  and wait for  responses. This work is  splitted between a certain
        number of threads using a queue.
    Attributes:
        processor (object): processor object that performs the requests.
        n_workers (int): number of threads to work on the downlodas.
    """

    def __init__(self, processor, n_workers):
        self.processor = processor
        self.n_workers = n_workers
        self.workers = []

        # Queue variables
        self.queue = queue.Queue()
        self.thread_count = threading.active_count()

    def manage(self, elements, process_name):
        """Manage the processing, splitting the task between the workres.
        Args:
            elements (str): list of elements that feed the process.
            process_name (str): name of the task to be paralelized.
        """
        process = getattr(self.processor, process_name)
        n_bundles = int(len(elements)/self.n_workers)
        bundles = list(helpers.chunks(elements, n_bundles))

        for bundle in bundles:
            self.queue.put(bundle)
            worker = Task(process, self.queue)
            worker.start()
            self.workers.append(worker)

        while threading.active_count() > self.thread_count:
            pass

    def stop_all_workers(self):
        """Commands all workers to interrupt their processes."""
        for worker in self.workers:
            worker.stop()
