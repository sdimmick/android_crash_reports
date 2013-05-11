from google.appengine.api import memcache

'''
Wraps request handlers in a function that does the following:
    1. Computes a unique key based on template name and function parameters
    2. Checks memcache for pre-rendered data at that key
    3. If no data is found, the request handler is called to render that data,
       which is then stored at the key.
    4. Renders the speficied template
'''
class cached(object):
    def __init__(self, template):
        self.template = template

    def __call__(self, f):
        def wrapper(*args):
            key = self.getkey(*args)
            cached_data = memcache.get(key)
            
            if cached_data == None:
                cached_data = f(*args)
                memcache.set(key, cached_data)
            
            return args[0].response.write(cached_data)
        
        return wrapper
    
    '''
    Computes a memcache key that looks like either:
        1. len(args) == 1: template_name
        2. len(args) > 1:  template_name|arg1|arg2|...
    '''
    def getkey(self, *args):
        key = self.template
        
        if len(args) > 1:
            return key + '|' + reduce(lambda x, y: x + '|' + y, str(args[1:]))
        
        return key

