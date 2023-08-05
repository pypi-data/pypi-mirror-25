import string


def asciify(line: str) -> str:
    """
    Receive string and return printable ascii characters + TAB as string.
    """

    if isinstance(line, str):
        ascii_printable = set(string.digits +
                              string.ascii_letters +
                              string.punctuation +
                              '\t' +
                              ' ')

        return ''.join(c for c in line if c in ascii_printable)
    else:
        raise TypeError(f"func requires a str but a {type(line).__name__} "
                        f"was passed.")
