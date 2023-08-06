from collections import deque

from epiphany.support.string import String


class Collection:
    """
    This module exports the following functions:
        queue           Returns a queue of the collection
        push            Appends a value to the collection
        position        Returns the numeric position of the value in the stack
        keyof           Returns the key for the requested value
        pair            Returns a key/value pair using the given stacks
        longest         Returns the value with the longest length
        shortest        Returns the value with the shortest length
        each            Performs a callback on each iteration
    """
    cast = dict
    keys = []
    collection_queue = None


    @property
    def collection(self):
        return self.pair(self.keys, self.vals)


    @collection.setter
    def collection(self, values):
        self.keys = list(values.keys())
        self.vals = list(values.values())


    @collection.getter
    def collection(self):
        return {k: v for k, v in zip(self.keys, self.vals)}


    def __init__(self, collection: dict):
        self.collection = self.cast(collection)

    def __getattr__(self, item):
        if item in self.collection:
            return self.collection[item]

    def __iter__(self):
        yield from self.collection


    def __str__(self):
        """
            Allows the collection to be printed in a human readable format while converting
            table style strings to title strings.

            Example:
                With a key value pair as "'first_name':'john'" in the collection, its relative
                string would be printed as "First Name: john"
        """
        return str('\n'.join(['{}: {}'.format(String(str(k)).table(), v) for k, v in self.collection.items()]))


    def queue(self):
        """ Returns the collection as a FIFO (first-in,first-out) deque stack """
        self.queue_collection = deque(tuple(self.collection))
        return self


    def push(self, value, key=None):
        """ Pushes a value to the dictionary - not requiring its key definition """
        self.keys.append(len(self.keys) + 1 if key is None else key)
        self.vals.append(value)
        return self


    def position(self, value):
        """ Returns an integer containing the numeric position of the value """
        return list(self.collection.values()).index(value)


    def keyof(self, value):
        """ Returns the key related to the value in the stack """
        return list(self.collection.keys()).pop(self.position(value))


    def pair(self, keys, values):
        """ Returns a dictionary with the keys and values paired """
        return {k: v for k, v in zip(keys, values)}


    def longest(self):
        """ Returns the value with the longest length in the collection """
        return sorted(self.vals, key=len, reverse=True).pop(0)


    def shortest(self):
        """ Returns the value with the shortest length in the collection """
        return sorted(self.vals, key=len, reverse=False).pop(0)


    def each(self, callback: callable):
        """ Performs a callback for each iteration of the key/value pair
            within the collection.

            :usage
                collection = Collection({'first_name':'john','last_name':'doe'})
                collection.each(lambda key,value: print(value))
        """
        for key, value in dict(self.collection).items():
            callback(key, value)
