def typeFilter(var):
    '''
    Get the type of a variable
    '''
    return type(var).__name__

class FilterModule(object):
    def filters(self):
        return {
            'type': typeFilter
        }
