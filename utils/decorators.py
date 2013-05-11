from google.appengine.api import memcache

class cached(object):
    def __init__(self, template):
        self.template = template

    def __call__(self, f):
        def wrapper(*args):
            key = self.getkey(*args)
            print 'key: ', key

            cached_data = memcache.get(key)
            
            if cached_data == None:
                cached_data = f(*args)
                memcache.set(key, cached_data)
            
            return args[0].response.write(cached_data)
        
        return wrapper

    def getkey(self, *args):
        key = self.template
        
        if len(args) > 1:
            return key + '|' + reduce(lambda x, y: x + '|' + y, args[1:])
        
        return key

