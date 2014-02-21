'''
Generic utilities.
'''


class ObjectList(object):
    '''
    @var klass: Class to instatiate when acessing bigip objecs in this list.
    '''
    klass = None
    _objects = None
    _names = None

    def __init__(self, con):
        '''
        @param con: L{Connection} instance.
        '''
        self._con = con
        self._objects = dict()
    
    @property
    def names(self):
        '''
        Lazy load object names.

        @return: List of object names.
        '''
        if not self._names:
            self._names = self._lcon.get_list()

        return self._names
    
    def get(self, name, reload=False):
        '''
        Get a Object by name.

        @param name: Name of object
        @keyword reload: Reload cache.
        @return: object.
        '''
        return self.get_multi([name], reload)

    def get_all(self, reload=False):
        '''
        Get all objects configured on the bigip.

        @keyword reload: Reload cache.
        @return: list of objects.
        '''
        return self.get_multi(self.names, reload)

    def get_multi(self, names, reload=False):
        '''
        Get a set of objects

        @param names: List of objects names to get.
        @keyword reload: Reload cache.
        @return: List of objects
        '''
        missing = list()
        objects = list()

        if reload:
            missing = names
        else:
            for name in names:
                try:
                    objects.append(self._objects[name])
                except KeyError:
                    missing.append(name)
        
        if missing:
            temp = self.load(missing)
            objects += temp
            self._objects = dict(((p.name, p) for p in temp))

        return objects

    def load(self, names):
        '''
        Read object from bigip.

        @param names: object names
        @return: list of objects
        '''
        return [self.klass(self._con, n) for n in names]
