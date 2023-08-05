from typing import Text


def textcheck(text: Text) -> None:
    if isinstance(text, Text):
        return True
    else:
        raise TypeError("func requires Text but "
                        "{0} was passed.".format(type(text).__name__))
