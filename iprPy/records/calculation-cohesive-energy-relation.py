from DataModelDict import DataModelDict as DM

import atomman as am
import atomman.unitconvert as uc
import numpy as np
import pandas as pd

def schema():
    dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir, 'record-calculation-cohesive-energy-relation.xsd')

def todict(record, full=True):

    model = DM(record)

    calc = model['calculation-cohesive-energy-relation']
    params = {}
    params['calc_key'] =            calc['key']
    params['calc_script'] =         calc['calculation']['script']
    params['minimum_r'] =           uc.value_unit(calc['calculation']['run-parameter']['minimum_r'])
    params['maximum_r'] =           uc.value_unit(calc['calculation']['run-parameter']['maximum_r'])
    params['number_of_steps_r'] =   calc['calculation']['run-parameter']['number_of_steps_r']
    params['size_mults'] =    calc['calculation']['run-parameter']['size-multipliers']
    params['size_mults'] =    np.array([params['size_mults']['a'], 
                                        params['size_mults']['b'], 
                                        params['size_mults']['c']])
    params['potential_key'] = calc['potential']['key']
    params['potential_id'] =  calc['potential']['id']
    params['load'] =          '%s %s' % (calc['system-info']['artifact']['format'],
                                         calc['system-info']['artifact']['file'])
    params['prototype'] =     calc['system-info']['artifact']['family']
    params['symbols'] =       calc['system-info']['symbols']
    
    if full is True:
        if 'status' in calc:
            params['status'] = calc['status']
            params['error'] = np.nan
            params['e_vs_r_plot'] = np.nan
            params['number_min_states'] = np.nan
            
        elif 'error' in calc:
            params['status'] = np.nan
            params['error'] = calc['error']
            params['e_vs_r_plot'] = np.nan
            params['number_min_states'] = np.nan
            
        else:
            params['status'] = np.nan
            params['error'] = np.nan
            plot = calc['cohesive-energy-relation']
            params['e_vs_r_plot'] = pd.DataFrame({'r': uc.value_unit(plot['r']),
                                           'a': uc.value_unit(plot['a']),
                                           'E_coh': uc.value_unit(plot['cohesive-energy'])})            
            params['number_min_states'] = len(calc.aslist('minimum-atomic-system'))
    return params 