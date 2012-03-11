def tailored(func):
    ''' This decorator marks a fabric method as being viewable to tailor.'''
    func.tailored = True
    return func
    
def change_run_to_local(func):
    ''' Change any run method to local in the method. '''
    
    func_map = {}
    func_map['run'] = 'local'
    
    return func