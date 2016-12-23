import os
import glob

from ..tools import aslist, iaslist

def get_files_in_directory(directory_path, ext=None):
    """
    Function for adding all file paths within a directory or list of directories to a variable name.
    """
    file_paths = []
    
    for dir in iaslist(directory_path):
        for fname in glob.iglob(os.path.join(dir, '*')):
            fname = os.path.realpath(fname)
            if os.path.isfile(fname):
                if ext is not None and os.path.splitext(fname)[1] not in aslist(ext):
                    continue
                
                file_paths.append(fname)
                
    return file_paths