import re


""" 
    String Support Methods
    
    :author     Damien Rose
    :purpose    String Manipulation
    
    For the most part all methods are composed of elegant, yet readable
    one-liners intended to aid the manipulation of strings.
"""


def contains(needle: str, string: str) -> bool:
    """ Returns a boolean value depending on whether or not the neeedle
        was found within the requested string."""
    return True if string.find(needle) is not -1 else False


def where(needle: str, string: str, relative=False) -> int:
    if relative is False:
        return string.find(needle)
    return string.find(needle) + len(needle)


def length(string: str) -> int:
    """ Returns an int containing the number of words in the string
        Note:   Unlike the standard len, this method returns the number
                words in the string and NOT the number of characters """
    return len(string.split())


def from_table(string: str):
    if '_' in string:
        return ucwords(string.replace('_', ' '))
    return string.upper() if len(string) <= 3 else string.capitalize()


def table(string: str):
    """ Automatically converts table names to titles and vice versa """
    return '%s'.lower() % ('_'.join(substring.lower() for substring in string.split()))


def ucwords(string: str):
    return ' '.join(substring.title() for substring in string.split())


def lcfirst(string: str):
    """ Lowercase the first letter in the string """
    return string[0].lower() + string[1:]


def before(needle: str, string: str) -> str:
    """ Returns the substring prior to the existence of the needle """
    return string[:string.find(needle)].rstrip()


def after(needle: str, string: str) -> str:
    """ Returns the substring following the existence of the needle """
    return string[string.find(needle) + len(needle):].lstrip()


def alpha(string: str) -> str:
    """ Returns the string containing only the alpha characters """
    return re.sub('[^a-zA-Z]', '', string)


def numeric(string: str):
    """ Returns an int of the string containing only the numeric characters """
    return int(re.sub('[^\d]', '', string))


def stripnumeric(string: str):
    """ Strips all numeric characters from the string """
    return None if re.sub('[\d]', '', string) is '' else re.sub('[\d]', '', string)


def stripalpha(string: str):
    """ Strips all alpha characters from the string """
    return re.sub('[a-zA-Z]', '', string)


def autotype(string: str):
    """ If upon removing all numeric characters from the string, the string is empty.
        Return the original string as an int as it contains only numeric characters """
    return int(string) if stripnumeric(string) is '' else string
