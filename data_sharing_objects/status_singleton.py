### Create data classes for sharing among objects, use Singleton for that

class SingletonStatus:
    """Alex Martelli implementation of Singleton (Borg)
    http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html"""
    _shared_status_state = {}

    def __init__(self):
        self.__dict__ = self._shared_status_state


# Status class for keeping track of actual status
class Status(SingletonStatus):
    '''
    Class containing the methods used for the Singleton Status
    Attributes can be add with add() and keys can be added like in a dict
    Inherited from SingletonData.

    --------
    Methods:
    --------

    add(self, **kwargs)
    delete_item(self, del_string)

    '''
    def __init__(self):
        SingletonStatus.__init__(self)

    def add(self, **kwargs):
        '''
        Add attributes in the form: status.add(hdr=True). These attributes can then be accessed
        like keys in a dict
        @param kwargs: attributes to add
        '''
        self.__dict__.update(kwargs)

    def delete_item(self, del_string):
        '''
        Deletes the specified attribute or key
        @param del_string: attribute or key to delete
        '''
        self.__dict__.__delitem__(del_string)