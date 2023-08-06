from json import *


class JSON:
    storage = {}


    def __init__(self, data):
        """ Determines whether or not the data provided is a string containing a JSON
            data structure and if so, loads the string as a JSON object. Otherwise,
            the assumption is made that the data is a file name, in which case
            the file is loaded and its contents are the definition of the JSON object """
        self.storage = self.insert(data) if data.startswith('{') else self.load(data)


    def __iter__(self):
        """ Allows for direct iteration over the JSON object """
        return self.storage


    def __str__(self):
        """ Prints the json object a string """
        return str(self.storage)


    def __setitem__(self, key, value):
        """ Sets the key/value pairs within the JSON object """
        self.storage[key] = value


    def __getitem__(self, item):
        """ Returns the item depending on its existence within the JSON object """
        return self.storage[item]


    def insert(self, data):
        """ Loads a string as JSON """
        return loads(data)


    def load(self, data: str):
        """ Loads the contents of a file as JSON """
        with open(data, 'r') as f:
            storage = load(f)
        return storage


    def save(self, file):
        """ Saves the JSON object (including any key/value changes) to file """
        with open(file, 'w') as f:
            dump(self.storage, f, indent=2)
