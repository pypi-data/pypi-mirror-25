import re


class StringManifest(type):
    source_string: str = None
    source_vector: list = None


    @property
    def source(self):
        return self.source_string


    @source.setter
    def source(self, source):
        """ Updates both the source_string as well as the source_vector upon in one call """
        self.source_string = str(source)
        self.source_vector = self.source_string.split()


    @source.getter
    def source(self):
        return self.source_string


    def __str__(self):
        """ Returns the source_string when requested as a str type """
        return str(self.source_string)


    def __int__(self):
        """ Strips all non-numeric characters from the string and
            produces an integer type containing only the remaining
            integers. If no integers remain, return an int 0 """
        if re.sub('[^\d]', '', self.source_string) is '':
            return 0
        return int(re.sub('[^\d]', '', self.source_string))


    def __len__(self):
        """ Strips the all numeric characters from the string and
            returns the total number of words contained within it"""
        return len(self.strip_numeric().source.split())


    def __iter__(self):
        """ Allows for iteration over the words in the source string
            as opposed to the sources individual characters """
        yield from self.source_string.split()


class String(metaclass=StringManifest):
    """
    This module exports the following functions:
        using           Defines the source to be used throughout subsequent calls.
        concat          Concatenates a set of string or list into a string
        char_pos        Returns an integer of the character position of a substring
        word_post       Returns an integer the word position of a substring
        before          Returns a substring containing all words prior the one specified
        after           Returns a substring containing all the words following the one specified
        between         Returns the string that exists between two words/strings
        swap            Swaps a character or substring with an alternative (default: ' ')
        table           Converts table names to titles and vice versa
        strip_numeric   Strips all numeric characters from the source string.
        strip_alpha     Strips all alpha characters from the source string
        delimiter       Identifies the delimiter used to separate words within the source
    """


    @classmethod
    def using(cls, source):
        """ Defines the source to be used throughout subsequent calls """
        cls.source = str(source)
        # cls.source_vector = cls.source_string.split()
        return cls


    @classmethod
    def concat(cls, *strings):
        """ Concatenates a set of strings or list into a string """
        cls.source = ' '.join(i for i in strings)
        return cls.source


    @classmethod
    def char_pos(cls, needle) -> int:
        """ Returns the needles character position relative to the string """
        return cls.source.find(needle)


    @classmethod
    def word_pos(cls, needle) -> int:
        """ Returns the needles word position of the word within the string """
        return cls.source.split().index(needle) + 1


    @classmethod
    def before(cls, needle: str):
        """ Returns the substring prior to the existence of the needle """
        cls.source = cls.concat(*cls.source_vector[:cls.word_pos(needle) - 1])
        return cls


    @classmethod
    def after(cls, needle: str):
        """ Returns the substring following to the existence of the needle """
        cls.source = cls.concat(*cls.source_vector[cls.word_pos(needle):])
        return cls


    @classmethod
    def between(cls, start, end):
        """ Returns the substring that exists between two words/substrings """
        cls.source = cls.before(end).after(start)
        return cls


    @classmethod
    def swap(cls, needle, replacement=' '):
        """ Alternative to Pythons str.replace function """
        return str(cls.source).replace(needle, replacement)


    @classmethod
    def table(cls):
        """ Converts table names to its appropriate alternative based on the
            current pattern of the source string. """
        if re.match('^[a-z_]+', cls.source):
            cls.source = cls.swap('_').title()
        else:
            cls.source = cls.swap(' ', '_').lower()
        return cls


    @classmethod
    def strip_numeric(cls):
        """ Strips all numeric characters from the source string """
        cls.source = re.sub('[\d]', '', cls.source)
        return cls


    @classmethod
    def strip_alpha(cls):
        """ Strips all alpha characters from the source string """
        cls.source = re.sub('[_a-zA-Z]', '', cls.source)
        return cls


    @classmethod
    def delimiter(cls):
        """ Determines the delimiter used in the string by first identifying all
            characters used as word separators and finally returning the word
            separator most commonly used throughout the source string """
        match = re.findall('[^a-zA-Z\d]', cls.source)
        return list(max(zip((match.count(item) for item in set(match)), set(match)))).pop(1)

