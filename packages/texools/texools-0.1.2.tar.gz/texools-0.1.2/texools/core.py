import string

from typing import Text


def asciify(text_arg: Text) -> Text:
    """
    Receive string and return printable ascii characters + TAB as string.
    """

    if isinstance(text_arg, Text):
        ascii_printable = set(string.digits +
                              string.ascii_letters +
                              string.punctuation +
                              '\t' +
                              ' ')

        return ''.join(c for c in text_arg if c in ascii_printable)
    else:
        raise TypeError(f"func requires Text but {type(text_arg).__name__} "
                        f"was passed.")
