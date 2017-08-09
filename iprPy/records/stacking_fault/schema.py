from __future__ import division, absolute_import, print_function

__all__ = ['schema']

import os

def schema():
    """
    Gets the path to the .xsd file associated with the record style.
    style.
    
    Returns
    -------
    str
        The absolute path for the record style's schema file.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir, 'record-stacking-fault.xsd')