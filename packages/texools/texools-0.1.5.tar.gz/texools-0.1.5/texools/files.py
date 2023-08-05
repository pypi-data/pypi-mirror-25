from typing import Text

from os import path

from .utils import textcheck


def partspath(*parts: Text) -> Text:
    """
    Take path parts and return a joined and normalized filepath.
    """

    return path.normpath(path.join(*[str(p) for p in parts if textcheck(p)]))
