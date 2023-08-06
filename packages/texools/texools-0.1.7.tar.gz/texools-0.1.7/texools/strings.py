import string
from typing import Text

from .utils import textcheck


def asciify(text_arg: Text) -> Text:
    """
    Receive string and return printable ascii characters + TAB as string.
    """

    textcheck(text_arg)
    ascii_printable = set(string.digits +
                          string.ascii_letters +
                          string.punctuation +
                          '\t' +
                          ' ')

    return ''.join(c for c in text_arg if c in ascii_printable)
