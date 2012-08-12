'''
Decorator methods to allow access from the Tailor API
'''


def tailored(func):
    ''' This decorator marks a fabric method as being viewable to tailor.'''
    func.tailored = True
    return func
    
def dependency(func):
    ''' Marks method as a dependency, not availble to the API, but is used with other API commands. '''
    func.dependency = True
    return func