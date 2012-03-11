def tailored(func):
    ''' This decorator marks a fabric method as being viewable to tailor.'''
    func.tailored = True
    return func