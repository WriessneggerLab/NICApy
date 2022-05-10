### Create data classes for sharing among objects, use Singleton for that

class SingletonData:
    """Alex Martelli implementation of Singleton (Borg)
    http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html"""
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


# Data class for storing Data: filename and -paths as well as hdr and xdf data
class Data(SingletonData):
    '''
    Class containing the methods used for the Singleton Data
    Attributes can be add with add() and keys can be added like in a dict
    Inherited from SingletonData.

    --------
    Methods:
    --------

    add(self, **kwargs)
    delete_item(self, del_string)

    '''
    def __init__(self):
        SingletonData.__init__(self)

    def add(self, **kwargs):
        '''
        Add attributes in the form: data.add(analysis_path='Documents/Analysis'). These attributes can then be accessed
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