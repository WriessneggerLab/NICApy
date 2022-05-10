class data_dict():
    '''
    Class used to creat nirx objects and others in order to behave like a dict

    --------
    Methods:
    --------

    add(self, **kwargs)

    '''
    def __init__(self):
        nothing = None

    def add(self, **kwargs):
        '''
        Add attributes in the form: nirx_physio.add(clean=cleaned_signals). These attributes can then be accessed
        like keys in a dict
        @param kwargs: attributes to add
        '''
        self.__dict__.update(kwargs)