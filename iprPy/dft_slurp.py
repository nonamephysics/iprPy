# Standard Python libraries
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)
import os
import glob

# https://github.com/usnistgov/atomman
import atomman as am

# iprPy imports
from . import rootdir

def get_mp_structures(elements, api_key=None, lib_directory=None):
    """
    Accesses the Materials Project and downloads all structures for a list of
    elements as poscar files.
    
    Parameters
    ----------
    elements : list
        A list of element symbols.
    api_key : str, optional
        The user's Materials Project API key. If not given, will use "MAPI_KEY"
        environment variable
    lib_directory : str
        Path to the lib_directory to save the poscar files to.  Default uses
        the iprPy library/dft_structures directory.
    """
    # Function-specific imports
    import pymatgen as pmg
    from pymatgen.ext.matproj import MPRester
    
    # Handle lib_directory
    if lib_directory is None:
        lib_directory = os.path.join(os.path.dirname(rootdir), 'library', 'ref')
    lib_directory = os.path.abspath(lib_directory)
    
    elements.sort()
    
    # Open connection to Materials Project
    with MPRester(api_key) as m:
        
        # Loop over subsets of elements
        for subelements in subsets(elements):
            
            # Set comp_directory
            elements_string = '-'.join(subelements)
            comp_directory = os.path.join(lib_directory, elements_string)
            if not os.path.isdir(comp_directory):
                os.makedirs(comp_directory)
            
            # Build list of downloaded entries
            have = []
            for fname in glob.iglob(os.path.join(comp_directory, 'mp-*.poscar')):
                have.append(os.path.splitext(os.path.basename(fname))[0])
            #print('Have', len(have), elements_string, 'records')
            
            # Query MP for all entries corresponding to the elements
            entries = m.query({"elements": subelements}, ["material_id"])
            
            # Add entries to the list if not there
            missing = []
            for entry in entries:
                if entry['material_id'] not in have and entry['material_id'] not in missing:
                    missing.append(entry['material_id'])
            #print('Missing', len(missing), elements_string, 'records')
            
            # Download missing entries
            entries = m.query({"material_id": {"$in": missing}}, ['material_id', 'cif'])
            
            # Convert cif to poscar and save
            for entry in entries:
                struct = pmg.Structure.from_str(entry['cif'], fmt='cif')
                struct = pmg.symmetry.analyzer.SpacegroupAnalyzer(struct).get_conventional_standard_structure()
                system = am.load('pymatgen_Structure', struct)
                system = system.normalize()
                structure_file = os.path.join(comp_directory, entry['material_id']+'.poscar')
                system.dump('poscar', f=structure_file)
                print('Added', entry['material_id'])

def get_oqmd_structures(elements, lib_directory=None):
    """
    Accesses the Materials Project and downloads all structures for a list of
    elements as poscar files.
    
    Parameters
    ----------
    elements : list
        A list of element symbols.
    lib_directory : str
        Path to the lib_directory to save the poscar files to.  Default uses
        the iprPy library/dft_structures directory.
    """
    # Function-specific imports
    import requests
    
    # Get default lib_directory
    if lib_directory is None:
        lib_directory = os.path.join(os.path.dirname(rootdir), 'library', 'ref')
    lib_directory = os.path.abspath(lib_directory)
    
    # Set comp_directory
    elements.sort()
    have = []
    for subelements in subsets(elements):
        elements_string = '-'.join(subelements)
        comp_directory = os.path.join(lib_directory, elements_string)
        if not os.path.isdir(comp_directory):
            os.makedirs(comp_directory)
        
        # Build list of downloaded entries
        for fname in glob.iglob(os.path.join(comp_directory, 'oqmd-*.poscar')):
            have.append(os.path.splitext(os.path.basename(fname))[0])
    #print('Have', len(have), 'records')
    
    # Build list of missing OQMD entries
    elements_string = '-'.join(elements)
    
    composition_r = requests.get('http://oqmd.org/materials/composition/' + elements_string)
    composition_html = composition_r.text
    
    missing = []
    count = 0
    while True:
        count += 1
        try:
            start = composition_html.index('href="/materials/entry/') + len('href="/materials/entry/')
        except:
            break
        else:
            end = start + composition_html[start:].index('">')
            entry_number = composition_html[start:end]
            composition_html = composition_html[end+2:]
            entry_id = 'oqmd-'+entry_number
            if entry_id not in have and entry_id not in missing:
                missing.append(entry_id)
        if count > 100:
            raise ValueError('Loop likely infinite')
    #print('Missing', len(missing), 'records')
    
    # Download missing entries
    for entry_id in missing:
        entry_number = entry_id.replace('oqmd-', '')
        entry_r = requests.get('http://oqmd.org/materials/entry/' + entry_number)
        entry_html = entry_r.text
        
        start = entry_html.index('href="/materials/structure/') + len('href="/materials/structure/')
        end = start + entry_html[start:].index('">')
        structure_number = entry_html[start:end]
        
        try:
            structure_url = 'http://oqmd.org/materials/export/conventional/poscar/' + structure_number
            structure_r = requests.get(structure_url)
            structure_r.raise_for_status()
        except:
            try:
                structure_url = 'http://oqmd.org/materials/export/primitive/poscar/' + structure_number
                structure_r = requests.get(structure_url)
                structure_r.raise_for_status()
            except:
                continue
        
        # Save poscar
        poscar = structure_r.text
        system = am.load('poscar', poscar)
        system = system.normalize()
        elements_string = '-'.join(system.symbols)
        structure_file = os.path.join(lib_directory, elements_string, entry_id + '.poscar')
        
        with open(structure_file, 'w') as f:
            f.write(poscar)
        print('Added', entry_id)

# Define subset generator
def subsets(fullset):
    for i, item in enumerate(fullset):
        yield [item]
        if len(fullset) > 1:
            for subset in subsets(fullset[i+1:]):
                yield [item] + subset