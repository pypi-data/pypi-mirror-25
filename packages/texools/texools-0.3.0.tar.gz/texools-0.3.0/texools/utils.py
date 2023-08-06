from typing import Text


def textcheck(text: Text) -> bool:
    if text and isinstance(text, Text):
        return True
    else:
        raise TypeError("func requires Text but "
                        "{0} was passed.".format(type(text).__name__))


def tabify(delimiter: Text) -> Text:
    """
    Return '\t' if 'tab' passed else return passed delimiter.
    """

    if isinstance(delimiter, Text):
        if delimiter.lower() in ('tab', '\t'):
            return '\t'
        else:
            return delimiter
    else:
        raise TypeError("func requires Text but "
                        "{0} was passed.".format(type(delimiter).__name__))
