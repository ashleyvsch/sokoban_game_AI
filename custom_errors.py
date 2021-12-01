

class FileNotFoundError(Exception):
    ''' Raised when a path to a file is invalid'''
    pass

class InvalidFileError(Exception):
    ''' 
    Raised when a file is invalid:
    - expected to have exactly five lines
    '''
    pass

class BoxMoveError(Exception):
    ''' 
    Raised when a box was moved into a wall
    '''
    pass

class NotOptimalAction(Exception):
    ''' 
    Raised when a box was moved into a wall
    '''
    pass

class ValuesTooBigError(Exception):
    '''
    precision
    '''
    pass

class EndTrialsError(Exception):
    '''
    precision
    '''
    pass