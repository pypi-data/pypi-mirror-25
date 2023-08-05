# -*- coding: utf-8 -*-
"""
.. module:: metaclasses.py
   :platform: Unix, Windows
   :synopsis: Metaclasses for a variety of uses in the package.

.. moduleauthor:: Sasha Petrenko <sap625@mst.edu>
"""

class MetaSingleton(type):
    """Metaclass, makes a singleton of the instantiated class
    
    :returns: First instance of the called class
    :rtype: class
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class ClassSingleton(object):
    """Class, makes a singleton object without a metaclass
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance