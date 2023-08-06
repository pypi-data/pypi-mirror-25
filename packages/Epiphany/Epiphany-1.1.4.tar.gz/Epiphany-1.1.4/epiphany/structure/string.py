import re


class String(object):
    """
    This module exports the following functions:
        swap            Swaps a character or substring with an alternative (default: ' ')
        concat          Concatenates a set of string or list into a string
        char_pos        Returns an integer of the character position of a substring
        word_post       Returns an integer the word position of a substring
        before          Returns a substring containing all words prior the one specified
        after           Returns a substring containing all the words following the one specified
        between         Returns the string that exists between two words/strings
        delimiter       Identifies the delimiter used to separate words within the source
        strip_numeric   Strips all numeric characters from the source string.
        strip_alpha     Strips all alpha characters from the source string
        shortest        Returns the shortest string find in a list
        longest         Returns the longest string find in a list
        table           Converts table names to titles and vice versa
    """
    definition = {'string': '', 'delimiter': '', 'collection': []}

    delimiter = property(lambda self: self.definition.get('delimiter'))
    collection = property(lambda self: self.definition.get('collection'))


    @property
    def prototype(self):
        return self.definition.get('string')


    @prototype.setter
    def prototype(self, value):
        self.definition['string'] = str(value)
        self.definition['delimiter'] = self.__delim__(value)
        self.definition['collection'] = str(value).split(self.delimiter)


    def __init__(self, prototype):
        self.prototype = prototype


    def __str__(self):
        return self.prototype


    def __delim__(self, string: str):
        """ Determines the delimiter used in the string by first identifying all
            characters used as word separators and finally returning the word
            separator most commonly used throughout the source string """
        match = re.findall('[^a-zA-Z0-9]', string)
        return ' ' if len(match) is 0 else match.pop(0)


    def __len__(self):
        """ Returns the number of words in the string and NOT the number of characters """
        return len(self.collection)


    def __int__(self):
        """ When requesting the string as an int type, all non-numeric characters are
            removed prior to converting the prototype to a true numeric value"""
        return int(re.sub('[^\d]', '', self.prototype))


    def swap(self, needle, replacement=' '):
        """ Alternative to Pythons str.replace function """
        self.prototype = str(self.prototype).replace(needle, replacement)
        return self


    def concat(self, *prototypes):
        """ Concatenates multiple strings appended to the current prototype string """
        self.prototype = self.prototype + ' ' + ' '.join(i for i in prototypes)
        return self


    def char_pos(self, needle: str) -> int:
        """ Returns the position of the first occurrence of the first character in the needle """
        return self.prototype.find(needle)


    def word_pos(self, needle: str) -> int:
        """ Returns the position of the first occurrence of the needle in the string """
        return self.collection.index(needle) + 1


    def before(self, needle: str):
        """ Returns a substring of all the words prior to the given needle """
        self.prototype = self.prototype[:self.char_pos(needle)].rstrip(self.delimiter)
        return self


    def after(self, needle: str):
        """ Returns a substring of all the words after to the given needle """
        self.prototype = self.prototype[self.char_pos(needle) + len(needle):].lstrip(self.delimiter)
        return self


    def between(self, start, end):
        """ Returns the substring that exists between two words/substrings """
        self.prototype = self.before(end).after(start)
        return self


    def strip_numeric(self):
        """ Strips all numeric characters from the source string """
        self.prototype = re.sub('[\d]', '', self.prototype)
        return self


    def strip_alpha(self):
        """ Strips all alpha characters from the source string """
        self.prototype = re.sub('[_a-zA-Z]', '', self.prototype)
        return self


    def shortest(self):
        """ Returns the shortest word found in the string """
        return sorted(self.collection, key=len, reverse=True).pop(0)


    def longest(self):
        """ Returns the longest word found in the string """
        return sorted(self.collection, key=len, reverse=True).pop(0)


    def table(self):
        """ Converts table names to its appropriate alternative based on the
            current pattern of the prototype string. """
        if re.match('^[a-z_]+', self.prototype):
            self.prototype = self.prototype.replace(self.delimiter, ' ').title()
        else:
            self.prototype = self.prototype.replace(self.delimiter, '_').lower()
        return self
