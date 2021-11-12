

class FileNotFoundError(Exception):
    ''' Raised when a path to a file is invalid'''
    pass

class InvalidFileError(Exception):
    ''' 
    Raised when a file is invalid:
    - expected to have exactly five lines
    '''
    pass