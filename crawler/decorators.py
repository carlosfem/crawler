# -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:10:27 2018

@author: Carlos
"""

from functools import wraps


class Decorators(object):
    """Class with decorator methods."""

    @staticmethod
    def initializer(private_name):
        """Decorator to initialize properties of a class.
        Note:
            Used to initialize properties that follow a particular pattern
            during the first use. Initialize the 'private' field with a given
            function and then return it.
        Args:
            private_name (str): name of the private field to initialize.
        """
        def decorator(func):
            @wraps(func)
            def wraper(obj, *args, **kwargs):
                field = getattr(obj, private_name)
                if len(field) == 0:
                    field = func(obj, *args, **kwargs)
                return field
            return wraper
        return decorator
