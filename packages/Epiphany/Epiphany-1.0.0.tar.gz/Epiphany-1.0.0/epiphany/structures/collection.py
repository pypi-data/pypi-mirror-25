import re

from epiphany.types import string


class Collection:
    """ Allows direct manipulation of the values contained within the collection """


    def __init__(self, data={}):
        self.data = data


    def __contains__(self, item):
        """ Checks the existence of the value within the collection """
        return item in self.data.values()


    def __iter__(self):
        """ Allows the collection class to act as an iterator for all subsequent calls """
        return self.data.items()


    def __str__(self):
        """ Returns a human readable key: value line index of the pairs within the collection """
        return ''.join(["%s: %s \n" % (string.from_table(k), v) for k, v in self.data.items()])


    def __call__(self, *args, **kwargs):
        """ Forwards calls made to the collection, to the values type class """
        result = {key: value(*args, **kwargs) for key, value in self.data.items()}
        return self.__class__(result)


    def __buildattr__(self, item):
        """ Defines the values in the collection as attributes, allowing for all
            subsequent calls made to the value, to be called via the collection """
        result = {key: getattr(value, item) for key, value in self.data.items()}
        return self.__class__(result)


    def __getitem__(self, item):
        """ Allows direct access to items within the collection """
        return self.data[item]


    def __getattr__(self, item):
        """ Returns the value of the given pair if the item is a valid collection index.
            Otherwise, an attribute is built from the values allowing for subsequent calls"""
        return self.__cast__(item) if self.has_index(item) else self.__buildattr__(item)


    def __cast__(self, item):
        """ If the requested item has no value upon removing all integers, assume its value
            is a pure integer and return its type cast accordingly."""
        return int(self[item]) if re.sub('[\d]', '', self[item]) is '' else self[item]


    def uniform_keys(self):
        self.data = {re.sub('[^a-zA-Z\d_]', '', k.lower()): v for k, v in self.data.items()}
        return self


    def has_index(self, key):
        """ Determines whether or not the requested key exists within the dictionary """
        return key in self.data.keys()


    def where(self, *needle):
        """ Returns the key of the requested needle if it exists within the dictionary """
        return [key for key, value in self.data.items() if value == needle[0]][0]
