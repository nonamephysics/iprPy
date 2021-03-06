# Standard Python libraries
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)

# iprPy imports
from .input.interpret_functions import loaded as input_interpret_loaded
from .input.interpret_functions import failed as input_interpret_failed
from .input.buildcombos_functions import loaded as input_buildcombos_loaded
from .input.buildcombos_functions import failed as input_buildcombos_failed
from .record import loaded as record_loaded
from .record import failed as record_failed
from .calculation import loaded as calculation_loaded
from .calculation import failed as calculation_failed
from .database import loaded as database_loaded
from .database import failed as database_failed

__all__ = ['check_modules']

def check_modules():
    """
    Prints lists of the calculation, record, and database styles that were
    successfully and unsuccessfully loaded when iprPy was initialized.
    """
    print('input.interpret styles that passed import:')
    for style in input_interpret_loaded.keys():
        print('-', style)
    print('input.interpret styles that failed import:')
    for style in input_interpret_failed.keys():
        print('-', style + ':', input_interpret_failed[style])
    print()
    
    print('input.buildcombos styles that passed import:')
    for style in input_buildcombos_loaded.keys():
        print('-', style)
    print('input.buildcombos styles that failed import:')
    for style in input_buildcombos_failed.keys():
        print('-', style + ':', input_buildcombos_failed[style])
    print()
    
    print('record styles that passed import:')
    for style in record_loaded.keys():
        print('-', style)
    print('record styles that failed import:')
    for style in record_failed.keys():
        print('-', style + ':', record_failed[style])
    print()
    
    print('calculation styles that passed import:')
    for style in calculation_loaded.keys():
        print('-', style)
    print('calculation styles that failed import:')
    for style in calculation_failed.keys():
        print('-', style + ':', calculation_failed[style])
    print()
    
    print('database styles that passed import:')
    for style in database_loaded.keys():
        print('-', style)
    print('database styles that failed import:')
    for style in database_failed.keys():
        print('-', style + ':', database_failed[style])
    print()