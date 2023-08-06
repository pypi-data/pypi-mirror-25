import os
"""
Module for simple directory based functions
"""

def list_files(directory=os.getcwd(), file_extension=None, return_full_path=True):
    """
    List all files contained in a directory
    
    Usage:
    list_files(directory=os.getcwd(), file_extension=None, return_full_path=True)

    Input arguments:
    - directory (default=os.getcwd()): full directory path
    - file_extension (default=None): filter by file extension
    - return_full_path (default=True): full path of files (True) or relative
    """
    
    filelist = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if file_extension is not None:
        filelist = [f for f in filelist if f.endswith('.'+file_extension)]

    if return_full_path:
        filelist = [os.path.join(directory, f) for f in filelist]

    return filelist

def list_dirs(directory=os.getcwd(), return_full_path=True):
    """
    List all directories contained in a directory
    
    Usage:
    list_files(directory=os.getcwd(), file_extension=None, return_full_path=True)

    Input arguments:
    - directory (default=os.getcwd()): full directory path
    - file_extension (default=None): filter by file extension
    - return_full_path (default=True): full path of files (True) or relative
    """

    dirlist = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    if return_full_path:
        dirlist = [os.path.join(directory, d) for d in dirlist]

    return dirlist


def list_records(directory=os.getcwd(), return_full_path=True):
    """
    List all wfdb records in a directory (by finding header files).
    Wraps around list_files with .hea extension.
    
    Usage:
    list_records(directory=os.getcwd(), return_full_path=True)
    """

    filelist = list_files(directory=directory, file_extension='hea', return_full_path=return_full_path)
    recordlist = [f.split('.hea')[0] for f in filelist]

    return recordlist