from typing import Text

from os import path

from .utils import textcheck


def partspath(*parts: Text) -> Text:
    """
    Take path parts and return a joined and normalized filepath.
    """

    return path.normpath(path.join(*[str(p) for p in parts if textcheck(p)]))


def new_file_check(infile_path: Text, outfile_path: Text, force: bool) -> bool:
    """
    Checks for existence of new source file to process.
    1. If force then return True.
    2. If outfile_path doesn't exist then return True
    3. If outfile_path exists and infile_path is newer than outfile_path
    then return True.
    4. Else return False
    """

    if force:
        return True
    elif not path.exists(outfile_path):
        return True
    else:
        if path.getmtime(infile_path) > path.getmtime(outfile_path):
            return True
        else:
            return False
